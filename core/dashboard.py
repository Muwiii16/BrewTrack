import flet as ft
from core.theme import *
from core.components import _sidebar_section_title
from core.admin_overview import AdminOverview
from core.admin_low_stock import AdminLowStock
from core.admin_po import AdminPurchaseOrders

def dashboard_view(page: ft.Page):
    
    sidebar_container = ft.Container(
        width=240,
        bgcolor=PANEL_LEFT_BG,
        padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )
    
    main_content = ft.Container(
        expand=True,
        padding=40
    )

    def open_new_po_modal(e):
        if new_po_dialog not in page.overlay:
            page.overlay.append(new_po_dialog)
        new_po_dialog.open = True
        page.update()

    def close_new_po_modal(e):
        new_po_dialog.open = False
        page.update()

    new_po_dialog = ft.AlertDialog(
        bgcolor=PANEL_RIGHT_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        title=ft.Column(
            spacing=4,
            controls=[
                ft.Text("New Purchase Order", size=24, weight="bold", color=TEXT_PRIMARY),
                ft.Text("Order stock from a supplier. Costs default to each item's unit cost", size=12, color=TEXT_MUTED)
            ]
        ),
        content=ft.Container(
            width=600,
            content=ft.Column(
                tight=True,
                spacing=20,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                expand=1,
                                controls=[
                                    ft.Text("Supplier", size=14, weight="bold", color=TEXT_PRIMARY),
                                    ft.Dropdown(
                                        hint_text="Select Supplier",
                                        hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                                        bgcolor=INPUT_BG,
                                        border_color=INPUT_BORDER,
                                        border_radius=8,
                                        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                                        options=[
                                            ft.dropdown.Option("ABC Farms"),
                                            ft.dropdown.Option("ZXC Farm")
                                        ]
                                    )
                                ]
                            ),
                            ft.Column(
                                expand=1,
                                controls=[
                                    ft.Text("Expected Date", size=14, weight="bold", color=TEXT_PRIMARY),
                                    ft.TextField(
                                        hint_text="dd/mm/yy",
                                        hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                                        bgcolor=INPUT_BG,
                                        border_color=INPUT_BORDER,
                                        border_radius=8,
                                        suffix_icon=ft.Icons.CALENDAR_TODAY,
                                        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                                    )
                                ]
                            )
                        ]
                    ),
                    ft.Text("Line Items", size=14, weight="bold", color=TEXT_PRIMARY),
                    ft.Row(
                        vertical_alignment="center",
                        controls=[
                            ft.Dropdown(
                                expand=2,
                                hint_text="Choose supplier list",
                                hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                                bgcolor=INPUT_BG,
                                border_color=INPUT_BORDER,
                                border_radius=8,
                                text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                            ),
                            ft.TextField(
                                expand=1,
                                hint_text="Qty",
                                hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                                bgcolor=INPUT_BG,
                                border_color=INPUT_BORDER,
                                border_radius=8,
                                text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                            ),
                            ft.Text(
                                "P 0.00", 
                                size=14, 
                                weight="bold", 
                                color=TEXT_PRIMARY,
                                text_align="right",
                                width=80
                            ),
                            ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color="#F44336")
                        ]
                    ),
                    ft.Container(
                        padding=ft.Padding.symmetric(vertical=10, horizontal=20),
                        border=ft.Border.all(1, INPUT_BORDER),
                        border_radius=8,
                        ink=True,
                        on_click=lambda e: None,
                        content=ft.Text("+ Add Line", size=12, color=TEXT_MUTED)
                    ),
                    ft.Divider(color=CARD_BORDER),
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Text("Order Total", size=18, weight="bold", color=TEXT_PRIMARY),
                            ft.Text("P 0.00", size=18, weight="bold", color=TEXT_PRIMARY)
                        ]
                    )
                ]
            )
        ),
        actions=[
            ft.TextButton(
                "Cancel", 
                style=ft.ButtonStyle(color=TEXT_MUTED),
                on_click=close_new_po_modal
            ),
            ft.Container(
                bgcolor=ACCENT,
                padding=ft.Padding.symmetric(horizontal=20, vertical=10),
                border_radius=8,
                ink=True,
                on_click=close_new_po_modal,
                content=ft.Text("Create Order", size=13, weight="bold", color=PANEL_LEFT_BG)
            )
        ]
    )

    def navigate_to(e, view_name):
        if view_name in ["Dashboard", "Low-Stock Alerts", "Purchase Orders"]:
            render_view(view_name)
            page.update()

    def build_sidebar(active_view: str):
        
        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10),
                border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT,
                ink=True,
                on_click=lambda e: navigate_to(e, title),
                content=ft.Text(
                    title,
                    size=13,
                    color=TEXT_PRIMARY if is_active else "#CCCCCC",
                    weight="bold" if is_active else "normal",
                ),
            )

        return ft.Column(
            expand=True,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Icon(ft.Icons.COFFEE, size=24, color=ACCENT),
                        ft.Text("BUT FIRST, COFFEE", size=10, weight="bold", color=ACCENT, style=ft.TextStyle(letter_spacing=1.5)),
                        ft.Text("BREWTRACK", size=22, weight="bold", color=TEXT_PRIMARY, font_family=FONT_HEADING),
                    ]
                ),
                ft.Divider(height=30, color=CARD_BORDER),
                
                ft.Column(
                    expand=True,
                    spacing=2,
                    scroll="hidden",
                    controls=[
                        _sidebar_section_title("Overview"),
                        _sidebar_link("Dashboard"),
                        
                        _sidebar_section_title("Master Records"),
                        _sidebar_link("User Management"),
                        _sidebar_link("Suppliers"),
                        _sidebar_link("Ingredients & Supplies"),
                        
                        _sidebar_section_title("Operations"),
                        _sidebar_link("Inventory Monitoring"),
                        _sidebar_link("Low-Stock Alerts"),
                        _sidebar_link("Purchase Orders"),
                        _sidebar_link("Movement History"),
                        
                        _sidebar_section_title("Transactions"),
                        _sidebar_link("Receiving/ Stock-In"),
                        _sidebar_link("Stock-Out/ Usage"),
                        _sidebar_link("Daily Sales"),
                        
                        _sidebar_section_title("Insights"),
                        _sidebar_link("Reports"),
                    ]
                ),
                
                ft.Divider(height=20, color=CARD_BORDER),
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Row(
                            spacing=12,
                            controls=[
                                ft.CircleAvatar(
                                    bgcolor=TEXT_PRIMARY,
                                    color=PANEL_LEFT_BG,
                                    radius=18,
                                    content=ft.Icon(ft.Icons.PERSON, size=20)
                                ),
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text("Juan Dela Cruz", size=13, weight="bold", color=TEXT_PRIMARY),
                                        ft.Text("Owner / Admin", size=11, color=TEXT_MUTED),
                                    ]
                                )
                            ]
                        ),
                        ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ACCENT, icon_size=20, tooltip="Log Out")
                    ]
                )
            ]
        )

    def render_view(view_name: str):
        sidebar_container.content = build_sidebar(view_name)
        
        # Route to the correct separated file!
        if view_name == "Dashboard":
            main_content.content = AdminOverview(page)
        elif view_name == "Low-Stock Alerts":
            main_content.content = AdminLowStock(page, open_new_po_modal)
        elif view_name == "Purchase Orders":
            main_content.content = AdminPurchaseOrders(page, open_new_po_modal)

    # Load default view
    render_view("Dashboard")

    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        content=ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar_container,
                main_content,
            ]
        )
    )