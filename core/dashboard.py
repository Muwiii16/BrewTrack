import flet as ft
from core.theme import *


def _sidebar_section_title(title: str):
    return ft.Container(
        padding=ft.Padding.only(top=10, bottom=5),
        content=ft.Text(title, size=11, color=TEXT_MUTED, weight="w500"),
    )


def _sidebar_link(title: str, active: bool = False):
    return ft.Container(
        padding=ft.Padding.symmetric(vertical=6, horizontal=10),
        border_radius=6,
        bgcolor="#1A1A1A" if active else ft.Colors.TRANSPARENT,
        ink=True,
        on_click=lambda e: None,
        content=ft.Text(
            title,
            size=13,
            color=TEXT_PRIMARY if active else "#CCCCCC",
            weight="bold" if active else "normal",
        ),
    )


def _po_summary_card_small(title: str, value: str):
    return ft.Container(
        expand=1,
        padding=20,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(title, size=12, color=TEXT_MUTED),
                ft.Text(value, size=24, weight="bold", color=TEXT_PRIMARY),
            ]
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
            weight="bold",
            color=fg_color
        )
    )


def _po_list_item(po_num, status, supplier, date_created, expected_date, amount, items_count, chips: list):
    status_bg = "#332400" if status == "Pending" else "#0A290A"
    status_fg = ACCENT if status == "Pending" else "#4CAF50"
    
    chip_controls = []
    for chip in chips:
        chip_controls.append(
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                border=ft.Border.all(1, CARD_BORDER),
                border_radius=16,
                content=ft.Text(chip, size=11, color=TEXT_MUTED)
            )
        )
        
    return ft.Container(
        padding=20,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        content=ft.Row(
            alignment="spaceBetween",
            vertical_alignment="start",
            controls=[
                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.Text(po_num, size=16, weight="bold", color=TEXT_PRIMARY),
                                _badge(status, status_bg, status_fg)
                            ]
                        ),
                        ft.Text(f"{supplier} | Created {date_created} | Expected {expected_date}", size=12, color=TEXT_MUTED),
                        ft.Row(spacing=10, controls=chip_controls)
                    ]
                ),
                ft.Row(
                    spacing=20,
                    vertical_alignment="start",
                    controls=[
                        ft.Column(
                            horizontal_alignment="end",
                            spacing=4,
                            controls=[
                                ft.Text(amount, size=16, weight="bold", color=TEXT_PRIMARY),
                                ft.Text(f"{items_count} line item(s)", size=12, color=TEXT_MUTED)
                            ]
                        ),
                        ft.PopupMenuButton(
                            icon=ft.Icons.MORE_HORIZ,
                            icon_color=TEXT_PRIMARY,
                            items=[
                                ft.PopupMenuItem(content=ft.Text("Approve", color="#4CAF50")),
                                ft.PopupMenuItem(content=ft.Text("Cancel Order", color="#F44336")),
                            ]
                        )
                    ]
                )
            ]
        )
    )


def _cell(text, is_bold=False):
    return ft.DataCell(ft.Text(text, size=13, weight="bold" if is_bold else "normal", color=TEXT_PRIMARY))


