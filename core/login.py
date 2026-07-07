import flet as ft
from core.theme import *
from models import user_model


def login_view(page: ft.Page, on_login_success):
    """
    on_login_success: callback(user_dict) -> called by main.py once
    credentials are verified against the database. login.py never imports
    dashboard.py directly - that keeps navigation decisions in one place (main.py).
    """
    username = ft.TextField(
        label="Username", width=320, color=TEXT_PRIMARY,
        border_color=BORDER_COLOR, cursor_color=TEXT_PRIMARY,
    )
    password = ft.TextField(
        label="Password", width=320, password=True, can_reveal_password=True,
        color=TEXT_PRIMARY, border_color=BORDER_COLOR, cursor_color=TEXT_PRIMARY,
    )
    error_text = ft.Text("", color=STATUS_RED, size=12)

    def do_login(e):
        if not username.value or not password.value:
            error_text.value = "Please enter your username and password."
            page.update()
            return
        try:
            user = user_model.authenticate(username.value.strip(), password.value)
        except Exception as ex:
            error_text.value = f"Database error: {ex}"
            page.update()
            return

        if user:
            on_login_success(user)
        else:
            error_text.value = "Invalid username or password."
            page.update()

    password.on_submit = do_login

    form = ft.Column(
        [
            ft.Text("BrewTrack", size=28, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Text("Sign in to manage your brewery", size=13, color=TEXT_SECONDARY),
            ft.Container(height=20),
            username,
            password,
            error_text,
            ft.Container(height=10),
            ft.ElevatedButton(
                "Sign In",
                width=320,
                height=45,
                bgcolor=ACCENT_GOLD,
                color="#000000",
                on_click=do_login,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    placeholder = ft.Container(
        content=form,
        bgcolor=BG_COLOR,
        alignment=ft.Alignment.CENTER,
        expand=True,
    )

    return ft.Row(
        [placeholder],
        expand=True,
        spacing=0,
    )