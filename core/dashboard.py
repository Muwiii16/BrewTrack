import flet as ft
from core.theme import *

def _sidebar_section_title(title: str):
    return ft.Container(
        padding=ft.Padding.only(top=10, bottom=5),
        content=ft.Text(title, size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_500),
    )

def _summary_card(title: str, value: str, subtitle: str = None):
    controls = [
        ft.Text(title, size=12, color=TEXT_MUTED),
        ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
    ]
    if subtitle:
        controls.append(ft.Text(subtitle, size=11, color=TEXT_MUTED))
        
    return ft.Container(
        expand=1,
        padding=20,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.Column(
            spacing=4,
            controls=controls
        )
    )

def _badge(text: str, bg_color: str, fg_color: str):
    return ft.Container(
        bgcolor=bg_color,
        border_radius=12,
        padding=ft.Padding.symmetric(horizontal=12, vertical=4),
        content=ft.Text(
            text,
            size=11,
            weight=ft.FontWeight.BOLD,
            color=fg_color
        )
    )

def _panel_container(title: str, content_controls: list):
    return ft.Container(
        expand=1,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        padding=20,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Row(
                            spacing=4,
                            controls=[
                                ft.Text("View all", size=11, color=TEXT_MUTED),
                                ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=TEXT_MUTED)
                            ]
                        )
                    ]
                ),
                ft.Column(spacing=10, controls=content_controls)
            ]
        )
    )

def _low_stock_row(item_name: str, desc: str):
    return ft.Container(
        padding=15,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(item_name, size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text(desc, size=11, color=TEXT_MUTED),
                    ]
                ),
                _badge("Low", "#332400", ACCENT)
            ]
        )
    )

def _movement_row(badge_text: str, badge_bg: str, badge_fg: str, title: str, desc: str, amount: str, amount_color: str):
    return ft.Container(
        padding=15,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=15,
                    controls=[
                        _badge(badge_text, badge_bg, badge_fg),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                ft.Text(desc, size=11, color=TEXT_MUTED),
                            ]
                        )
                    ]
                ),
                ft.Text(amount, size=12, weight=ft.FontWeight.BOLD, color=amount_color)
            ]
        )
    )

def _po_card(po_num: str, amount: str, status: str):
    return ft.Container(
        padding=15,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        content=ft.Row(
            spacing=15,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(po_num, size=14, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text(amount, size=11, color=TEXT_MUTED),
                    ]
                ),
                _badge(status, "#332400" if status == "Pending" else "#0A290A", ACCENT if status == "Pending" else "#4CAF50")
            ]
        )
    )

def _cell(text, is_bold=False):
    return ft.DataCell(ft.Text(text, size=13, weight=ft.FontWeight.BOLD if is_bold else ft.FontWeight.NORMAL, color=TEXT_PRIMARY))


