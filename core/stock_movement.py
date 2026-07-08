import flet as ft
from core.theme import *
from models import stock_movement_model


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

    nav_column = ft.Column([
        nav_section_label("Overview"),
        nav_item("Dashboard", selected=(current_page == "Dashboard"), on_nav=on_nav),

        ft.Container(height=12),  # spacer
        nav_section_label("Master Records"),
        nav_item("User Management", selected=(current_page == "User Management"), on_nav=on_nav),
        nav_item("Supplier Management", selected=(current_page == "Supplier Management"), on_nav=on_nav),
        nav_item("Ingredients & Supplies", selected=(current_page == "Ingredients & Supplies"), on_nav=on_nav),

        ft.Container(height=12),
        nav_section_label("Operations"),
        nav_item("Inventory Monitoring", selected=(current_page == "Inventory Monitoring"), on_nav=on_nav),
        nav_item("Low-Stock Alerts", selected=(current_page == "Low-Stock Alerts"), on_nav=on_nav),
        nav_item("Purchase Orders", selected=(current_page == "Purchase Orders"), on_nav=on_nav),
        nav_item("Movement History", selected=(current_page == "Movement History"), on_nav=on_nav),

        ft.Container(height=12),
        nav_section_label("Transactions"),
        nav_item("Receiving/Stock-In", selected=(current_page == "Receiving/Stock-In"), on_nav=on_nav),
        nav_item("Stock-Out/Usage", selected=(current_page == "Stock-Out/Usage"), on_nav=on_nav),
        nav_item("Daily Sales", selected=(current_page == "Daily Sales"), on_nav=on_nav),

        ft.Container(height=12),
        nav_section_label("Insights"),
        nav_item("Reports", selected=(current_page == "Reports"), on_nav=on_nav),
    ], spacing=2, scroll=ft.ScrollMode.AUTO, expand=True,)

    profile_block = ft.Row([
        ft.Icon(ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                size=36, color=TEXT_SECONDARY),
        ft.Column([
            ft.Text(user["full_name"], size=13, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text(user["role"], size=11, color=TEXT_SECONDARY),
        ], spacing=0)
    ], spacing=8,)

    return ft.Container(
        content=ft.Column([
            logo_block,
            ft.Container(height=20),
            nav_column,
            profile_block,
        ], expand=True,),
        width=260,
        bgcolor=SIDEBAR_COLOR,
        padding=20,
    )


def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Movement History", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Movement History", size=28, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Complete audit trail of every stock-in, stock-out, sale, and adjustment",
        size=13, color=TEXT_SECONDARY)

    return ft.Column([
        breadcrumb,
        title,
        subtitle,
    ], spacing=6,)


def badge(text, bg_color, text_color='#000000'):
    return ft.Container(
        content=ft.Text(
            text, size=13, weight=ft.FontWeight.BOLD, color=text_color),
        bgcolor=bg_color,
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
    )


TYPE_COLORS = {
    "stock in": (STATUS_GREEN, "#ffffff"),
    "stock out": (STATUS_LOW, "#000000"),
    "sale": (STATUS_TEAL, "#ffffff"),
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
            ft.Text(text, size=18, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            width=width,
        )

    return ft.Container(
        content=ft.Row([
            col("Date", 140),
            col("Item", 160),
            col("Type", 130),
            col("Qty.", 100),
            col("Resulting Stock", 140),
            col("By", 150),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        padding=ft.Padding.only(left=16, right=16, top=14, bottom=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def movement_row(date, item, move_type, qty, resulting_stock, by):
    type_bg, type_text = TYPE_COLORS.get(move_type.lower(), (STATUS_TEAL, "#ffffff"))

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
            cell(date, 140),
            cell(item, 160, color=TEXT_PRIMARY, bold=True),
            ft.Container(badge(move_type, type_bg, type_text), width=130, alignment=ft.alignment.Alignment(-1, 0)),
            cell(qty, 100),
            cell(resulting_stock, 140),
            cell(by, 150),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def _qty_fmt(v, uom=""):
    try:
        v = float(v)
        if v == int(v):
            v = int(v)
        sign = "+" if v > 0 else ""  # negative values already carry their own "-"
        return f"{sign}{v} {uom}".strip()
    except (TypeError, ValueError):
        return f"{v} {uom}".strip()


def _date_fmt(dt):
    # Portable version of "%b %-d, %I:%M %p" (the %-d flag isn't available on Windows)
    return f"{dt:%b} {dt.day}, {dt:%I:%M %p}"


def _movement_type_label(row):
    """DB stores movement_type as 'Stock-In' / 'Stock-Out'. A stock-out whose
    reference_type is 'Sales' gets shown as 'Sale' instead, matching the
    original three-way badge (Stock In / Stock Out / Sale)."""
    if row.get("reference_type") == "Sales":
        return "Sale"
    return "Stock In" if row["movement_type"] == "Stock-In" else "Stock Out"


def get_movements_data(search=None):
    """Pulls live rows from models.movement instead of the old hardcoded list."""
    rows = stock_movement_model.get_movement_history(search=search)
    return [
        {
            "date": _date_fmt(r["movement_date"]),
            "item": r["item_name"],
            "type": _movement_type_label(r),
            "qty": _qty_fmt(r["quantity"], r["unit_of_measurement"]),
            "resulting_stock": _qty_fmt(r["resulting_stock"], r["unit_of_measurement"]).lstrip("+"),
            "by": r["full_name"],
        }
        for r in rows
    ]

def build_movements_table():
    rows = [table_header_row()] + [
        movement_row(item["date"], item["item"], item["type"], item["qty"], item["resulting_stock"], item["by"])
        for item in get_movements_data()
    ]

    return ft.Container(
        content=ft.Column(rows, spacing=0),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
    )


def movement_history_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Movement History", on_nav)

    header = build_header()
    search_bar = build_search_bar()
    movements_table = build_movements_table()

    main_content = ft.Container(
        content=ft.Column([
            header, search_bar, movements_table], spacing=20, scroll=ft.ScrollMode.AUTO,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )