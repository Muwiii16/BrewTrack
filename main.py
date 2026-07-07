import flet as ft
from core.theme import *
from core.login import login_view
from core.dashboard import dashboard_view


class BrewTrackApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "BrewTrack"
        self.page.bgcolor = BG_COLOR
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0

        self.page.window.maximized = True

        self.user = None  # holds the logged-in user's row (dict) once authenticated
 
        self.show_login()  # start with the dashboard view
 
    def show_login(self):
        self.user = None
        self.page.clean()
        self.page.add(login_view(self.page, on_login_success=self.show_dashboard))
 
    def show_dashboard(self, user):
        """Called by login_view once db.authenticate() succeeds."""
        self.user = user
        self.page.clean()
        self.page.add(dashboard_view(self.page, user, on_logout=self.show_login))
        
def main(page: ft.Page):
    BrewTrackApp(page)
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")