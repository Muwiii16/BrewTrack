import flet as ft
from core.theme import *
from core.components import _po_summary_card_small, _po_list_item

def AdminPurchaseOrders(page: ft.Page, open_new_po_modal):
    action_bar = ft.Row(
        alignment="spaceBetween",
        controls=[
            ft.TextField(
                hint_text="Search",
                hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                prefix_icon=ft.Icons.SEARCH,
                bgcolor=INPUT_BG,
                border_color=ft.Colors.TRANSPARENT,
                border_radius=8,
                content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                height=40,
                width=300,
            ),
            ft.Container(
                bgcolor=ACCENT,
                border_radius=8,
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                ink=True,
                on_click=open_new_po_modal,
                content=ft.Text(
                    "New Purchase Order",
                    size=13,
                    weight="bold",
                    color=PANEL_LEFT_BG, 
                )
            )
        ]
    )

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
                            ft.Icon(ft.Icons.RECEIPT_LONG, size=20, color=TEXT_MUTED),
                            ft.Text("Purchase Order", size=14, color=TEXT_MUTED, weight="bold")
                        ]
                    ),
                    ft.Container(height=10),
                    ft.Text("Purchase Order", size=28, weight="bold", color=TEXT_PRIMARY),
                    ft.Text("Raise and track orders to your suppliers", size=12, color=TEXT_MUTED),
                ]
            ),
            
            # Summary Cards
            ft.Row(
                spacing=20,
                controls=[
                    _po_summary_card_small("Open Orders", "2"),
                    _po_summary_card_small("Pending Approval", "1"),
                    _po_summary_card_small("Approved", "1"),
                    _po_summary_card_small("Received", "1"),
                ]
            ),
            
            action_bar,
            
            # List of Purchase Orders
            ft.Column(
                spacing=15,
                controls=[
                    _po_list_item(
                        po_num="PO- 1001", 
                        status="Pending", 
                        supplier="ABC Farms", 
                        date_created="Jul 3, 2026", 
                        expected_date="Jul 8, 2026", 
                        amount="P 800.00", 
                        items_count="2",
                        chips=["Arabica Coffee Beans * 5 kg * P500.00", "Black Coffee Beans * 5 kg * P300.00"]
                    ),
                    _po_list_item(
                        po_num="PO- 1002", 
                        status="Approved", 
                        supplier="ABC Farms", 
                        date_created="Jul 3, 2026", 
                        expected_date="Jul 8, 2026", 
                        amount="P 1,200.00", 
                        items_count="2",
                        chips=["Ceremonial Matcha Powder * 5 kg * P600.00", "Culinary Matcha Powder * 5 kg * P600.00"]
                    ),
                ]
            )
        ]
    )