import flet as ft
from core.theme import *


def nav_section_label(text):
    """Small gray section label for sidebar navigation"""
    return ft.Text(text.upper(), size=11, color=TEXT_SECONDARY, weight=ft.FontWeight.BOLD)


def nav_item(text, selected=False):
    """A single sidebar nav link. Bold+White if selected, muted gray otherwise."""
    return ft.Text(text, size=13, color=TEXT_PRIMARY if selected else TEXT_SECONDARY, weight=ft.FontWeight.NORMAL,)


def build_sidebar(page: ft.Page):
    logo_block = ft.Column([
        ft.Text('BUT FIRST, COFFEE', size=11,
                color=ACCENT_GOLD, weight=ft.FontWeight.BOLD),
        ft.Text('BrewTrack', size=22, color=TEXT_PRIMARY,
                weight=ft.FontWeight.BOLD),
    ], spacing=2,)

    nav_column = ft.Column([
        nav_section_label("Overview"),
        nav_item("Dashboard", selected=True),

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
        nav_item("Movement History"),

        ft.Container(height=12),
        nav_section_label("Transactions"),
        nav_item("Receiving/Stock-In"),
        nav_item("Stock-Out/Usage"),
        nav_item("Daily Sales"),

        ft.Container(height=12),
        nav_section_label("Insights"),
        nav_item("Reports"),
    ], spacing=10, expand=True,)

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


def build_header(user_name="Juan"):
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Dashboard", size=14, color=TEXT_PRIMARY),
    ], spacing=4,)

    greeting = ft.Text(f'Good day, {user_name}!', size=28,
                       color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        'Here is the current state of your brewery inventory and procurement', size=13, color=TEXT_SECONDARY)

    return ft.Column([
        breadcrumb,
        greeting,
        subtitle,
    ], spacing=6,)


def stat_card(label, value, caption):
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=12, color=TEXT_SECONDARY),
            ft.Text(value, size=26, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text(caption, size=11, color=TEXT_SECONDARY),
        ], spacing=4,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=True,
    )


def build_stats_row():
    return ft.Row([
        stat_card("Total Ingredients", "1,234", "As of today"),
        stat_card("Low Stock Items", "56", "Needs attention"),
        stat_card("Pending Orders", "12", "Awaiting approval"),
        stat_card("Daily Sales", "₱4,567", "Today so far"),
    ], spacing=16,)


def badge(text, bg_color, text_color='#000000'):
    return ft.Container(
        content=ft.Text(
            text, size=11, weight=ft.FontWeight.BOLD, color=text_color),
        bgcolor=bg_color,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=20,
    )


STATUS_COLORS = {
    "low": STATUS_LOW,
    "pending": STATUS_LOW,
    "approved": STATUS_GREEN,
    "stock-in": STATUS_GREEN,
    "stock-out": STATUS_RED,
    "sale": STATUS_TEAL,
}


def stock_list_row(name, info, status_text, status_color, text_color='#000000'):
    return ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(name, size=14, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(info, size=11, color=TEXT_SECONDARY),
            ], spacing=2),
            badge(status_text, status_color, text_color),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=12,
    )


def panel_header(title):
    return ft.Row([
        ft.Text(title, size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.Text('View All', size=12, color=TEXT_SECONDARY),
            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED,
                    size=14, color=TEXT_SECONDARY),
        ], spacing=4, )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,)


low_stock_data = [
    {"name": "Coffee Bean", "info": "145 kg on hand • reorder at 150", "status": "Low"},
    {"name": "Matcha Powder", "info": "120 g on hand • reorder at 150", "status": "Low"},
    {"name": "Oatmilk", "info": "1 L on hand • reorder at 3", "status": "Low"},
    {"name": "Vanilla Syrup", "info": "2 L on hand • reorder at 5", "status": "Low"},
]


def build_low_stock_card():
    rows = [
        stock_list_row(item["name"], item["info"],
                       item["status"], STATUS_COLORS["low"])
        for item in low_stock_data
    ]

    return ft.Container(
        content=ft.Column(
            [panel_header("Low-Stock Alerts")] + rows,
            spacing=10,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=True,
    )


def movement_list_row(tag_text, tag_color, title, subtitle, amount_text, amount_color):
    return ft.Container(
        content=ft.Row([
            badge(tag_text, tag_color, '#ffffff'),
            ft.Column([
                ft.Text(title, size=14, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=11, color=TEXT_SECONDARY),
            ],
                spacing=2,
                expand=True,),
            ft.Text(amount_text, size=13, color=amount_color,
                    weight=ft.FontWeight.BOLD),
        ], spacing=12),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=12,
    )


movements_data = [
    {"tag": "Stock-In", "title": "Coffee Bean • PO...",
        "subtitle": "Marco Reyes | Jun 30, 12:22 AM", "amount": "+1000 units", "color": STATUS_GREEN},
    {"tag": "Stock-Out", "title": "Matcha Powder • Ba...",
        "subtitle": "Marco Reyes | Jul 12, 12:22 AM", "amount": "- 220 g", "color": STATUS_LOW},
    {"tag": "Sale", "title": "Oatmilk • Restock from...",
        "subtitle": "Jose Santos | Aug 14, 12:22 AM", "amount": "- 3 cases", "color": STATUS_RED},
    {"tag": "Stock-Out", "title": "Vanilla Syrup • Restock...",
        "subtitle": "Kim Chua | Sep 1, 12:22 AM", "amount": "+ 6 bottles", "color": STATUS_GREEN},
]


def build_movements_card():
    rows = [
        movement_list_row(
            item["tag"],
            STATUS_COLORS[item["tag"].lower()],
            item["title"],
            item["subtitle"],
            item["amount"],
            item["color"],
        )
        for item in movements_data
    ]

    return ft.Container(
        content=ft.Column(
            [panel_header("Recent Stock Movements")] + rows,
            spacing=10,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=True,
    )



def dashboard_view(page: ft.Page):
    sidebar = build_sidebar(page)

    header = build_header('Juan')
    stats_row = build_stats_row()
    low_stock_card = build_low_stock_card()
    movements_card = build_movements_card()

    cards_row = ft.Row(
        [low_stock_card, movements_card],
        spacing=16,
    )

    main_content = ft.Container(
        content=ft.Column([
            header, stats_row, cards_row], spacing=20,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )
