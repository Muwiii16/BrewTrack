import flet as ft
from theme import *


def nav_section_label(text):
    """Small gray section label for sidebar navigation"""
    return ft.Text(text.upper(), size=11, color=TEXT_SECONDARY, weight=ft.FontWeight.BOLD)


def nav_item(text, selected=False):
    """A single sidebar nav link. Bold+White if selected, muted gray otherwise."""
    return ft.Text(text, size=13, color=TEXT_PRIMARY if selected else TEXT_SECONDARY, weight=ft.FontWeight.NORMAL,)


def build_sidebar(page: ft.Page):
    logo_block = ft.Column([
        ft.Image(src='assets/BFC_logo.jpg', width=140, fit=ft.BoxFit.CONTAIN),
        ft.Text('BrewTrack', size=22, color=TEXT_PRIMARY,
                weight=ft.FontWeight.BOLD),
    ], spacing=6,)

    nav_column = ft.Column([
        nav_section_label("Overview"),
        nav_item("Dashboard"),

        ft.Container(height=12),  # spacer
        nav_section_label("Master Records"),
        nav_item("User Management"),
        nav_item("Suppliers"),
        nav_item("Ingredients & Supplies"),

        ft.Container(height=12),
        nav_section_label("Operations"),
        nav_item("Inventory Monitoring", selected=True),
        nav_item("Low-Stock Alerts"),
        nav_item("Purchase Orders"),
        nav_item("Movement History"),

        ft.Container(height=12),
        nav_section_label("Transactions"),
        nav_item("Receiving/Stock-In"),
        nav_item("Stock-Out/Usage"),
        nav_item("Daily Sales"),

        ft.Container(height=12),
        nav_section_label("Insights"),
        nav_item("Reports"),
    ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True,)

    profile_block = ft.Row([
        ft.Icon(ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                size=36, color=TEXT_SECONDARY),
        ft.Column([
            ft.Text("John Doe", size=13, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text("Admin", size=11, color=TEXT_SECONDARY),
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


def build_stats_row():
    return ft.Row([
        stat_card("Total Items", "14"),
        stat_card("Inventory Value", "P 5,691"),
        stat_card("Low/ Out of Stock", "7"),
        stat_card("Out of Stock", "0"),
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
            ft.Text(text, size=18, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
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
    status_bg, status_text = STATUS_COLORS.get(status.lower(), (STATUS_GREEN, "#ffffff"))
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
            ft.Container(badge(status, status_bg, status_text), width=130, alignment=ft.alignment.Alignment(-1, 0)),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


inventory_data = [
    {"item": "Coffee Bean", "supplier": "ABC Company", "stock_level": "2 kg", "value": "P 1,116.00", "status": "In Stock"},
    {"item": "Matcha Powder", "supplier": "ABC Company", "stock_level": "300 g", "value": "P 1,123.00", "status": "Low"},
    {"item": "Oatmilk", "supplier": "ABC Company", "stock_level": "1 L", "value": "P 760.25", "status": "In Stock"},
    {"item": "Vanilla Syrup", "supplier": "ZXC Farm", "stock_level": "1 L", "value": "P 2,093.50", "status": "Low"},
]


def build_inventory_table():
    rows = [table_header_row()] + [
        inventory_row(item["item"], item["supplier"], item["stock_level"], item["value"], item["status"])
        for item in inventory_data
    ]

    return ft.Container(
        content=ft.Column(rows, spacing=0),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
    )


def inventory_monitoring_view(page: ft.Page):
    sidebar = build_sidebar(page)

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