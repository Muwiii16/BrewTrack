import flet as ft
from core.theme import *
from core.components import _sidebar_section_title
from models import inventory_model

def staff_inventory_monitoring_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):

    def navigate_to(e, view_name):
        if global_navigate_to:
            global_navigate_to(view_name)

    def build_sidebar(active_view: str):
        user_name = user["full_name"] if user else "Juan Dela Cruz"
        user_role = user["role"] if user else "Owner / Admin"

        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10), border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT, ink=True,
                on_click=lambda e: navigate_to(e, title),
                content=ft.Text(title, size=13, color=TEXT_PRIMARY if is_active else "#CCCCCC", weight="bold" if is_active else "normal"),
            )

        return ft.Column(
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
        
    # FIX 1: Wrap the sidebar in the styled container
    sidebar_container = ft.Container(
        content=build_sidebar("Inventory Monitoring"),
        width=240, bgcolor=PANEL_LEFT_BG, padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )

    items = inventory_model.get_inventory_overview()
    rows = []
    
    # Custom Row Table Header
    rows.append(ft.Container(padding=16, border=ft.Border(bottom=ft.BorderSide(1, CARD_BORDER)), content=ft.Row([
        ft.Container(ft.Text("Item", size=16, weight="bold"), width=200),
        ft.Container(ft.Text("Supplier", size=16, weight="bold"), width=170),
        ft.Container(ft.Text("Stock Level", size=16, weight="bold"), width=170),
        ft.Container(ft.Text("Status", size=16, weight="bold"), width=130),
    ], alignment="spaceBetween")))

    for i in items:
        cq = float(i["current_quantity"]); rl = float(i["reorder_level"]) if i["reorder_level"] else 0
        if cq <= 0: bg, txt, label = "#330000", "#F44336", "Out of Stock"
        elif cq <= rl: bg, txt, label = "#332400", ACCENT, "Low"
        else: bg, txt, label = "#0f2e16", "#22c55e", "In Stock"
        
        rows.append(ft.Container(padding=16, border=ft.Border(bottom=ft.BorderSide(1, CARD_BORDER)), content=ft.Row([
            ft.Container(ft.Text(i["item_name"], size=15, weight="bold", max_lines=1), width=200),
            ft.Container(ft.Text(i["supplier_name"] or "-", size=15, color=TEXT_MUTED, max_lines=1), width=170),
            ft.Container(ft.Text(f"{cq:g} {i['unit_of_measurement']}", size=15, weight="bold", color=txt), width=170),
            ft.Container(ft.Container(content=ft.Text(label, size=11, weight="bold", color=txt), bgcolor=bg, padding=8, border_radius=20), width=130),
        ], alignment="spaceBetween", vertical_alignment="center")))

    inv_table = ft.Container(content=ft.Column(rows, spacing=0), border_radius=6)

    # FIX 2: Declare main_content only once here
    main_content = ft.Container(expand=True, padding=24, content=ft.Column(scroll="auto", spacing=20, controls=[
        ft.Column([ft.Text("Inventory Monitoring", size=28, weight="bold", color=TEXT_PRIMARY), ft.Text("Live view of stock levels across all tracked items", size=13, color=TEXT_MUTED)], spacing=6),
        inv_table
    ]))
    
    return ft.Row([sidebar_container, main_content], expand=True, spacing=0)