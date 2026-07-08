import flet as ft
from core.theme import *
from core.components import _po_summary_card_small, _po_list_item
from models import purchase_order_model

def format_date(d):
    if not d: 
        return "N/A"
    try:
        return d.strftime("%b %d, %Y")
    except AttributeError:
        return str(d)[:10]

def AdminPurchaseOrders(page: ft.Page, open_new_po_modal):
    # Fetch real POs from the DB
    all_pos = purchase_order_model.get_purchase_orders()
    
    # Calculate Summary metrics
    open_count = sum(1 for po in all_pos if po['po_status'] in ['Pending', 'Approved'])
    pending_count = sum(1 for po in all_pos if po['po_status'] == 'Pending')
    approved_count = sum(1 for po in all_pos if po['po_status'] == 'Approved')
    received_count = sum(1 for po in all_pos if po['po_status'] == 'Received')

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

    po_list_controls = []
    
    if not all_pos:
        po_list_controls.append(
            ft.Container(
                padding=40, 
                alignment=ft.Alignment.CENTER, 
                content=ft.Text("No Purchase Orders found. Create a new one to get started.", color=TEXT_MUTED)
            )
        )
    else:
        for po in all_pos:
            items = po.get('items', [])
            total_amount = sum(float(i['line_total']) for i in items)
            items_count = len(items)
            
            # Create chips summarizing the ordered items
            chips = []
            for i in items:
                # Eg: "Coffee Beans * 5 kg * P500.00"
                chips.append(f"{i['item_name']} * {float(i['ordered_quantity']):g} * P{float(i['unit_cost']):,.2f}")
                
            po_list_controls.append(
                _po_list_item(
                    po_num=f"PO-{po['po_id']:04d}",
                    status=po['po_status'],
                    supplier=po['supplier_name'] or "Unknown",
                    date_created=format_date(po['po_date']),
                    expected_date=format_date(po['expected_delivery_date']),
                    amount=f"P {total_amount:,.2f}",
                    items_count=str(items_count),
                    chips=chips
                )
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
                    _po_summary_card_small("Open Orders", str(open_count)),
                    _po_summary_card_small("Pending Approval", str(pending_count)),
                    _po_summary_card_small("Approved", str(approved_count)),
                    _po_summary_card_small("Received", str(received_count)),
                ]
            ),
            
            action_bar,
            
            # List of Purchase Orders
            ft.Column(
                spacing=15,
                controls=po_list_controls
            )
        ]
    )