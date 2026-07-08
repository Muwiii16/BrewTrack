import flet as ft
from core.theme import *
from core.components import _summary_card, _badge, _cell
from models import inventory_model

def AdminLowStock(page: ft.Page, open_new_po_modal):
    # Fetch real data from the database
    low_stock_items = inventory_model.get_low_stock_items()
    
    needs_attention_count = len(low_stock_items)
    out_of_stock_count = sum(1 for item in low_stock_items if float(item['current_quantity']) <= 0)
    
    # Calculate estimated replenishment cost (assuming we order at least the reorder level to restock safely)
    replenishment_cost = 0.0
    for item in low_stock_items:
        curr_qty = float(item['current_quantity'])
        ro_level = float(item['reorder_level'])
        cost = float(item['cost_per_unit'])
        
        # Calculate how much to order to get back comfortably above the reorder line
        shortage = max(ro_level - curr_qty, 0)
        suggested_qty = max(shortage, ro_level) # Minimum order of reorder_level
        replenishment_cost += suggested_qty * cost

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

    table_rows = []
    for item in low_stock_items:
        curr_qty = float(item['current_quantity'])
        ro_level = float(item['reorder_level'])
        uom = item['unit_of_measurement']
        supplier_name = item['supplier_name'] if item['supplier_name'] else "Unassigned"
        
        # Suggest quantity logic
        shortage = max(ro_level - curr_qty, 0)
        suggested_qty = max(shortage, ro_level)
        
        is_out = (curr_qty <= 0)
        status_text = "Out of Stock" if is_out else "Low"
        status_bg = "#330000" if is_out else "#332400"
        status_fg = "#F44336" if is_out else ACCENT

        table_rows.append(ft.DataRow(cells=[
            _cell(item['item_name'], True),
            _cell(supplier_name),
            _cell(f"{curr_qty:g} {uom}"),
            _cell(f"{ro_level:g} {uom}"),
            _cell(f"{suggested_qty:g} {uom}"),
            ft.DataCell(_badge(status_text, status_bg, status_fg))
        ]))

    table = ft.DataTable(
        expand=True,
        bgcolor=ft.Colors.TRANSPARENT,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        heading_row_color="#1A1A1A",
        heading_row_height=50,
        data_row_min_height=60,
        data_row_max_height=60,
        column_spacing=40,
        columns=[
            ft.DataColumn(ft.Text("Item", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Supplier", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("On Hand", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Reorder At", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Suggested Qty.", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Status", size=15, weight="bold", color=TEXT_PRIMARY)),
        ],
        rows=table_rows
    )
    
    # Handle empty state
    if not table_rows:
        table_container = ft.Container(
            padding=40,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("All inventory levels are healthy! No low stock alerts.", color=TEXT_MUTED)
        )
    else:
        table_container = table

    return ft.Column(
        expand=True,
        scroll="auto",
        spacing=30,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=20, color=TEXT_MUTED),
                            ft.Text("Low-Stock Items", size=14, color=TEXT_MUTED, weight="bold")
                        ]
                    ),
                    ft.Container(height=10),
                    ft.Text("Low-Stock Items", size=28, weight="bold", color=TEXT_PRIMARY),
                    ft.Text("Items at or below their reorder level. Replenish these to avoid production stoppages", size=12, color=TEXT_MUTED),
                ]
            ),
            ft.Row(
                spacing=20,
                controls=[
                    _summary_card("Items Needing Attention", str(needs_attention_count)),
                    _summary_card("Out of Stock", str(out_of_stock_count)),
                    _summary_card("Estimated Replenishment Cost", f"P {replenishment_cost:,.2f}"),
                ]
            ),
            action_bar,
            ft.Container(
                expand=True,
                content=ft.Column(
                    scroll="auto",
                    controls=[table_container]
                )
            )
        ]
    )