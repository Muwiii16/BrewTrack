import flet as ft
from core.theme import *
from core.login import login_view
from core.admin_overview import dashboard_view

def main(page: ft.Page):
    page.title = "BrewTrack"
    page.bgcolor = BG_COLOR
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    try:
        page.window.maximized = True
    except AttributeError:
        pass

    # --- Routing Logic ---
    def route_change(e):
        page.views.clear()
        
        # Default route (Login)
        page.views.append(
            ft.View(
                route="/",
                controls=[login_view(page)],
                bgcolor=BG_COLOR,
                padding=0
            )
        )
        
        # Dashboard route
        if page.route == "/dashboard":
            page.views.append(
                ft.View(
                    route="/dashboard",
                    controls=[dashboard_view(page)],
                    bgcolor=BG_COLOR,
                    padding=0
                )
            )
            
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.route = top_view.route
        page.update()

    # Attach routing events to the page
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Force the initial route load
    page.route = "/"
    route_change(None)

ft.run(main, assets_dir='assets')