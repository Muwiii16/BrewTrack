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
        nav_item("Movement History"),

        ft.Container(height=12),
        nav_section_label("Transactions"),
        nav_item("Receiving/Stock-In", selected=True),
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
        ft.Text("Receiving/ Stock-In", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Receiving/ Stock-In", size=28, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Log incoming deliveries to add them into inventory", size=13, color=TEXT_SECONDARY)

    return ft.Column([
        breadcrumb,
        title,
        subtitle,
    ], spacing=6,)


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


def build_record_delivery_card():
    item_dropdown = ft.Dropdown(
        hint_text="Select Item",
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

    quantity_field = form_field("0")
    source_field = form_field("e.g. PO-1043 or supplier delivery")

    awaiting_delivery_box = ft.Container(
        content=ft.Column([
            ft.Text("Awaiting Delivery", size=12, color=TEXT_SECONDARY),
            ft.Text("PO-1008 | ZXC Farm", size=15, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        ], spacing=4),
        bgcolor=CARD_COLOR,
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=14,
    )

    add_to_inventory_btn = ft.ElevatedButton(
        content=ft.Text("Add to Inventory", size=13, weight=ft.FontWeight.BOLD, color="#000000"),
        bgcolor=STATUS_GREEN,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            padding=ft.Padding.symmetric(horizontal=18, vertical=18),
        ),
        width=float("inf"),
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Record Delivery", size=20, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                field_label("Item"),
                item_dropdown,
                ft.Container(height=14),
                field_label("Quantity Received"),
                quantity_field,
                ft.Container(height=14),
                field_label("Source/ Reference"),
                source_field,
                ft.Container(height=14),
                awaiting_delivery_box,
                ft.Container(height=20),
                add_to_inventory_btn,
            ],
            spacing=6,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=24,
        expand=True,
    )


def stock_in_entry(item, qty, note, date):
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
                    ft.Text(qty, size=14, color=TEXT_SECONDARY),
                    ft.Text(date, size=12, color=TEXT_SECONDARY),
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.END,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


recent_stock_in_data = [
    {"item": "Coffee Beans", "qty": "+ 20 kg", "note": "PO-1008 received | Marco (Staff)", "date": "Jul 15, 5:00 PM"},
]


def build_recent_stock_in_card():
    entries = [stock_in_entry(item["item"], item["qty"], item["note"], item["date"])
               for item in recent_stock_in_data]

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Recent Stock-In", size=20, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
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


def receiving_stock_in_view(page: ft.Page):
    sidebar = build_sidebar(page)

    header = build_header()
    record_delivery_card = build_record_delivery_card()
    recent_stock_in_card = build_recent_stock_in_card()

    panels_row = ft.Row(
        [record_delivery_card, recent_stock_in_card],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    main_content = ft.Container(
        content=ft.Column([
            header, panels_row], spacing=20, scroll=ft.ScrollMode.AUTO,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )