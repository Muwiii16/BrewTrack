import flet as ft

from core.theme import *
from core.login import login_view
from core.dashboard import dashboard_view
from core.staff_dashboard import staff_dashboard_view
from core.inventory_monitoring import inventory_monitoring_view
from core.low_stock_alerts import low_stock_alerts_view
from core.receiving_stock_in import receiving_stock_in_view
from core.stock_out_usage import stock_out_usage_view
from core.daily_sales import daily_sales_view
from core.staff_receiving import staff_receiving_view


class BrewTrackApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "BrewTrack"
        self.page.bgcolor = BG_COLOR
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0

        self.page.window.maximized = True

        self.user = None  # holds the logged-in user's dict once authenticated

        self.show_login()  # start at the login screen

    def show_login(self):
        self.user = None
        self.page.clean()
        self.page.add(login_view(
            self.page, on_login_success=self.show_dashboard))

    def show_dashboard(self, user):
        """Called by login_view once login succeeds (real or fake)."""
        self.user = user
        self.page.clean()
        if user["role"].lower() == "staff":
            self.navigate_to("Staff Dashboard")
        else:
            self.navigate_to("Dashboard")

    def navigate_to(self, page_name):
        """The central router. Clears the screen and loads the requested page."""
        self.page.clean()

        if page_name == "Dashboard":
            self.page.add(dashboard_view(self.page, self.user,
                          self.show_login, self.navigate_to))

        elif page_name == "Staff Dashboard":
            self.page.add(staff_dashboard_view(self.page, self.user,
                          self.show_login, self.navigate_to))

        elif page_name == "Inventory Monitoring":
            self.page.add(inventory_monitoring_view(self.page, self.user,
                          self.show_login, self.navigate_to))

        elif page_name == "Low-Stock Alerts":
            self.page.add(low_stock_alerts_view(self.page, self.user,
                          self.show_login, self.navigate_to))

        elif page_name == "Receiving/Stock-In":
            if self.user and self.user["role"].lower() == "staff":
                self.page.add(receiving_stock_in_view(self.page, self.user,
                                                      self.show_login, self.navigate_to))
            else:
                self.page.add(staff_receiving_view(self.page, self.user,
                                                   self.show_login, self.navigate_to))

        elif page_name == "Stock-Out/Usage":
            self.page.add(stock_out_usage_view(self.page, self.user,
                                               self.show_login, self.navigate_to))

        elif page_name == "Daily Sales":
            self.page.add(daily_sales_view(self.page, self.user,
                                           self.show_login, self.navigate_to))

        self.page.update()


def main(page: ft.Page):
    BrewTrackApp(page)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
