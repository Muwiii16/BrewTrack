import flet as ft
from core.theme import *


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


def _right_panel(page: ft.Page):
    # Pre-filled with Admin credentials for easy testing!
    email_field = ft.TextField(
        value="admin@brewtrack.com",
        hint_text="juandelacruz@gmail.com",
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
        value="admin_password123",
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

    def sign_up_clicked(e):
        # 1. Clear the login UI from the screen completely
        page.controls.clear()
        
        # 2. Check the email to determine which dashboard to show (Admin vs Staff)
        if email_field.value == "admin@brewtrack.com":
            from core.dashboard import dashboard_view
            page.add(dashboard_view(page))
        else:
            from core.staff_dashboard import staff_dashboard_view
            page.add(staff_dashboard_view(page))
            
        # 3. Tell Flet to redraw the window
        page.update()

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
                    "Create Account",
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
                    "or use your email for registration",
                    size=12,
                    color=TEXT_MUTED,
                ),
                ft.Container(height=10),
                ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("Email", size=12, weight=ft.FontWeight.W_600, color=TEXT_LABEL),
                        email_field,
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
                    on_click=sign_up_clicked,
                    content=ft.Text(
                        "Sign Up",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY,
                    ),
                ),
            ],
        ),
    )


def login_view(page: ft.Page):
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
                _right_panel(page),
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
                ft.Text("Log In Page", size=14, color=TEXT_MUTED),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    content=card,
                ),
            ],
        ),
    )