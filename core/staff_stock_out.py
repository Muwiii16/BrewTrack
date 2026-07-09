import flet as ft
from core.theme import *
from core.components import _sidebar_section_title
from models import inventory_model, stock_movement_model

def staff_stock_out_usage_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    def build_sidebar(active_view: str):
        user_name = user["full_name"] if user else "Staff Member"
        user_role = user["role"] if user else "Staff"

        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10), border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT, ink=True,
                on_click=lambda e: global_navigate_to(title) if global_navigate_to else None,
                content=ft.Text(title, size=13, color=TEXT_PRIMARY if is_active else "#CCCCCC", weight="bold" if is_active else "normal"),
            )

        return ft.Container(
            width=240, bgcolor=PANEL_LEFT_BG, padding=20, border=ft.Border(right=ft.BorderSide(1, CARD_BORDER)),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Column(spacing=2, controls=[
                        ft.Icon(ft.Icons.COFFEE, size=24, color=ACCENT),
                        ft.Text("BUT FIRST, COFFEE", size=10, weight="bold", color=ACCENT, style=ft.TextStyle(letter_spacing=1.5)),
                        ft.Text("BREWTRACK", size=22, weight="bold", color=TEXT_PRIMARY, font_family=FONT_HEADING),
                    ]),
                    ft.Divider(height=30, color=CARD_BORDER),
                    ft.Column(
                        expand=True, spacing=2, scroll="hidden",
                        controls=[
                            _sidebar_section_title("Overview"), _sidebar_link("Dashboard"),
                            _sidebar_section_title("Operations"), _sidebar_link("Inventory Monitoring"), _sidebar_link("Low-Stock Alerts"), _sidebar_link("Movement History"),
                            _sidebar_section_title("Transactions"), _sidebar_link("Receiving/ Stock-In"), _sidebar_link("Stock-Out/ Usage"), _sidebar_link("Daily Sales"),
                        ]
                    ),
                    ft.Divider(height=20, color=CARD_BORDER),
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Row(spacing=12, controls=[
                                ft.CircleAvatar(bgcolor=TEXT_PRIMARY, color=PANEL_LEFT_BG, radius=18, content=ft.Icon(ft.Icons.PERSON, size=20)),
                                ft.Column(spacing=0, controls=[ft.Text(user_name, size=13, weight="bold", color=TEXT_PRIMARY), ft.Text(user_role, size=11, color=TEXT_MUTED)])
                            ]),
                            ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ACCENT, icon_size=20, tooltip="Log Out", on_click=lambda e: show_login() if show_login else None)
                        ]
                    )
                ]
            )
        )
    
    sidebar = build_sidebar("Stock-Out/ Usage")

    items = inventory_model.get_inventory_overview()
    usage_state = {i["item_id"]: 0 for i in items}
    qty_refs = {i["item_id"]: {} for i in items}
    
    usage_list_col = ft.Column(spacing=8)
    reason_dd = ft.Dropdown(value="Ingredient Usage", options=[ft.dropdown.Option("Ingredient Usage"), ft.dropdown.Option("Waste / Spoilage")], border_color=CARD_BORDER, color=TEXT_PRIMARY, bgcolor=INPUT_BG)
    log_btn = ft.Container(
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text("Log Shift Usage", size=14, color="#000000", weight="bold")]),
        bgcolor=ACCENT, border_radius=6, padding=12, ink=True, disabled=True, opacity=0.5
    )

    def _border(): return ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER))

    def refresh_usage_list():
        usage_list_col.controls.clear()
        active = [(item, usage_state[item["item_id"]]) for item in items if usage_state[item["item_id"]] > 0]
        if not active:
            usage_list_col.controls.append(ft.Column([ft.Icon(ft.Icons.TOUCH_APP_ROUNDED, size=32, color=TEXT_MUTED), ft.Text("Tap items to build usage list", size=12, color=TEXT_MUTED)], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
            log_btn.disabled = True; log_btn.opacity = 0.5
        else:
            for item, qty in active:
                usage_list_col.controls.append(ft.Container(border=_border(), border_radius=6, padding=12, content=ft.Row([
                    ft.Column([ft.Text(item["item_name"], size=13, weight="bold", color=TEXT_PRIMARY), ft.Text(f"{qty:g} {item['unit_of_measurement']}", size=11, color=TEXT_MUTED)], spacing=2, expand=True),
                    ft.IconButton(ft.Icons.CLOSE_ROUNDED, icon_size=16, on_click=make_change(item["item_id"], -9999))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)))
            log_btn.disabled = False; log_btn.opacity = 1
        page.update()

    def log_shift(e):
        for item in [i for i in items if usage_state[i["item_id"]] > 0]:
            inventory_model.stock_out(item["item_id"], usage_state[item["item_id"]], user["user_id"] if user else 1, reason_dd.value, remarks=reason_dd.value)
            usage_state[item["item_id"]] = 0
            qty_refs[item["item_id"]]["control"].value = "0"
        page.snack_bar = ft.SnackBar(ft.Text("Shift usage logged!"), bgcolor=ft.Colors.GREEN_800); page.snack_bar.open = True
        refresh_usage_list()
    log_btn.on_click = log_shift

    def make_change(item_id, delta):
        def handler(e):
            item = next(i for i in items if i["item_id"] == item_id)
            step = 0.5 if item["unit_of_measurement"] in ["kg", "L", "l"] else 1
            usage_state[item_id] = max(0, usage_state[item_id] + (delta * step) if delta != -9999 else 0)
            qty_refs[item_id]["control"].value = f"{usage_state[item_id]:g}"
            refresh_usage_list()
        return handler

    cards = []
    for item in items:
        qty_text = ft.Text("0", size=16, weight="bold", color=TEXT_PRIMARY, text_align=ft.TextAlign.CENTER)
        qty_refs[item["item_id"]]["control"] = qty_text
        cards.append(ft.Container(expand=True, border=_border(), border_radius=8, padding=16, content=ft.Column([
            ft.Row([ft.Text(item["item_name"], size=15, weight="bold", color=TEXT_PRIMARY)]), ft.Container(height=4),
            ft.Row([
                ft.Container(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.REMOVE_ROUNDED, size=16)]), width=32, height=32, border=_border(), border_radius=6, on_click=make_change(item["item_id"], -1), ink=True),
                ft.Container(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[qty_text]), expand=True),
                ft.Container(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.ADD_ROUNDED, size=16)]), width=32, height=32, border=_border(), border_radius=6, on_click=make_change(item["item_id"], 1), ink=True),
                ft.Text(item["unit_of_measurement"], size=13, color=TEXT_MUTED)
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ], spacing=4)))

    grid_rows = []
    for idx in range(0, len(cards), 2):
        pair = cards[idx:idx + 2]
        if len(pair) == 1: pair.append(ft.Container(expand=True))
        grid_rows.append(ft.Row(pair, spacing=16))

    refresh_usage_list()

    main_content = ft.Container(expand=True, padding=24, content=ft.Column(scroll="auto", spacing=20, controls=[
        ft.Column([ft.Text("Stock-Out/ Usage", size=28, weight="bold", color=TEXT_PRIMARY), ft.Text("Tap items through your shift, then log the batch.", size=13, color=TEXT_MUTED)], spacing=6),
        ft.Row(spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, controls=[
            ft.Container(expand=2, border=_border(), border_radius=6, padding=16, content=ft.Column([ft.Text("Tap to Add", size=16, weight="bold", color=TEXT_PRIMARY)] + grid_rows, spacing=16)),
            ft.Container(expand=1, border=_border(), border_radius=6, padding=16, content=ft.Column([ft.Text("Usage List", size=16, weight="bold", color=TEXT_PRIMARY), ft.Container(usage_list_col, padding=20), reason_dd, log_btn], spacing=12))
        ])
    ]))
    return ft.Row([sidebar, main_content], expand=True, spacing=0)