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
        nav_item("User Management", selected=True),
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
        ft.Text("User Management", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("User Management", size=28, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Manage staff and admin accounts and their access", size=13, color=TEXT_SECONDARY)

    add_user_btn = ft.ElevatedButton(
        content=ft.Text("Add User", size=13, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
        bgcolor=ACCENT_GOLD,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            padding=ft.Padding.symmetric(horizontal=18, vertical=18),
        ),
    )

    title_row = ft.Row(
        [
            ft.Column([title, subtitle], spacing=6),
            add_user_btn,
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


ROLE_COLORS = {
    "owner/ admin": (ACCENT_GOLD, "#000000"),
    "staff": (STATUS_TEAL, "#ffffff"),
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
            col("Name", 220),
            col("Email", 260),
            col("Role", 150),
            col("Status", 140),
            ft.Container(width=80),  # lines up with the action icons below
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        padding=ft.Padding.only(left=16, right=16, top=14, bottom=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def user_row(name, email, role, status):
    role_bg, role_text = ROLE_COLORS.get(role.lower(), (STATUS_TEAL, "#ffffff"))

    return ft.Container(
        content=ft.Row([
            ft.Container(
                ft.Text(name, size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                width=220,
            ),
            ft.Container(
                ft.Text(email, size=15, color=TEXT_SECONDARY),
                width=260,
            ),
            ft.Container(badge(role, role_bg, role_text), width=150, alignment=ft.alignment.Alignment(-1, 0)),
            ft.Container(badge(status, STATUS_GREEN, "#ffffff"), width=140, alignment=ft.alignment.Alignment(-1, 0)),
            ft.Container(
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED,
                        icon_size=18,
                        icon_color=TEXT_PRIMARY,
                        tooltip="Edit user",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_ROUNDED,
                        icon_size=18,
                        icon_color=STATUS_RED,
                        tooltip="Delete user",
                    ),
                ], spacing=0),
                width=80,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


users_data = [
    {"name": "Dana Whitfield", "email": "owner@brewtrack.com", "role": "Owner/ Admin", "status": "Active"},
    {"name": "Marco Reyes", "email": "staff@brewtrack.com", "role": "Staff", "status": "Active"},
    {"name": "Priya Nair", "email": "priya@brewtrack.com", "role": "Staff", "status": "Active"},
    {"name": "Sam Okafor", "email": "sam@brewtrack.com", "role": "Staff", "status": "Active"},
]


def build_users_table():
    rows = [table_header_row()] + [
        user_row(item["name"], item["email"], item["role"], item["status"])
        for item in users_data
    ]

    return ft.Container(
        content=ft.Column(rows, spacing=0),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
    )


def user_management_view(page: ft.Page):
    sidebar = build_sidebar(page)

    header = build_header()
    search_bar = build_search_bar()
    users_table = build_users_table()

    main_content = ft.Container(
        content=ft.Column([
            header, search_bar, users_table], spacing=20, scroll=ft.ScrollMode.AUTO,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )