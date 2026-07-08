import flet as ft
from core.theme import *
from models import user_model


def _fake_login(role, on_login_success):
    """TEMP: bypasses real authentication for now"""
    fake_user = {
        "full_name": "Marco Reyes" if role == "staff" else "Juan Dela Cruz",
        "role": "Staff" if role == "staff" else "Owner/Admin",
    }
    on_login_success(fake_user)


def login_view(page: ft.Page, on_login_success):
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
            user = user_model.authenticate(
                username.value.strip(), password.value)
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
            ft.Text("BrewTrack", size=28, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text("Sign in to manage your brewery",
                    size=13, color=TEXT_SECONDARY),
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
            ft.Container(height=20),
            ft.Text("— Temporary testing shortcuts —",
                    size=11, color=TEXT_SECONDARY),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Enter as Staff",
                        width=150,
                        bgcolor=CARD_COLOR,
                        color=TEXT_PRIMARY,
                        on_click=lambda e: _fake_login(
                            "staff", on_login_success),
                    ),
                    ft.ElevatedButton(
                        "Enter as Admin",
                        width=150,
                        bgcolor=CARD_COLOR,
                        color=TEXT_PRIMARY,
                        on_click=lambda e: _fake_login(
                            "admin", on_login_success),
                    ),
                ],
                spacing=10,
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
