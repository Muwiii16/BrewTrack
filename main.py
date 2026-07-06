import flet as ft
from core.theme import *
from core.login import login_view
from core.dashboard import dashboard_view


def main(page: ft.Page):
    page.title = "BrewTrack"
    page.bgcolor = BG_COLOR
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    page.window.maximized = True

    page.add(dashboard_view(page))


ft.app(target=main, assets_dir='assets')
