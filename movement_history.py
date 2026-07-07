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
        nav_item("Inventory Monitoring"),
        nav_item("Low-Stock Alerts"),
        nav_item("Purchase Orders"),
        nav_item("Movement History", selected=True),

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


movements_data = [
    {"date": "Jul 3, 1:46 AM", "item": "Coffee Bean", "type": "Stock Out", "qty": "-50 kg", "resulting_stock": "350 kg", "by": "Dana Whitfield"},
    {"date": "Jul 2, 1:46 AM", "item": "Coffee Bean", "type": "Stock In", "qty": "-100 kg", "resulting_stock": "350 kg", "by": "Dana Whitfield"},
    {"date": "Jul 2, 1:46 AM", "item": "Matcha Powder", "type": "Stock Out", "qty": "-75 g", "resulting_stock": "250 g", "by": "Priya Nair"},
    {"date": "Jun 1, 1:46 AM", "item": "Oatmilk", "type": "Stock Out", "qty": "-1 L", "resulting_stock": "5 L", "by": "Sam Okafor"},
    {"date": "Jun 1, 1:46 AM", "item": "Vanilla Syrup", "type": "Sale", "qty": "-1 L", "resulting_stock": "10 L", "by": "Marco Reyes"},
]


def build_movements_table():
    rows = [table_header_row()] + [
        movement_row(item["date"], item["item"], item["type"], item["qty"], item["resulting_stock"], item["by"])
        for item in movements_data
    ]

    return ft.Container(
        content=ft.Column(rows, spacing=0),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
    )


def movement_history_view(page: ft.Page):
    sidebar = build_sidebar(page)

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