import flet as ft
from core.theme import *
from core.login import login_view
from core.dashboard import dashboard_view
from core.user_management import user_management_view  # <-- Import the new view

def main(page: ft.Page):
    page.title = "BrewTrack"
    page.bgcolor = BG_COLOR
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    page.window.maximized = True

    # Swap dashboard_view(page) out to load the new User Management system UI 
    page.app(user_management_view(page))

ft.run(main, assets_dir='assets')