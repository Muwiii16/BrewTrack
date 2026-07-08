import flet as ft
from core.theme import *
from core.components import _sidebar_section_title, _badge, _cell
from models import user_model

def user_management_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):

    sidebar_container = ft.Container(
        width=240,
        bgcolor=PANEL_LEFT_BG,
        padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )
    
    main_content = ft.Container(
        expand=True,
        padding=40,
        bgcolor=BG_COLOR
    )

    def navigate_to(e, view_name):
        if global_navigate_to:
            global_navigate_to(view_name)

    def build_sidebar(active_view: str):
        user_name = user["full_name"] if user else "Juan Dela Cruz"
        user_role = user["role"] if user else "Owner / Admin"

        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10),
                border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT,
                ink=True,
                on_click=lambda e: navigate_to(e, title),
                content=ft.Text(
                    title,
                    size=13,
                    color=TEXT_PRIMARY if is_active else "#CCCCCC",
                    weight="bold" if is_active else "normal",
                ),
            )

        return ft.Column(
            expand=True,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Icon(ft.Icons.COFFEE, size=24, color=ACCENT),
                        ft.Text("BUT FIRST, COFFEE", size=10, weight="bold", color=ACCENT, style=ft.TextStyle(letter_spacing=1.5)),
                        ft.Text("BREWTRACK", size=22, weight="bold", color=TEXT_PRIMARY, font_family=FONT_HEADING),
                    ]
                ),
                ft.Divider(height=30, color=CARD_BORDER),
                
                ft.Column(
                    expand=True,
                    spacing=2,
                    scroll="hidden",
                    controls=[
                        _sidebar_section_title("Overview"),
                        _sidebar_link("Dashboard"),
                        
                        _sidebar_section_title("Master Records"),
                        _sidebar_link("User Management"),
                        _sidebar_link("Suppliers"),
                        _sidebar_link("Ingredients & Supplies"),
                        
                        _sidebar_section_title("Operations"),
                        _sidebar_link("Inventory Monitoring"),
                        _sidebar_link("Low-Stock Items"),
                        _sidebar_link("Purchase Orders"),
                        _sidebar_link("Movement History"),
                        
                        _sidebar_section_title("Transactions"),
                        _sidebar_link("Receiving/ Stock-In"),
                        _sidebar_link("Stock-Out/ Usage"),
                        _sidebar_link("Daily Sales"),
                        
                        _sidebar_section_title("Insights"),
                        _sidebar_link("Reports"),
                    ]
                ),
                
                ft.Divider(height=20, color=CARD_BORDER),
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Row(
                            spacing=12,
                            controls=[
                                ft.CircleAvatar(
                                    bgcolor=TEXT_PRIMARY,
                                    color=PANEL_LEFT_BG,
                                    radius=18,
                                    content=ft.Icon(ft.Icons.PERSON, size=20)
                                ),
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text(user_name, size=13, weight="bold", color=TEXT_PRIMARY),
                                        ft.Text(user_role, size=11, color=TEXT_MUTED),
                                    ]
                                )
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT, 
                            icon_color=ACCENT, 
                            icon_size=20, 
                            tooltip="Log Out",
                            on_click=lambda e: show_login() if show_login else None
                        )
                    ]
                )
            ]
        )

    data_table = ft.DataTable(
        expand=True,
        bgcolor=ft.Colors.TRANSPARENT,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        heading_row_color="#1A1A1A",
        heading_row_height=50,
        data_row_min_height=60,
        data_row_max_height=60,
        column_spacing=30,
        columns=[
            ft.DataColumn(ft.Text("Name", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Username", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Email", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Role", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Status", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Actions", size=15, weight="bold", color=TEXT_PRIMARY)),
        ],
        rows=[]
    )

    def load_data():
        users = user_model.get_users()
        data_table.rows.clear()
        
        for u in users:
            role_bg = "#332400" if "Admin" in u["role"] else "#002b2b"
            role_fg = ACCENT if "Admin" in u["role"] else "#00BCD4"
            status_bg = "#0A290A" if u["status"] == "Active" else "#330000"
            status_fg = "#4CAF50" if u["status"] == "Active" else "#F44336"
            
            data_table.rows.append(
                ft.DataRow(cells=[
                    _cell(u["full_name"], is_bold=True),
                    _cell(u["username"]),
                    _cell(u["email"]),
                    ft.DataCell(_badge(u["role"], role_bg, role_fg)),
                    ft.DataCell(_badge(u["status"], status_bg, status_fg)),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE, 
                            icon_color="#F44336",
                            tooltip="Delete User",
                            on_click=lambda e, uid=u["user_id"]: handle_delete_user(uid)
                        )
                    )
                ])
            )
        page.update()

    def handle_delete_user(uid):
        user_model.delete_user(uid)
        snack = ft.SnackBar(content=ft.Text("User deleted successfully!"), bgcolor=ft.Colors.RED_800)
        page.overlay.append(snack)
        snack.open = True
        load_data()

    def dialog_field(hint="", is_password=False):
        return ft.TextField(
            hint_text=hint,
            password=is_password,
            can_reveal_password=is_password,
            bgcolor=INPUT_BG,
            border_color=INPUT_BORDER,
            focused_border_color=ACCENT,
            color=TEXT_PRIMARY,
            hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
            text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            height=40,
        )

    full_name_field = dialog_field("e.g. Dana Whitfield")
    username_field = dialog_field("e.g. danaw")
    password_field = dialog_field("••••••••", is_password=True)
    email_field = dialog_field("name@brewtrack.com")
    contact_field = dialog_field("e.g. 09123456789")
    
    role_dropdown = ft.Dropdown(
        hint_text="Select a role",
        options=[
            ft.dropdown.Option("Staff"),
            ft.dropdown.Option("Owner/ Admin"),
        ],
        bgcolor=INPUT_BG,
        border_color=INPUT_BORDER,
        focused_border_color=ACCENT,
        color=TEXT_PRIMARY,
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
        border_radius=8,
        height=45,
    )

    def close_dialog(e=None):
        add_user_dialog.open = False
        page.update()

    def create_user(e=None):
        if not full_name_field.value or not username_field.value or not password_field.value or not role_dropdown.value:
            snack = ft.SnackBar(content=ft.Text("Please fill out all required fields."), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return
            
        try:
            user_model.add_user(
                full_name=full_name_field.value,
                email=email_field.value,
                username=username_field.value,
                password=password_field.value,
                role=role_dropdown.value,
                contact_number=contact_field.value
            )
            
            # Clear fields
            full_name_field.value = ""
            username_field.value = ""
            password_field.value = ""
            email_field.value = ""
            contact_field.value = ""
            role_dropdown.value = None
            
            snack = ft.SnackBar(content=ft.Text("User created successfully!"), bgcolor=ft.Colors.GREEN_800)
            page.overlay.append(snack)
            snack.open = True
            
            close_dialog()
            load_data()
            
        except Exception as ex:
            snack = ft.SnackBar(content=ft.Text(f"Error creating user: {str(ex)}"), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    add_user_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=PANEL_RIGHT_BG,
        shape=ft.RoundedRectangleBorder(radius=10),
        title=ft.Column(
            spacing=4,
            controls=[
                ft.Text("Add User", size=24, color=TEXT_PRIMARY, weight="bold"),
                ft.Text("Create a new staff or admin account.", size=12, color=TEXT_MUTED),
            ]
        ),
        content=ft.Container(
            width=500,
            content=ft.Column(
                spacing=15,
                tight=True,
                controls=[
                    ft.Column(spacing=4, controls=[ft.Text("Full Name *", size=12, weight="bold", color=TEXT_PRIMARY), full_name_field]),
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Column(expand=1, spacing=4, controls=[ft.Text("Username *", size=12, weight="bold", color=TEXT_PRIMARY), username_field]),
                            ft.Column(expand=1, spacing=4, controls=[ft.Text("Password *", size=12, weight="bold", color=TEXT_PRIMARY), password_field]),
                        ]
                    ),
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Column(expand=1, spacing=4, controls=[ft.Text("Email", size=12, weight="bold", color=TEXT_PRIMARY), email_field]),
                            ft.Column(expand=1, spacing=4, controls=[ft.Text("Contact Number", size=12, weight="bold", color=TEXT_PRIMARY), contact_field]),
                        ]
                    ),
                    ft.Column(spacing=4, controls=[ft.Text("Role *", size=12, weight="bold", color=TEXT_PRIMARY), role_dropdown]),
                ]
            )
        ),
        actions=[
            ft.TextButton("Cancel", style=ft.ButtonStyle(color=TEXT_MUTED), on_click=close_dialog),
            ft.Container(
                bgcolor=ACCENT,
                padding=ft.Padding.symmetric(horizontal=20, vertical=10),
                border_radius=8,
                ink=True,
                on_click=create_user,
                content=ft.Text("Create User", size=13, weight="bold", color=PANEL_LEFT_BG)
            )
        ]
    )

    def open_add_user_dialog(e=None):
        if add_user_dialog not in page.overlay:
            page.overlay.append(add_user_dialog)
        add_user_dialog.open = True
        page.update()

    main_content.content = ft.Column(
        expand=True,
        scroll="auto",
        spacing=30,
        controls=[
            ft.Row(
                alignment="spaceBetween",
                vertical_alignment="start",
                controls=[
                    ft.Column(
                        spacing=4,
                        controls=[
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Icon(ft.Icons.PEOPLE_ALT, size=20, color=TEXT_MUTED),
                                    ft.Text("User Management", size=14, color=TEXT_MUTED, weight="bold")
                                ]
                            ),
                            ft.Container(height=10),
                            ft.Text("User Management", size=28, weight="bold", color=TEXT_PRIMARY),
                            ft.Text("Manage staff and admin accounts and their access levels.", size=12, color=TEXT_MUTED),
                        ]
                    ),
                    ft.Container(
                        bgcolor=ACCENT,
                        border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                        ink=True,
                        on_click=open_add_user_dialog,
                        content=ft.Text("+ Add User", size=13, weight="bold", color=PANEL_LEFT_BG)
                    )
                ]
            ),
            
            ft.TextField(
                hint_text="Search users by name or email",
                hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                prefix_icon=ft.Icons.SEARCH,
                bgcolor=INPUT_BG,
                border_color=ft.Colors.TRANSPARENT,
                border_radius=8,
                content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                height=40,
                width=350,
            ),
            
            ft.Container(
                expand=True,
                content=ft.Column(scroll="auto", controls=[data_table])
            )
        ]
    )

    sidebar_container.content = build_sidebar("User Management")
    
    # Load initial data from database
    load_data()

    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        content=ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar_container,
                main_content,
            ]
        )
    )