def dashboard_view(page: ft.Page):
    
    # Containers to hold the dynamic parts of our layout
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

    def navigate_to(e, view_name):
        # Only navigate if it's one of the pages we have built so far
        if view_name in ["Dashboard", "Low-Stock Alerts"]:
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
                    weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                ),
            )

        return ft.Column(
            expand=True,
            controls=[
                # Logo Area
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Icon(ft.Icons.COFFEE, size=24, color=ACCENT),
                        ft.Text(
                            "BUT FIRST, COFFEE",
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=ACCENT,
                            style=ft.TextStyle(letter_spacing=1.5),
                        ),
                        ft.Text(
                            "BREWTRACK",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                            font_family=FONT_HEADING,
                        ),
                    ]
                ),
                ft.Divider(height=30, color=CARD_BORDER),
                
                # Navigation
                ft.Column(
                    expand=True,
                    spacing=2,
                    scroll=ft.ScrollMode.HIDDEN,
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
                
                # User Profile at Bottom
                ft.Divider(height=20, color=CARD_BORDER),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
                                        ft.Text("Juan Dela Cruz", size=13, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                        ft.Text("Owner / Admin", size=11, color=TEXT_MUTED),
                                    ]
                                )
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            icon_color=ACCENT,
                            icon_size=20,
                            tooltip="Log Out"
                        )
                    ]
                )
            ]
        )

    def build_overview_content():
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=30,
            controls=[
                # Header
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.DASHBOARD_ROUNDED, size=20, color=TEXT_MUTED),
                                ft.Text("Dashboard", size=14, color=TEXT_MUTED, weight=ft.FontWeight.BOLD)
                            ]
                        ),
                        ft.Container(height=10),
                        ft.Text("Good day, Juan", size=28, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text("Here is the current state of your brewery inventory and procurement", size=12, color=TEXT_MUTED),
                    ]
                ),
                
                # Summary Cards
                ft.Row(
                    spacing=20,
                    controls=[
                        _summary_card("Inventory Value", "P5,691", "14 tracked items"),
                        _summary_card("Low/ Out of Stock", "7", "Needs attention"),
                        _summary_card("Pending Approval", "1", "2 open orders"),
                        _summary_card("Sales Today", "$0", "$2,367 recent total"),
                    ]
                ),
                
                # Middle Section (Split Panels)
                ft.Row(
                    expand=True,
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        _panel_container(
                            "Low-Stock Alerts",
                            [
                                _low_stock_row("Coffee Bean", "145 kg on hand * reorder at 150"),
                                _low_stock_row("Matcha Powder", "120 g on hand * reorder at 150"),
                                _low_stock_row("Oatmilk", "1 L on hand * reorder at 3"),
                                _low_stock_row("Vanilla Syrup", "2 L on hand * reorder at 5"),
                            ]
                        ),
                        _panel_container(
                            "Recent Stock Movements",
                            [
                                _movement_row("Stock-In", "#0A290A", "#4CAF50", "Coffee Bean * PO...", "Marco Reyes | Jun 30, 12:22 AM", "+1000 units", "#4CAF50"),
                                _movement_row("Stock-Out", "#330000", "#F44336", "Matcha Powder * Ba...", "Marco Reyes | Jul 12, 12:22 AM", "- 220 g", "#FF9800"),
                                _movement_row("Sale", "#002b2b", "#00BCD4", "Oatmilk * Restock from...", "Jose Santos | Aug 14, 12:22 AM", "- 3 cases", "#FF9800"),
                                _movement_row("Stock-Out", "#330000", "#F44336", "Vanilla Syrup * Restock...", "Kim Chua | Sep 1, 12:22 AM", "+ 6 bottles", "#4CAF50"),
                            ]
                        ),
                    ]
                ),
                
                # Footer Section (Purchase Orders)
                ft.Container(
                    border=ft.Border.all(1, CARD_BORDER),
                    border_radius=8,
                    padding=20,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text("Purchase", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                    ft.Text("Orders", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                ]
                            ),
                            ft.Row(
                                spacing=15,
                                controls=[
                                    _po_card("PO- 1008", "P 1,548.00", "Pending"),
                                    _po_card("PO- 1009", "P 612.00", "Pending"),
                                    _po_card("PO- 1010", "P 2,500.00", "Approved"),
                                ]
                            ),
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.Text("View all", size=11, color=TEXT_MUTED),
                                    ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=TEXT_MUTED)
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    def build_low_stock_content():
        action_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.TextField(
                    hint_text="Search",
                    hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                    prefix_icon=ft.Icons.SEARCH,
                    bgcolor=INPUT_BG,
                    border_color=ft.Colors.TRANSPARENT,
                    border_radius=8,
                    content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                    height=40,
                    width=300,
                ),
                ft.Container(
                    bgcolor=ACCENT,
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                    ink=True,
                    on_click=lambda e: None,
                    content=ft.Text(
                        "New Purchase Order",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=PANEL_LEFT_BG, 
                    )
                )
            ]
        )

        table = ft.DataTable(
            expand=True,
            bgcolor=ft.Colors.TRANSPARENT,
            border=ft.Border.all(1, CARD_BORDER),
            border_radius=8,
            heading_row_color="#1A1A1A",
            heading_row_height=50,
            data_row_min_height=60,
            data_row_max_height=60,
            column_spacing=40,
            columns=[
                ft.DataColumn(ft.Text("Item", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("Supplier", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("On Hand", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("Reorder At", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("Suggested Qty.", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("Status", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
            ],
            rows=[
                ft.DataRow(cells=[_cell("Coffee Bean", True), _cell("ABC Company"), _cell("145 kg"), _cell("150 kg"), _cell("350 kg"), ft.DataCell(_badge("Low", "#332400", ACCENT))]),
                ft.DataRow(cells=[_cell("Matcha Powder", True), _cell("ABC Company"), _cell("120 g"), _cell("150 g"), _cell("250 g"), ft.DataCell(_badge("Low", "#332400", ACCENT))]),
                ft.DataRow(cells=[_cell("Oatmilk", True), _cell("ABC Company"), _cell("1 L"), _cell("3 L"), _cell("5 boxes"), ft.DataCell(_badge("Low", "#332400", ACCENT))]),
                ft.DataRow(cells=[_cell("Vanilla Syrup", True), _cell("ZXC Farm"), _cell("2 L"), _cell("5 L"), _cell("10 bottles"), ft.DataCell(_badge("Low", "#332400", ACCENT))]),
            ]
        )

        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=30,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=20, color=TEXT_MUTED),
                                ft.Text("Low-Stocks Alert", size=14, color=TEXT_MUTED, weight=ft.FontWeight.BOLD)
                            ]
                        ),
                        ft.Container(height=10),
                        ft.Text("Low-Stocks Alert", size=28, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text("Items at or below their reorder level. Replenish these to avoid production stoppages", size=12, color=TEXT_MUTED),
                    ]
                ),
                ft.Row(
                    spacing=20,
                    controls=[
                        _summary_card("Items Needing Attention", "7"),
                        _summary_card("Out of Stock", "0"),
                        _summary_card("Estimated Replenishment Cost", "P 33,470.7"),
                    ]
                ),
                action_bar,
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[table]
                    )
                )
            ]
        )

    def render_view(view_name: str):
        # Update the active sidebar link
        sidebar_container.content = build_sidebar(view_name)
        
        # Swap the main layout content
        if view_name == "Dashboard":
            main_content.content = build_overview_content()
        elif view_name == "Low-Stock Alerts":
            main_content.content = build_low_stock_content()

    # Initialize the dashboard to the overview page on first load
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