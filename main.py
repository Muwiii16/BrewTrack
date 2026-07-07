import flet as ft
from db_connection import DatabaseConnection # Make sure database.py is in the same folder

def get_users_from_db():
    """Fetches all users from the database."""
    users = []
    conn = DatabaseConnection.get_connection() 
    
    if not conn:
        print("Could not connect to database.")
        return users

    try:
        cursor = conn.cursor(dictionary=True)
        # Fetching the fields needed for our UI
        cursor.execute("SELECT user_id, full_name, email, role, status FROM users")
        users = cursor.fetchall()
        cursor.close()
    except Exception as err:
        print(f"Query execution error: {err}")
    finally:
        DatabaseConnection.close_connection(conn) 
        
    return users

def main(page: ft.Page):
    # --- Page Configuration ---
    page.title = "BrewTrack - User Management"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141414" 
    page.padding = 40
    page.window_width = 1000
    page.window_height = 700

    # --- Helper Functions for UI Elements ---
    def create_badge(text, text_color, bg_color):
        return ft.Container(
            content=ft.Text(text, color=text_color, weight=ft.FontWeight.BOLD, size=13),
            bgcolor=bg_color,
            # Updated to modern Padding class structure
            padding=ft.Padding(left=12, top=6, right=12, bottom=6),
            border_radius=15,
        )

    def create_action_buttons(user_id):
        # We pass user_id here so later you can attach functions to edit/delete specific users
        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.EDIT, 
                    icon_color=ft.Colors.WHITE, 
                    icon_size=20, 
                    tooltip="Edit User",
                    data=user_id # Store the ID in the button's data attribute
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE, 
                    icon_color=ft.Colors.RED_500, 
                    icon_size=20, 
                    tooltip="Delete User",
                    data=user_id
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.END
        )

    # --- Dynamic Styling Helpers ---
    def get_role_colors(role):
        role_lower = role.lower()
        if "admin" in role_lower or "owner" in role_lower:
            return "#F3C354", "#3D311A" # Amber/Yellow
        return "#4DD0E1", "#193B3D"     # Teal for Staff

    def get_status_colors(status):
        status_lower = status.lower()
        if status_lower == "active":
            return "#5EE25E", "#1B3A1B" # Green
        return "#FF5252", "#3A1B1B"     # Red for Inactive/Suspended

    # --- 1. Header Section ---
    header = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text("User Management", size=32, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Manage staff and admin accounts and their access", 
                        color=ft.Colors.WHITE60, 
                        size=14
                    ),
                ],
                spacing=2,
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # --- 2. Search Bar ---
    search_bar = ft.Container(
        content=ft.TextField(
            hint_text="Search",
            hint_style=ft.TextStyle(color=ft.Colors.WHITE24),
            prefix_icon=ft.Icons.SEARCH,
            filled=True,
            bgcolor="#1E1E1E",
            border_color="transparent",
            border_radius=20,
            height=40,
            content_padding=ft.Padding(left=15, top=0, right=15, bottom=0),
            text_size=14,
        ),
        width=250,
        margin=ft.Margin(left=0, top=20, right=0, bottom=20)
    )

    # --- 3. Data Table (Empty Initially) ---
    users_table = ft.DataTable(
        expand=True,
        bgcolor="#1C1A1A",
        border=ft.Border(
            top=ft.BorderSide(1, "#333333"),
            right=ft.BorderSide(1, "#333333"),
            bottom=ft.BorderSide(1, "#333333"),
            left=ft.BorderSide(1, "#333333")
        ),
        border_radius=10,
        heading_row_height=60,
        data_row_min_height=60,
        data_row_max_height=60,
        divider_thickness=1,
        column_spacing=40,
        columns=[
            ft.DataColumn(ft.Text("Name", size=18, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Email", size=18, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Role", size=18, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Status", size=18, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("")), # Empty header for Actions
        ],
        rows=[] # Rows will be added dynamically
    )

    # --- Render Page Outline First ---
    page.add(
        header,
        search_bar,
        ft.Row([users_table]) 
    )

    # --- 4. Populate Table Function ---
    def load_user_data():
        users_table.rows.clear()
        user_records = get_users_from_db()

        for user in user_records:
            r_text_color, r_bg_color = get_role_colors(user['role'])
            s_text_color, s_bg_color = get_status_colors(user['status'])

            users_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(user['full_name'], weight=ft.FontWeight.BOLD, size=15)),
                    ft.DataCell(ft.Text(user['email'], color=ft.Colors.WHITE70, size=15)),
                    ft.DataCell(create_badge(user['role'].title(), r_text_color, r_bg_color)),
                    ft.DataCell(create_badge(user['status'].title(), s_text_color, s_bg_color)),
                    ft.DataCell(create_action_buttons(user['user_id'])), 
                ])
            )
        page.update()

    # Trigger the database fetch and UI update
    load_user_data()

ft.app(target=main)