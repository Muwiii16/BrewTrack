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


def dashboard_view(page: ft.Page):
    sidebar = build_sidebar(page)

    header = build_header('Juan')
    stats_row = build_stats_row()

    test_badges = ft.Row(
        [
            badge("Low", STATUS_COLORS["low"]),
            badge("Approved", STATUS_COLORS["approved"], text_color="#ffffff"),
            badge("Stock-Out",
                  STATUS_COLORS["stock-out"], text_color="#ffffff"),
        ],
        spacing=8,
    )

    main_content = ft.Container(
        content=ft.Column([
            header, stats_row, test_badges], spacing=20,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )
