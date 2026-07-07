import flet as ft
from core.theme import *
from core.dashboard import build_sidebar  # Reusing your existing sidebar layout

def user_row_item(name, email, role, is_admin, status, text_color="#FFFFFF"):
    """Creates a custom row item representing a single user row."""
    
    # Custom colors matching the screenshot
    role_bg = "#5A4515" if is_admin else "#1B3B3F"
    role_text = "#FFC107" if is_admin else "#4DD0E1"
    status_bg = "#1B4D1C" if status.lower() == "active" else STATUS_RED
    status_text = "#4CAF50" if status.lower() == "active" else "#FFFFFF"

    return ft.Container(
        content=ft.Row([
            # Name Column
            ft.Container(
                content=ft.Text(name, size=15, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                expand=2
            ),
            # Email Column
            ft.Container(
                content=ft.Text(email, size=14, color=TEXT_SECONDARY),
                expand=2
            ),
            # Role Column
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text(role, size=12, weight=ft.FontWeight.BOLD, color=role_text),
                        bgcolor=role_bg,
                        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        border_radius=12,
                    )
                ], alignment=ft.MainAxisAlignment.START),
                expand=2
            ),
            # Status Column
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text(status, size=12, weight=ft.FontWeight.BOLD, color=status_text),
                        bgcolor=status_bg,
                        padding=ft.Padding.symmetric(horizontal=14, vertical=6),
                        border_radius=12,
                    )
                ], alignment=ft.MainAxisAlignment.START),
                expand=1.5
            ),
            # Actions Column
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED, 
                        icon_color=TEXT_PRIMARY, 
                        icon_size=18,
                        tooltip="Edit User"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_ROUNDED, 
                        icon_color=STATUS_RED, 
                        icon_size=18,
                        tooltip="Delete User"
                    ),
                ], alignment=ft.MainAxisAlignment.END, spacing=4),
                expand=1
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(vertical=12, horizontal=16),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR))
    )

def user_management_view(page: ft.Page):
    # 1. Reuse your shared sidebar component
    sidebar = build_sidebar(page)
    
    # Update active item visual states manually if desired, 
    # or leave as configured in your original sidebar layout builder.

    # 2. Header Block Layout
    header_title_block = ft.Row([
        ft.Icon(ft.Icons.CHROME_READER_MODE_ROUNDED, size=20, color=TEXT_SECONDARY),
        ft.Text("User Management", size=14, color=TEXT_SECONDARY, weight=ft.FontWeight.BOLD),
    ], spacing=6)

    title_and_button_row = ft.Row([
        ft.Column([
            ft.Text("User Management", size=28, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Text("Manage staff and admin accounts and their access", size=12, color=TEXT_SECONDARY),
        ], spacing=2),
        ft.ElevatedButton(
            text="Add User",
            bgcolor="#F0B440",
            color="#000000",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                text_style=ft.TextStyle(font_family="sans-serif")
            ),
            height=36
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # 3. Search Bar Field Layout
    search_input = ft.TextField(
        hint_text="Search",
        hint_style=ft.TextStyle(color=TEXT_SECONDARY, size=13),
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        bgcolor="#1C1816",
        border_radius=6,
        border_color=ft.Colors.TRANSPARENT,
        height=36,
        width=300,
        content_padding=ft.Padding.symmetric(vertical=0, horizontal=10)
    )

    # 4. Table Header Row Layout
    table_header = ft.Container(
        content=ft.Row([
            ft.Text("Name", size=15, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD, expand=2),
            ft.Text("Email", size=15, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD, expand=2),
            ft.Text("Role", size=15, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD, expand=2),
            ft.Text("Status", size=15, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD, expand=1.5),
            ft.Text("", expand=1) # Spacer for actions header match
        ]),
        padding=ft.Padding.symmetric(vertical=10, horizontal=16),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR))
    )

    # Mock Data matching the design spec
    users_data = [
        {"name": "Dana Whitfield", "email": "owner@brewtrack.com", "role": "Owner/ Admin", "is_admin": True, "status": "Active"},
        {"name": "Marco Reyes", "email": "staff@brewtrack.com", "role": "Staff", "is_admin": False, "status": "Active"},
        {"name": "Priya Nair", "email": "priya@brewtrack.com", "role": "Staff", "is_admin": False, "status": "Active"},
        {"name": "Sam Okafor", "email": "sam@brewtrack.com", "role": "Staff", "is_admin": False, "status": "Active"},
    ]

    # Generating dataset rows dynamically
    table_rows = [
        user_row_item(
            u["name"], u["email"], u["role"], u["is_admin"], u["status"]
        ) for u in users_data
    ]

    # Compiling custom grid inside a standard styled Container block 
    users_table_card = ft.Container(
        content=ft.Column([
            table_header,
            *table_rows
        ], spacing=0),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
    )

    # 5. Right Main Canvas layout composite logic
    main_content = ft.Container(
        content=ft.Column([
            header_title_block,
            ft.Container(height=10),
            title_and_button_row,
            ft.Container(height=10),
            search_input,
            ft.Container(height=15),
            users_table_card
        ], spacing=10, scroll=ft.ScrollMode.AUTO),
        expand=True,
        padding=24
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )