import flet as ft
from core.theme import *

def staff_dashboard_view(page: ft.Page):
    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Icon(ft.Icons.PERSON_OUTLINE, size=50, color=ACCENT),
                ft.Text("Staff Dashboard", size=28, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Text("Welcome back! Your daily tasks and POS will go here.", size=14, color=TEXT_MUTED),
            ]
        )
    )