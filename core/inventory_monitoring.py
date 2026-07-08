import flet as ft
from core.theme import *
from models import inventory_model


def nav_section_label(text):
    """Small gray section label for sidebar navigation"""
    return ft.Text(text.upper(), size=11, color=TEXT_SECONDARY, weight=ft.FontWeight.BOLD)


def nav_item(text, selected=False, on_nav=None):
    """A single sidebar nav link. Bold+White if selected, muted gray otherwise."""
    return ft.Container(
        content=ft.Text(
            text,
            size=13,
            color=TEXT_PRIMARY if selected else TEXT_SECONDARY,
            weight=ft.FontWeight.NORMAL
        ),
        on_click=lambda e: on_nav(text) if on_nav else None,
        padding=ft.Padding.symmetric(vertical=6, horizontal=12),
        border_radius=6,
        ink=True,
    )


def build_sidebar(page: ft.Page, user, on_logout, current_page, on_nav):
    logo_block = ft.Column([
        ft.Image(src='assets/BFC_logo.jpg', width=140, fit=ft.BoxFit.CONTAIN),
        ft.Text('BrewTrack', size=22, color=TEXT_PRIMARY,
                weight=ft.FontWeight.BOLD),
    ], spacing=6,)

    is_staff = user["role"].lower() == "staff"

    if is_staff:
        nav_groups = [
            ("Overview", ["Dashboard"]),
            ("Operations", ["Inventory Monitoring",
             "Low-Stock Alerts", "Movement History"]),
            ("Transactions", ["Receiving/Stock-In",
             "Stock-Out/Usage", "Daily Sales"]),
        ]
    else:
        nav_groups = [
            ("Overview", ["Dashboard"]),
            ("Master Records", ["User Management",
             "Supplier Management", "Ingredients & Supplies"]),
            ("Operations", ["Inventory Monitoring", "Low-Stock Alerts",
             "Purchase Orders", "Movement History"]),
            ("Transactions", ["Receiving/Stock-In",
             "Stock-Out/Usage", "Daily Sales"]),
            ("Insights", ["Reports"]),
        ]

    nav_children = []
    for label, items in nav_groups:
        nav_children.append(nav_section_label(label))
        for item in items:
            nav_children.append(nav_item(item, selected=(
                current_page == item), on_nav=on_nav))
        nav_children.append(ft.Container(height=12))

    nav_column = ft.Column(nav_children, spacing=4,
                           scroll=ft.ScrollMode.AUTO, expand=True,)

    profile_block = ft.Row([
        ft.Icon(ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                size=36, color=TEXT_SECONDARY),
        ft.Column([
            ft.Text(user["full_name"], size=13,
                    color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Text(user["role"], size=11, color=TEXT_SECONDARY),
        ], spacing=0),
        ft.Container(expand=True),
        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color=ACCENT_GOLD,
                      on_click=lambda e: on_logout(), alignment=ft.Alignment.CENTER_RIGHT),
    ], spacing=8,)

    return ft.Container(
        content=ft.Column([logo_block, ft.Container(
            height=20), nav_column, profile_block], expand=True,),
        width=260,
        bgcolor=SIDEBAR_COLOR,
        padding=20,
    )


def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Inventory Monitoring", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Inventory Monitoring", size=28, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Live view of stock levels across all tracked items", size=13, color=TEXT_SECONDARY)

    return ft.Column([
        breadcrumb,
        title,
        subtitle,
    ], spacing=6,)


def stat_card(label, value):
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=12, color=TEXT_SECONDARY),
            ft.Text(value, size=22, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
        ], spacing=6,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=True,
    )


def _qty_fmt(v, uom=""):
    try:
        v = float(v)
        if v == int(v):
            v = int(v)
        return f"{v} {uom}".strip()
    except (TypeError, ValueError):
        return f"{v} {uom}".strip()


def _money_fmt(v):
    try:
        return f"P {float(v):,.2f}"
    except (TypeError, ValueError):
        return "P 0.00"


def _item_status(current_quantity, reorder_level):
    current_quantity = float(current_quantity)
    reorder_level = float(reorder_level)
    if current_quantity <= 0:
        return "Out of Stock"
    if current_quantity <= reorder_level:
        return "Low"
    return "In Stock"


