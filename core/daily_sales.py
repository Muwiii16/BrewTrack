import flet as ft
from core.theme import *
from models import stock_out_model

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
        ft.Image(src='assets/LOGO.png', width=319, fit=ft.BoxFit.CONTAIN, align=ft.Alignment.CENTER),
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
        nav_item("Low-Stock Items", selected=(current_page == "Low-Stock Items"), on_nav=on_nav),
        nav_item("Purchase Orders", selected=(current_page == "Purchase Orders"), on_nav=on_nav),
        nav_item("Movement History", selected=(current_page == "Movement History"), on_nav=on_nav),

        ft.Container(height=12),
        nav_section_label("Transactions"),
        nav_item("Receiving/Stock-In", selected=(current_page == "Receiving/Stock-In"), on_nav=on_nav),
        nav_item("Usage/Stock-Out", selected=(current_page == "Usage/Stock-Out"), on_nav=on_nav),
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
        ], spacing=0),
        ft.Container(expand=True),  # spacer
        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color=ACCENT_GOLD, 
                on_click=lambda e: on_logout(), alignment=ft.Alignment.CENTER_RIGHT),
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
        ft.Text("Daily Sales Recording", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Daily Sales Recording", size=28, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Record sales and automatically deduct the ingredients they consume",
        size=13, color=TEXT_SECONDARY)

    return ft.Column([
        breadcrumb,
        title,
        subtitle,
    ], spacing=6,)


# --- Stat cards (same pattern as dashboard.py's stat_card) ---

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
        stat_card("Today's Revenue", "P 0.00"),
        stat_card("Units Sold Today", "0"),
        stat_card("Transactions Today", "0"),
    ], spacing=16,)


def field_label(text):
    return ft.Text(text, size=15, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD)


def form_field(hint=""):
    return ft.TextField(
        hint_text=hint,
        bgcolor=CARD_COLOR,
        border_color=BORDER_COLOR,
        focused_border_color=ACCENT_GOLD,
        color=TEXT_PRIMARY,
        hint_style=ft.TextStyle(color=TEXT_SECONDARY, size=13),
        text_size=13,
        border_radius=6,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
    )


def build_new_sale_card():
    product_field = form_field("e.g. Arabica Coffee Beans")
    quantity_field = form_field("0")
    revenue_field = form_field("P 0.00")

    ingredients_dropdown = ft.Dropdown(
        hint_text="+ Add",
        options=[
            ft.dropdown.Option("Coffee Beans"),
            ft.dropdown.Option("Matcha Powder"),
            ft.dropdown.Option("Oatmilk"),
            ft.dropdown.Option("Vanilla Syrup"),
        ],
        bgcolor=CARD_COLOR,
        border_color=BORDER_COLOR,
        focused_border_color=ACCENT_GOLD,
        color=TEXT_PRIMARY,
        text_size=13,
        border_radius=6,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=12),
    )

    record_sale_btn = ft.ElevatedButton(
        content=ft.Text("Record Sale", size=13, weight=ft.FontWeight.BOLD, color="#000000"),
        bgcolor=ACCENT_GOLD,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            padding=ft.Padding.symmetric(horizontal=18, vertical=18),
        ),
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("New Sale", size=20, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                field_label("Product"),
                product_field,
                ft.Container(height=14),
                ft.Row(
                    [
                        ft.Column([field_label("Quantity"), quantity_field], spacing=8, expand=True),
                        ft.Column([field_label("Revenue"), revenue_field], spacing=8, expand=True),
                    ],
                    spacing=16,
                ),
                ft.Container(height=14),
                field_label("Ingredients Consumed (optional)"),
                ingredients_dropdown,
                ft.Container(height=20),
                record_sale_btn,
            ],
            spacing=6,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=24,
        expand=True,
    )


def sale_entry(item, revenue, note, date):
    return ft.Row(
        [
            ft.Column(
                [
                    ft.Text(item, size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                    ft.Text(note, size=13, color=TEXT_SECONDARY),
                ],
                spacing=4,
                expand=True,
            ),
            ft.Column(
                [
                    ft.Text(revenue, size=14, color=TEXT_SECONDARY),
                    ft.Text(date, size=12, color=TEXT_SECONDARY),
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.END,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


recent_sales_data = [
    {"item": "18x Coffee Beans", "revenue": "P 5,000.00", "note": "Marco (Staff)", "date": "Jul 29, 5:00 PM"},
]


def build_recent_sales_card():
    entries = [sale_entry(item["item"], item["revenue"], item["note"], item["date"])
               for item in recent_sales_data]

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Recent Sales", size=20, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                *entries,
            ],
            spacing=16,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=24,
        expand=True,
    )


def daily_sales_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Daily Sales", on_nav)

    header = build_header()
    stats_row = build_stats_row()
    new_sale_card = build_new_sale_card()
    recent_sales_card = build_recent_sales_card()

    panels_row = ft.Row(
        [new_sale_card, recent_sales_card],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # 1. Isolate the header so it stays pinned
    header_block = ft.Container(
        content=header,
        padding=ft.Padding.only(bottom=20),
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_COLOR))
    )

    # 2. Wrap the stats and panels in a scrollable block
    main_block = ft.Container(
        content=ft.Column(
            [stats_row, panels_row], 
            spacing=20, 
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        padding=ft.Padding.only(top=20),
    )

    # 3. Combine them in the main layout (no scrolling here!)
    main_content = ft.Container(
        content=ft.Column(
            [header_block, main_block], 
            spacing=0, 
        ),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )