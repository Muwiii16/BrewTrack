import flet as ft
from core.theme import *
from core.components import _summary_card, _panel_container, _low_stock_row, _movement_row, _po_card

def AdminOverview(page: ft.Page):
    return ft.Column(
        expand=True,
        scroll="auto",
        spacing=30,
        controls=[
            # Header
            ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.DASHBOARD_ROUNDED, size=20, color=TEXT_MUTED),
                            ft.Text("Dashboard", size=14, color=TEXT_MUTED, weight="bold")
                        ]
                    ),
                    ft.Container(height=10),
                    ft.Text("Good day, Juan", size=28, weight="bold", color=TEXT_PRIMARY),
                    ft.Text("Here is the current state of your brewery inventory and procurement", size=12, color=TEXT_MUTED),
                ]
            ),
            
            # Summary Cards
            ft.Row(
                spacing=20,
                controls=[
                    _summary_card("Inventory Value", "P5,691", "14 tracked items"),
                    _summary_card("Low/ Out of Stock", "7", "Needs attention"),
                    _summary_card("Pending Approval", "1", "2 open orders"),
                    _summary_card("Sales Today", "$0", "$2,367 recent total"),
                ]
            ),
            
            # Middle Section (Split Panels)
            ft.Row(
                expand=True,
                spacing=20,
                vertical_alignment="start",
                controls=[
                    _panel_container(
                        "Low-Stock Alerts",
                        [
                            _low_stock_row("Coffee Bean", "145 kg on hand * reorder at 150"),
                            _low_stock_row("Matcha Powder", "120 g on hand * reorder at 150"),
                            _low_stock_row("Oatmilk", "1 L on hand * reorder at 3"),
                            _low_stock_row("Vanilla Syrup", "2 L on hand * reorder at 5"),
                        ]
                    ),
                    _panel_container(
                        "Recent Stock Movements",
                        [
                            _movement_row("Stock-In", "#0A290A", "#4CAF50", "Coffee Bean * PO...", "Marco Reyes | Jun 30, 12:22 AM", "+1000 units", "#4CAF50"),
                            _movement_row("Stock-Out", "#330000", "#F44336", "Matcha Powder * Ba...", "Marco Reyes | Jul 12, 12:22 AM", "- 220 g", "#FF9800"),
                            _movement_row("Sale", "#002b2b", "#00BCD4", "Oatmilk * Restock from...", "Jose Santos | Aug 14, 12:22 AM", "- 3 cases", "#FF9800"),
                            _movement_row("Stock-Out", "#330000", "#F44336", "Vanilla Syrup * Restock...", "Kim Chua | Sep 1, 12:22 AM", "+ 6 bottles", "#4CAF50"),
                        ]
                    ),
                ]
            ),
            
            # Footer Section (Purchase Orders)
            ft.Container(
                border=ft.Border.all(1, CARD_BORDER),
                border_radius=8,
                padding=20,
                content=ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text("Purchase", size=18, weight="bold", color=TEXT_PRIMARY),
                                ft.Text("Orders", size=18, weight="bold", color=TEXT_PRIMARY),
                            ]
                        ),
                        ft.Row(
                            spacing=15,
                            controls=[
                                _po_card("PO- 1008", "P 1,548.00", "Pending"),
                                _po_card("PO- 1009", "P 612.00", "Pending"),
                                _po_card("PO- 1010", "P 2,500.00", "Approved"),
                            ]
                        ),
                        ft.Row(
                            spacing=4,
                            controls=[
                                ft.Text("View all", size=11, color=TEXT_MUTED),
                                ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=TEXT_MUTED)
                            ]
                        )
                    ]
                )
            )
        ]
    )