import flet as ft
from core.theme import *

def login_view(page: ft.Page):
    return ft.Container(
        content=ft.Text("Login Page (placeholder)", color=TEXT_PRIMARY, size=20),
        bgcolor=BG_COLOR,
        expand=True,
    )