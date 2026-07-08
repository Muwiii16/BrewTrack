import flet as ft
from core.theme import *
from models import user_model

def _social_button(icon: str):
    return ft.Container(
        width=40,
        height=40,
        border_radius=20,
        bgcolor=SOCIAL_BG,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(icon, size=18, color=TEXT_PRIMARY),
        ink=True,
        on_click=lambda e: None,
    )

def _left_panel():
    return ft.Container(
        expand=1,
        bgcolor=PANEL_LEFT_BG,
        border_radius=ft.BorderRadius.only(top_left=16, bottom_left=16),
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.COFFEE, size=40, color=ACCENT),
                ft.Text(
                    "BUT FIRST, COFFEE",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=ACCENT,
                    style=ft.TextStyle(letter_spacing=2),
                ),
                ft.Text(
                    "BREWTRACK",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                    font_family=FONT_HEADING,
                ),
            ],
        ),
    )

def _right_panel(page: ft.Page, on_login_success=None):
    # Field to accept both username and email
    identifier_field = ft.TextField(
        hint_text="Email or Username",
        hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
        bgcolor=INPUT_BG,
        border_color=INPUT_BORDER,
        focused_border_color=ACCENT,
        border_radius=8,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
        height=44,
    )

    password_field = ft.TextField(
        hint_text="••••••••",
        hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
        password=True,
        can_reveal_password=True,
        bgcolor=INPUT_BG,
        border_color=INPUT_BORDER,
        focused_border_color=ACCENT,
        border_radius=8,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
        height=44,
    )

    def show_error(message):
        snack = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE), 
            bgcolor=ft.Colors.RED_800
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def login_clicked(e):
        identifier = identifier_field.value.strip()
        password = password_field.value.strip()

        if not identifier or not password:
            show_error("Please enter both email/username and password.")
            return

        # Authenticate via the DB model
        user = user_model.authenticate(identifier, password)
        
        if user:
            # Show friendly welcome message
            snack = ft.SnackBar(
                content=ft.Text(f"Welcome back, {user['full_name']}!", color=ft.Colors.WHITE), 
                bgcolor=ft.Colors.GREEN_800
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
            
            # Pass user back up to the app router (main.py)
            if on_login_success:
                on_login_success(user)
        else:
            show_error("Invalid credentials or inactive account.")
            password_field.value = ""
            page.update()

    # Allow Enter key to trigger login
    identifier_field.on_submit = login_clicked
    password_field.on_submit = login_clicked

    return ft.Container(
        expand=1,
        bgcolor=PANEL_RIGHT_BG,
        border_radius=ft.BorderRadius.only(top_right=16, bottom_right=16),
        padding=ft.Padding.symmetric(horizontal=50, vertical=40),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Text(
                    "Welcome Back",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        _social_button(ft.Icons.FACEBOOK),
                        _social_button(ft.Icons.G_MOBILEDATA),
                        _social_button(ft.Icons.SEND_ROUNDED),
                    ],
                ),
                ft.Text(
                    "or log in with your account credentials",
                    size=12,
                    color=TEXT_MUTED,
                ),
                ft.Container(height=10),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Email / Username", size=12, weight=ft.FontWeight.W_600, color=TEXT_LABEL),
                        identifier_field,
                    ],
                ),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Password", size=12, weight=ft.FontWeight.W_600, color=TEXT_LABEL),
                        password_field,
                    ],
                ),
                ft.Container(height=10),
                ft.Container(
                    width=180,
                    height=42,
                    border_radius=21,
                    bgcolor=ACCENT_DARK,
                    alignment=ft.Alignment.CENTER,
                    ink=True,
                    on_click=login_clicked,
                    content=ft.Text(
                        "Sign In",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                ),
            ],
        ),
    )

def login_view(page: ft.Page, on_login_success=None):
    card = ft.Container(
        width=720,
        height=430,
        border_radius=16,
        border=ft.Border.all(1, CARD_BORDER),
        content=ft.Row(
            spacing=0,
            expand=True,
            controls=[
                _left_panel(),
                _right_panel(page, on_login_success),
            ],
        ),
    )

    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        padding=20,
        content=ft.Column(
            expand=True,
            spacing=20,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=card,
                ),
            ],
        ),
    )