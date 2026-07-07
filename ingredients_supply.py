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
        nav_item("Suppliers", selected=True),
        nav_item("Ingredients & Supplies"),

        ft.Container(height=12),
        nav_section_label("Operations"),
        nav_item("Inventory Monitoring"),
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
        ft.Text("Ingredients & Supplies", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Ingredients & Supplies", size=28, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Master catalog of raw materials, packaging, and supplies.", size=13, color=TEXT_SECONDARY)

    add_supplier_btn = ft.ElevatedButton(
        content=ft.Text("Add Item", size=13, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
        bgcolor=ACCENT_GOLD,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            padding=ft.Padding.symmetric(horizontal=18, vertical=18),
        ),
    )

    title_row = ft.Row(
        [
            ft.Column([title, subtitle], spacing=6),
            add_supplier_btn,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    return ft.Column([
        breadcrumb,
        title_row,
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
    "low stock": (STATUS_LOW, "#ffffff"),
    "in stock": (STATUS_GREEN, "#ffffff"),
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
            col("P-ID", 70),
            col("S-ID", 70),
            col("Item", 130),
            col("Category", 110),
            col("Unit", 110),
            col("Cost", 90),
            col("Reorder At", 110),
            col("Status", 110),
            ft.Container(width=80),  # lines up with the action icons below
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        padding=ft.Padding.only(left=16, right=16, top=14, bottom=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def ingredient_supply_row(pid, sid, item, category, unit, cost, reorder_at, status):
    status_bg, status_text = STATUS_COLORS.get(status.lower(), (STATUS_GREEN, "#ffffff"))

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
            cell(pid, 70, color=TEXT_PRIMARY, bold=True),
            cell(sid, 70, color=TEXT_PRIMARY, bold=True),
            cell(item, 130),
            cell(category, 110),
            cell(unit, 110),
            cell(cost, 90),
            cell(reorder_at, 110),
            ft.Container(badge(status, status_bg, status_text), width=100, alignment=ft.alignment.Alignment(-1, 0)),
            ft.Container(
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED,
                        icon_size=18,
                        icon_color=TEXT_PRIMARY,
                        tooltip="Edit item",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_ROUNDED,
                        icon_size=18,
                        icon_color=STATUS_RED,
                        tooltip="Delete item",
                    ),
                ], spacing=0),
                width=80,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


ingredient_supply_data = [
    {"pid": "P0001", "sid": "S0002", "item": "Coffee Beans", "category": "Coffee",
        "unit": "kilogram (kg)", "cost": "P 100.00", "reorder_at": "150 kg", "status": "Low Stock"},
    {"pid": "P0002", "sid": "S0001", "item": "Matcha Powder", "category": "Coffee",
        "unit": "gram (g)", "cost": "P 150.00", "reorder_at": "350 g", "status": "Low Stock"},
    {"pid": "P0003", "sid": "S0001", "item": "Oatmilk", "category": "Dairy",
        "unit": "liter (L)", "cost": "P 120.00", "reorder_at": "3 L", "status": "Low Stock"},
    {"pid": "P0004", "sid": "S0001", "item": "Vanilla Syrup", "category": "Syrup",
        "unit": "liter (L)", "cost": "P 200.00", "reorder_at": "10 L", "status": "Low Stock"},
]


def build_ingredients_supply_table():
    rows = [table_header_row()] + [
        ingredient_supply_row(item["pid"], item["sid"], item["item"], item["category"], item["unit"],
                     item["cost"], item["reorder_at"], item["status"])
        for item in ingredient_supply_data
    ]

    return ft.Container(
        content=ft.Column(rows, spacing=0),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
    )


def ingredients_supply_view(page: ft.Page):
    sidebar = build_sidebar(page)

    header = build_header()
    search_bar = build_search_bar()
    ingredients_supply_table = build_ingredients_supply_table()

    main_content = ft.Container(
        content=ft.Column([
            header, search_bar, ingredients_supply_table], spacing=20, scroll=ft.ScrollMode.AUTO,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )