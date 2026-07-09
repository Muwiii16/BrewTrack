import flet as ft
from core.theme import *
from core.components import _sidebar_section_title
from models import inventory_model

def staff_low_stock_alerts_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
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
    
    sidebar = build_sidebar("Low-Stock Alerts")

    items = inventory_model.get_low_stock_items()
    for i in items:
        cq = float(i["current_quantity"]); rl = float(i["reorder_level"]) if i["reorder_level"] else 0
        if cq <= 0: i["urgency"] = "Out of Stock"
        elif rl > 0 and (cq / rl) <= 0.34: i["urgency"] = "Critical"
        else: i["urgency"] = "Low"

    def _border(): return ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER))

    def filter_chip(label, count, selected=False):
        return ft.Container(content=ft.Text(f"{label} {count}", size=13, color=TEXT_PRIMARY if selected else TEXT_MUTED, weight="bold" if selected else "normal"), bgcolor="#2a2a2a" if selected else None, border=_border(), border_radius=20, padding=12)

    def item_card(item):
        bg, txt, label = ("#330000", "#F44336", item["urgency"]) if item["urgency"] == "Out of Stock" else (("#002b2b", "#00BCD4", item["urgency"]) if item["urgency"] == "Critical" else ("#332400", ACCENT, item["urgency"]))
        prog = max(0.0, min(1.0, float(item["current_quantity"]) / float(item["reorder_level"]))) if float(item["reorder_level"]) > 0 else 0
        return ft.Container(expand=True, border=_border(), border_radius=8, padding=16, content=ft.Column([
            ft.Row([ft.Column([ft.Text(item["item_name"], size=18, weight="bold"), ft.Text(item["supplier_name"] or "-", size=12, color=TEXT_MUTED)], spacing=2), ft.Container(expand=True), ft.Container(content=ft.Text(label, size=11, weight="bold", color=txt), bgcolor=bg, padding=8, border_radius=20)], vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Row([ft.Text(f"{item['current_quantity']:g} {item['unit_of_measurement']} On Hand", size=15, weight="bold"), ft.Container(expand=True), ft.Text(f"threshold {item['reorder_level']:g}", size=12, color=TEXT_MUTED)]),
            ft.ProgressBar(value=prog, bgcolor=CARD_BORDER, color=txt, height=4), ft.Container(height=8),
            ft.Container(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text("Record Usage", size=13, color="#000000", weight="bold")]), bgcolor=ACCENT, border_radius=6, padding=12, ink=True, on_click=lambda e: global_navigate_to("Stock-Out/ Usage") if global_navigate_to else None)
        ], spacing=8))

    grid_rows = []
    for idx in range(0, len(items), 2):
        pair = items[idx:idx + 2]
        cards = [item_card(p) for p in pair]
        if len(cards) == 1: cards.append(ft.Container(expand=True))
        grid_rows.append(ft.Row(cards, spacing=16))

    main_content = ft.Container(expand=True, padding=24, content=ft.Column(scroll="auto", spacing=20, controls=[
        ft.Column([ft.Text("Low-Stocks Alert", size=28, weight="bold", color=TEXT_PRIMARY), ft.Text("Items running low, ranked by urgency.", size=13, color=TEXT_MUTED)], spacing=6),
        ft.Row([filter_chip("All", len(items), True), filter_chip("Out of Stock", sum(1 for i in items if i["urgency"] == "Out of Stock")), filter_chip("Critical", sum(1 for i in items if i["urgency"] == "Critical"))], spacing=10),
        ft.Column(grid_rows, spacing=16)
    ]))
    return ft.Row([sidebar, main_content], expand=True, spacing=0)