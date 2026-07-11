import flet as ft
from core.theme import *
from core.login import login_view
from core.dashboard import dashboard_view

# --- TEMPORARILY COMMENTED OUT PENDING VIEWS ---
# from core.inventory_monitoring import inventory_monitoring_view
# from core.stock_movement import movement_history_view
# from core.ingredients_supply import ingredients_supply_view
# from core.supplier_management import supplier_management_view
from core.user_management import user_management_view
from core.supplier_management import supplier_management_view
from core.ingredients_supply import ingredients_supply_view
from core.daily_sales import DailySales


class BrewTrackApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "BrewTrack"
        self.page.bgcolor = BG_COLOR
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.window.maximized = True
        #self.page.window.full_screen = True

        self.user = None  # holds the logged-in user's row (dict) once authenticated
 
        self.show_login()  # start with the login view
 
    def show_login(self):
        self.user = None
        self.page.clean()
        self.page.add(login_view(self.page, on_login_success=self.show_dashboard))
 
    def show_dashboard(self, user):
        """Called by login_view once db.authenticate() succeeds."""
        self.user = user
        self.page.clean()
        self.navigate_to("Dashboard")
        
    def navigate_to(self, page_name):
        """The central router. Clears the screen and loads the requested page."""
        self.page.clean()

        if page_name in ["Dashboard", "Purchase Orders", "Reports"]:
            if self.user["role"] == "Staff":
                    from core.staff_dashboard import staff_dashboard_view
                    self.page.add(staff_dashboard_view(self.page, self.user, self.show_login, self.navigate_to))
            else:
                from core.dashboard import dashboard_view
                self.page.add(dashboard_view(self.page, self.user, self.show_login, self.navigate_to, initial_view="Dashboard"))
        elif page_name == "User Management":
            self.page.add(user_management_view(self.page, self.user, self.show_login, self.navigate_to))
            
        elif page_name == "Suppliers":
             self.page.add(supplier_management_view(self.page, self.user, self.show_login, self.navigate_to))
             
        elif page_name == "Ingredients & Supplies":
             self.page.add(ingredients_supply_view(self.page, self.user, self.show_login, self.navigate_to))
             
            
        elif page_name == "Inventory Monitoring":
            if self.user["role"] == "Staff":
                from core.staff_inventory_monitoring import staff_inventory_monitoring_view
                self.page.add(staff_inventory_monitoring_view(self.page, self.user, self.show_login, self.navigate_to))
            else:
                from core.inventory_monitoring import inventory_monitoring_view
                self.page.add(inventory_monitoring_view(self.page, self.user, self.show_login, self.navigate_to))
        elif page_name in ["Low-Stock Alerts", "Low-Stock Items"]:
                if self.user["role"] == "Staff":
                    from core.staff_low_stock import staff_low_stock_alerts_view
                    self.page.add(staff_low_stock_alerts_view(self.page, self.user, self.show_login, self.navigate_to))
                else:
                    from core.dashboard import dashboard_view
                    self.page.add(dashboard_view(self.page, self.user, self.show_login, self.navigate_to, initial_view="AdminLowStock"))
                    
        elif page_name == "Movement History":
            if self.user["role"] == "Staff":
                from core.staff_movement_history import staff_movement_history_view
                self.page.add(staff_movement_history_view(self.page, self.user, self.show_login, self.navigate_to))
            else:
                from core.movement_history import movement_history_view
                self.page.add(movement_history_view(self.page, self.user, self.show_login, self.navigate_to))
        
        elif page_name == "Receiving/ Stock-In":
            if self.user["role"] == "Staff":
                from core.staff_receiving import staff_receiving_view
                self.page.add(staff_receiving_view(self.page, self.user, self.show_login, self.navigate_to))
            else:
                from core.receiving_stock_in import receiving_stock_in_view
                self.page.add(receiving_stock_in_view(self.page, self.user, self.show_login, self.navigate_to))
                
        elif page_name == "Stock-Out/ Usage":
            if self.user["role"] == "Staff":
                from core.staff_stock_out import staff_stock_out_usage_view
                self.page.add(staff_stock_out_usage_view(self.page, self.user, self.show_login, self.navigate_to))
            else:
                from core.stock_out_usage import stock_out_usage_view
                self.page.add(stock_out_usage_view(self.page, self.user, self.show_login, self.navigate_to))

        
        # --- TEMPORARILY COMMENTED OUT PENDING ROUTES ---
        
        elif page_name == "Daily Sales":
            if self.user["role"] == "Staff" :
                from core.staff_daily_sales import staff_daily_sales_view
                self.page.add(staff_daily_sales_view(self.page, self.user, self.show_login, self.navigate_to))
            else:
                from core.daily_sales import DailySales
                self.page.add(DailySales(self.page, self.user, self.show_login, self.navigate_to))
        
        self.page.update()
        
def main(page: ft.Page):
    BrewTrackApp(page)
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")