def build_stats_row():
    total_items = len(inventory_model.get_inventory_overview())
    inventory_value = sum(float(i["value"])
                          for i in inventory_model.get_inventory_overview())
    low_or_out = sum(
        1 for i in inventory_model.get_inventory_overview() if float(i["current_quantity"]) <= float(i["reorder_level"])
    )
    out_of_stock = sum(1 for i in inventory_model.get_inventory_overview(
    ) if float(i["current_quantity"]) <= 0)

    return ft.Row([
        stat_card("Total Items", str(total_items)),
        stat_card("Inventory Value", _money_fmt(inventory_value)),
        stat_card("Low/ Out of Stock", str(low_or_out)),
        stat_card("Out of Stock", str(out_of_stock)),
    ], spacing=16,)


def badge(text, bg_color, text_color='#000000'):
    return ft.Container(
        content=ft.Text(
            text, size=13, weight=ft.FontWeight.BOLD, color=text_color),
        bgcolor=bg_color,
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
    )


STATUS_COLORS = {
    "in stock": (STATUS_GREEN, "#ffffff"),
    "low": (STATUS_LOW, "#000000"),
    "out of stock": (STATUS_RED, "#ffffff"),
}


def build_search_bar():
    return ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SEARCH_ROUNDED, size=16, color=TEXT_SECONDARY),
            ft.TextField(
                hint_text="Search",
                border=ft.InputBorder.NONE,
                height=45,
                text_size=13,
                color=TEXT_PRIMARY,
                hint_style=ft.TextStyle(color=TEXT_SECONDARY, size=13),
                content_padding=ft.Padding.symmetric(horizontal=0, vertical=8),
                expand=True,
            ),
        ], spacing=8),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=12, vertical=2),
        width=340,
    )


def table_header_row():
    def col(text, width):
        return ft.Container(
            ft.Text(text, size=18, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            width=width,
        )

    return ft.Container(
        content=ft.Row([
            col("Item", 200),
            col("Supplier", 170),
            col("Stock Level", 170),
            col("Value", 150),
            col("Status", 130),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        padding=ft.Padding.only(left=16, right=16, top=14, bottom=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def inventory_row(item, supplier, stock_level, value, status):
    status_bg, status_text = STATUS_COLORS.get(
        status.lower(), (STATUS_GREEN, "#ffffff"))
    # Stock level text takes on the same color as the row's status badge
    stock_level_color = STATUS_LOW if status.lower() == "low" else STATUS_GREEN

    def cell(text, width, color=TEXT_SECONDARY, bold=False):
        return ft.Container(
            ft.Text(
                text, size=15, color=color,
                weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
                max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
            ),
            width=width,
        )

    return ft.Container(
        content=ft.Row([
            cell(item, 200, color=TEXT_PRIMARY, bold=True),
            cell(supplier, 170),
            cell(stock_level, 170, color=stock_level_color, bold=True),
            cell(value, 150),
            ft.Container(badge(status, status_bg, status_text),
                         width=130, alignment=ft.alignment.Alignment(-1, 0)),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def get_inventory_data():
    """Pulls live rows from models.inventory instead of the old hardcoded list."""
    items = inventory_model.get_inventory_overview()
    return [
        {
            "item": i["item_name"],
            "supplier": i["supplier_name"] or "-",
            "stock_level": _qty_fmt(i["current_quantity"], i["unit_of_measurement"]),
            "value": _money_fmt(i["value"]),
            "status": _item_status(i["current_quantity"], i["reorder_level"]),
        }
        for i in items
    ], items


def build_inventory_table():
    rows = [table_header_row()] + [
        inventory_row(item["item"], item["supplier"],
                      item["stock_level"], item["value"], item["status"])
        for item in get_inventory_data()[0]
    ]

    return ft.Container(
        content=ft.Column(rows, spacing=0),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
    )


def inventory_monitoring_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout,
                            "Inventory Monitoring", on_nav)

    header = build_header()
    stats_row = build_stats_row()
    search_bar = build_search_bar()
    inventory_table = build_inventory_table()

    main_content = ft.Container(
        content=ft.Column([
            header, stats_row, search_bar, inventory_table], spacing=20, scroll=ft.ScrollMode.AUTO,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )
