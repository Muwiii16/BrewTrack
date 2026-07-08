import flet as ft
from core.theme import *
from models import user_model 

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
                ft.Icon(ft.Icons.COFFEE, size=40, color=ACCENT_GOLD),
                ft.Text(
                    "BUT FIRST, COFFEE",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=ACCENT_GOLD,
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

def login_view(page: ft.Page, on_login_success):
    """
    on_login_success: callback(user_dict) -> called by main.py once
    credentials are verified against the database.
    """

    email_field = ft.TextField(
        value="admin@brewtrack.com",
        hint_text="juandelacruz@gmail.com",
        hint_style=ft.TextStyle(color=TEXT_SECONDARY, size=13),
        bgcolor=INPUT_BG,
        border_color=INPUT_BORDER,
        focused_border_color=ACCENT_GOLD,
        border_radius=8,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
        height=44,
    )

    password_field = ft.TextField(
        value="admin",
        hint_text="••••••••",
        hint_style=ft.TextStyle(color=TEXT_SECONDARY, size=13),
        password=True,
        can_reveal_password=True,
        bgcolor=INPUT_BG,
        border_color=INPUT_BORDER,
        focused_border_color=ACCENT_GOLD,
        border_radius=8,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
        height=44,
    )

    error_text = ft.Text("", color=STATUS_RED, size=12)

    def do_login(e):
        if not email_field.value or not password_field.value:
            error_text.value = "Please enter your email and password."
            page.update()
            return
        try:
            user = user_model.authenticate(email_field.value.strip(), password_field.value)
        except Exception as ex:
            error_text.value = f"Database error: {ex}"
            page.update()
            return

        if user:
            on_login_success(user)
        else:
            error_text.value = "Invalid credentials."
            page.update()

    password_field.on_submit = do_login

    right_panel_content = ft.Container(
        expand=1,
        bgcolor=INPUT_BG,
        border_radius=ft.BorderRadius.only(top_right=16, bottom_right=16),
        alignment=ft.Alignment.CENTER,
        padding=40,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            width=320,  
            controls=[
                ft.Text("BrewTrack", size=28, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                ft.Text("Sign in to manage your brewery", size=13, color=TEXT_SECONDARY),
                ft.Container(height=20),
                email_field,
                password_field,
                error_text,
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Sign In",
                    width=320,
                    height=45,
                    bgcolor=ACCENT_GOLD,
                    color="#000000",
                    on_click=do_login,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ),
            ],
        ),
    )
    
    login_card = ft.Container(
        width=900,
        height=530,
        border_radius=16,
        border=ft.Border.all(1, BORDER_COLOR),
        content=ft.Row(
            spacing=0,
            expand=True,
            controls=[
                _left_panel(),
                right_panel_content
            ],
        ),
    )

    return ft.Container(
        expand=True,
        bgcolor=COFFEE_BG_COLOR,
        alignment=ft.Alignment.CENTER,
        content=login_card,
    )