def _summary_card(title: str, value: str, subtitle: str = None):
    controls = [
        ft.Text(title, size=12, color=TEXT_MUTED),
        ft.Text(value, size=24, weight="bold", color=TEXT_PRIMARY),
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
                    alignment="spaceBetween",
                    controls=[
                        ft.Text(title, size=18, weight="bold", color=TEXT_PRIMARY),
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
            alignment="spaceBetween",
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(item_name, size=14, weight="bold", color=TEXT_PRIMARY),
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
            alignment="spaceBetween",
            controls=[
                ft.Row(
                    spacing=15,
                    controls=[
                        _badge(badge_text, badge_bg, badge_fg),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(title, size=14, weight="bold", color=TEXT_PRIMARY),
                                ft.Text(desc, size=11, color=TEXT_MUTED),
                            ]
                        )
                    ]
                ),
                ft.Text(amount, size=12, weight="bold", color=amount_color)
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
                        ft.Text(po_num, size=14, weight="bold", color=TEXT_PRIMARY),
                        ft.Text(amount, size=11, color=TEXT_MUTED),
                    ]
                ),
                _badge(status, "#332400" if status == "Pending" else "#0A290A", ACCENT if status == "Pending" else "#4CAF50")
            ]
        )
    )


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

    def open_new_po_modal(e):
        # Explicitly add the dialog to the overlay and force the screen to update
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
                            # Bypassed alignment property entirely. Using right-aligned text instead.
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
        # Only navigate if it's one of the pages we have built so far
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
                # Logo Area
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Icon(ft.Icons.COFFEE, size=24, color=ACCENT),
                        ft.Text(
                            "BUT FIRST, COFFEE",
                            size=10,
                            weight="bold",
                            color=ACCENT,
                            style=ft.TextStyle(letter_spacing=1.5),
                        ),
                        ft.Text(
                            "BREWTRACK",
                            size=22,
                            weight="bold",
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
                
                # User Profile at Bottom
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
            scroll="auto",
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
                                ft.Text("Dashboard", size=14, color=TEXT_MUTED, weight="bold")
                            ]
                        ),
                        ft.Container(height=10),
                        ft.Text("Good day, Juan", size=28, weight="bold", color=TEXT_PRIMARY),
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
                    vertical_alignment="start",
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
                        alignment="spaceBetween",
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text("Purchase", size=18, weight="bold", color=TEXT_PRIMARY),
                                    ft.Text("Orders", size=18, weight="bold", color=TEXT_PRIMARY),
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
            alignment="spaceBetween",
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
                    on_click=open_new_po_modal,
                    content=ft.Text(
                        "New Purchase Order",
                        size=13,
                        weight="bold",
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
                ft.DataColumn(ft.Text("Item", size=15, weight="bold", color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("Supplier", size=15, weight="bold", color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("On Hand", size=15, weight="bold", color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("Reorder At", size=15, weight="bold", color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("Suggested Qty.", size=15, weight="bold", color=TEXT_PRIMARY)),
                ft.DataColumn(ft.Text("Status", size=15, weight="bold", color=TEXT_PRIMARY)),
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
            scroll="auto",
            spacing=30,
            controls=[
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=20, color=TEXT_MUTED),
                                ft.Text("Low-Stocks Alert", size=14, color=TEXT_MUTED, weight="bold")
                            ]
                        ),
                        ft.Container(height=10),
                        ft.Text("Low-Stocks Alert", size=28, weight="bold", color=TEXT_PRIMARY),
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
                        scroll="auto",
                        controls=[table]
                    )
                )
            ]
        )

    def build_purchase_orders_content():
        action_bar = ft.Row(
            alignment="spaceBetween",
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
                    on_click=open_new_po_modal,
                    content=ft.Text(
                        "New Purchase Order",
                        size=13,
                        weight="bold",
                        color=PANEL_LEFT_BG, 
                    )
                )
            ]
        )

        return ft.Column(
            expand=True,
            scroll="auto",
            spacing=30,
            controls=[
                # Header
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Row(
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.RECEIPT_LONG, size=20, color=TEXT_MUTED),
                                ft.Text("Purchase Order", size=14, color=TEXT_MUTED, weight="bold")
                            ]
                        ),
                        ft.Container(height=10),
                        ft.Text("Purchase Order", size=28, weight="bold", color=TEXT_PRIMARY),
                        ft.Text("Raise and track orders to your suppliers", size=12, color=TEXT_MUTED),
                    ]
                ),
                
                # Summary Cards
                ft.Row(
                    spacing=20,
                    controls=[
                        _po_summary_card_small("Open Orders", "2"),
                        _po_summary_card_small("Pending Approval", "1"),
                        _po_summary_card_small("Approved", "1"),
                        _po_summary_card_small("Received", "1"),
                    ]
                ),
                
                action_bar,
                
                # List of Purchase Orders
                ft.Column(
                    spacing=15,
                    controls=[
                        _po_list_item(
                            po_num="PO- 1001", 
                            status="Pending", 
                            supplier="ABC Farms", 
                            date_created="Jul 3, 2026", 
                            expected_date="Jul 8, 2026", 
                            amount="P 800.00", 
                            items_count="2",
                            chips=["Arabica Coffee Beans * 5 kg * P500.00", "Black Coffee Beans * 5 kg * P300.00"]
                        ),
                        _po_list_item(
                            po_num="PO- 1002", 
                            status="Approved", 
                            supplier="ABC Farms", 
                            date_created="Jul 3, 2026", 
                            expected_date="Jul 8, 2026", 
                            amount="P 1,200.00", 
                            items_count="2",
                            chips=["Ceremonial Matcha Powder * 5 kg * P600.00", "Culinary Matcha Powder * 5 kg * P600.00"]
                        ),
                    ]
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
        elif view_name == "Purchase Orders":
            main_content.content = build_purchase_orders_content()

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