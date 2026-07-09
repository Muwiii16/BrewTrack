import flet as ft
import csv
from datetime import datetime
from core.theme import *
from core.components import _summary_card, _cell, _badge
from models import inventory_model, purchase_order_model, sales_model, supplier_model, stock_movement_model

def AdminReports(page: ft.Page):
    # Track the active tab for exporting
    active_tab_ref = ["Inventory"]

    # --- 1. FETCH ALL DATA FROM MODELS ---
    inventory_data = inventory_model.get_inventory_overview()
    pending_pos = purchase_order_model.get_pending_orders_count()
    recent_sales = sales_model.get_recent_sales(limit=100) 
    po_history = purchase_order_model.get_purchase_orders()
    movements = stock_movement_model.get_recent_movements(limit=100)
    suppliers = supplier_model.get_suppliers()
    
    # --- 2. CALCULATE AGGREGATES ---
    total_inventory_value = sum(float(item['value'] or 0) for item in inventory_data)
    total_sales_revenue = sum(float(sale['line_total'] or 0) for sale in recent_sales)
    total_items_tracked = len(inventory_data)
    low_stock_count = sum(1 for item in inventory_data if float(item['current_quantity']) <= float(item['reorder_level']))

    # --- 3. EXPORT TO CSV LOGIC ---
    def export_clicked(e):
        try:
            filename = f"BrewTrack_{active_tab_ref[0].replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                # Write data based on the active tab
                if active_tab_ref[0] == "Inventory":
                    writer.writerow(["Item Name", "Stock Level", "UOM", "Unit Cost", "Total Value", "Status"])
                    for item in inventory_data:
                        qty = float(item['current_quantity'])
                        reorder = float(item['reorder_level'])
                        status = "Low Stock" if qty <= reorder else "Healthy"
                        writer.writerow([
                            item['item_name'], f"{qty:g}", item['unit_of_measurement'], 
                            f"{float(item['cost_per_unit']):.2f}", f"{float(item['value'] or 0):.2f}", status
                        ])
                        
                elif active_tab_ref[0] == "Sales":
                    writer.writerow(["Date & Time", "Product Sold", "Qty", "Revenue", "Cashier"])
                    for sale in recent_sales:
                        writer.writerow([
                            sale['sales_date'].strftime("%Y-%m-%d %H:%M"), sale['product_name'], 
                            sale['quantity_sold'], f"{float(sale['line_total']):.2f}", sale['full_name']
                        ])
                        
                elif active_tab_ref[0] == "Movements":
                    writer.writerow(["Date", "Item", "Type", "Qty Changed", "Resulting Stock", "Reference"])
                    for mov in movements:
                        writer.writerow([
                            mov['movement_date'].strftime("%Y-%m-%d %H:%M"), mov['item_name'], 
                            mov['movement_type'], mov['quantity'], mov['resulting_stock'], mov['reference_type'] or "N/A"
                        ])
            
            snack = ft.SnackBar(content=ft.Text(f"Success! Report saved to your folder as {filename}"), bgcolor=ft.Colors.GREEN_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()
        except Exception as ex:
            snack = ft.SnackBar(content=ft.Text(f"Error saving file: {ex}"), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    # --- 4. TREND GRAPH GENERATION HELPER ---
    def _build_trend_graph(data_values, chart_color, max_val):
        if not data_values:
            return ft.Container(content=ft.Row([ft.Text("Not enough data to graph.", color=TEXT_MUTED)], alignment="center"), height=150)
            
        bars = []
        for val in data_values:
            # Calculate height dynamically. Ensure minimum of 5px so tiny values are still visible.
            bar_h = max(5, (val / max_val * 130)) if max_val > 0 else 5
            bars.append(
                ft.Container(
                    width=24,
                    height=bar_h,
                    bgcolor=chart_color,
                    border_radius=4,
                    tooltip=f"{val:g}" # Hover to see exact numerical value!
                )
            )
            
        return ft.Container(
            content=ft.Row(controls=bars, alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.END),
            height=150,
            padding=20,
            border=ft.Border(bottom=ft.BorderSide(1, CARD_BORDER))
        )

    # --- 5. BUILD HELPER TABLES & GRAPHS ---
    
    # Table A: Inventory & Low Stock
    inventory_rows, inv_vals = [], []
    for i, item in enumerate(inventory_data):
        qty = float(item['current_quantity'])
        inv_vals.append(qty)
        reorder = float(item['reorder_level'])
        status_cell = _badge("Low Stock", "#332400", ACCENT) if qty <= reorder else _badge("Healthy", "#0f2e16", "#22c55e")
        inventory_rows.append(ft.DataRow(cells=[_cell(item['item_name'], True), _cell(f"{qty:g} {item['unit_of_measurement']}"), _cell(f"P {float(item['cost_per_unit']):,.2f}"), _cell(f"P {float(item['value'] or 0):,.2f}", is_bold=True), ft.DataCell(status_cell)]))
        
    max_inv = max(inv_vals) if inv_vals else 0
    inv_chart = _build_trend_graph(inv_vals, ACCENT, max_inv)
    inventory_table = ft.DataTable(expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8, heading_row_color="#1A1A1A", columns=[ft.DataColumn(ft.Text(h, size=13, weight="bold", color=TEXT_MUTED)) for h in ["Item", "Stock Level", "Unit Cost", "Total Value", "Status"]], rows=inventory_rows)

    # Table B: Sales Activities
    sales_rows, sales_vals = [], []
    recent_20_sales = list(reversed(recent_sales[:20])) if recent_sales else []
    for sale in recent_20_sales:
        sales_vals.append(float(sale['line_total']))
        
    for sale in recent_sales:
        sales_rows.append(ft.DataRow(cells=[_cell(sale['sales_date'].strftime("%Y-%m-%d %H:%M")), _cell(sale['product_name'], True), _cell(str(sale['quantity_sold'])), _cell(f"P {float(sale['line_total']):,.2f}", is_bold=True, text_color=ACCENT), _cell(sale['full_name'])]))
        
    max_sale = max(sales_vals) if sales_vals else 0
    sales_chart = _build_trend_graph(sales_vals, "#4CAF50", max_sale)
    sales_table = ft.DataTable(expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8, heading_row_color="#1A1A1A", columns=[ft.DataColumn(ft.Text(h, size=13, weight="bold", color=TEXT_MUTED)) for h in ["Date & Time", "Product Sold", "Qty", "Revenue", "Cashier"]], rows=sales_rows)

    # Table C: Stock Movement History
    movement_rows, mov_vals = [], []
    recent_20_movs = list(reversed(movements[:20])) if movements else []
    for mov in recent_20_movs:
        mov_vals.append(float(mov['quantity']))
        
    for mov in movements:
        color = "#22c55e" if mov['movement_type'] == "Stock-In" else ACCENT
        movement_rows.append(ft.DataRow(cells=[_cell(mov['movement_date'].strftime("%Y-%m-%d %H:%M")), _cell(mov['item_name'], True), _cell(mov['movement_type'], text_color=color), _cell(str(float(mov['quantity']))), _cell(str(float(mov['resulting_stock']))), _cell(mov['reference_type'] or "N/A")]))
        
    max_mov = max(mov_vals) if mov_vals else 0
    mov_chart = _build_trend_graph(mov_vals, "#3b82f6", max_mov)
    movements_table = ft.DataTable(expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8, heading_row_color="#1A1A1A", columns=[ft.DataColumn(ft.Text(h, size=13, weight="bold", color=TEXT_MUTED)) for h in ["Date", "Item", "Type", "Qty Changed", "Resulting Stock", "Reference"]], rows=movement_rows)

    # --- 6. CUSTOM TAB SYSTEM ---
    tab_contents = {
        "Inventory": ft.Column(scroll="auto", controls=[ft.Text("Inventory Levels (All Items)", size=16, weight="bold", color=TEXT_PRIMARY), inv_chart, ft.Container(height=10), inventory_table]),
        "Sales": ft.Column(scroll="auto", controls=[ft.Text("Recent Sales Revenue Trend (Last 20)", size=16, weight="bold", color=TEXT_PRIMARY), sales_chart, ft.Container(height=10), sales_table]),
        "Movements": ft.Column(scroll="auto", controls=[ft.Text("Stock Movement Volume (Last 20)", size=16, weight="bold", color=TEXT_PRIMARY), mov_chart, ft.Container(height=10), movements_table])
    }
    
    active_content_container = ft.Container(expand=True, padding=20, content=tab_contents["Inventory"])

    def create_tab_button(title, icon_name, view_key, is_active=False):
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=20, vertical=10), border_radius=8, bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT,
            border=ft.Border.all(1, ACCENT if is_active else CARD_BORDER), ink=True, on_click=lambda e: switch_tab(view_key),
            content=ft.Row(spacing=8, controls=[ft.Icon(icon_name, size=16, color=ACCENT if is_active else TEXT_MUTED), ft.Text(title, size=13, weight="bold" if is_active else "normal", color=TEXT_PRIMARY if is_active else TEXT_MUTED)])
        )
        
    tab_buttons_row = ft.Row(spacing=15)
    def render_tab_buttons(active_key):
        tab_buttons_row.controls = [
            create_tab_button("Inventory & Valuation", ft.Icons.INVENTORY_2_OUTLINED, "Inventory", active_key == "Inventory"),
            create_tab_button("Sales Revenue", ft.Icons.POINT_OF_SALE_OUTLINED, "Sales", active_key == "Sales"),
            create_tab_button("Stock Movements", ft.Icons.SWAP_HORIZ_OUTLINED, "Movements", active_key == "Movements"),
        ]

    render_tab_buttons("Inventory")
    def switch_tab(view_key):
        active_tab_ref[0] = view_key # Updates the reference for the exporter
        active_content_container.content = tab_contents[view_key]
        render_tab_buttons(view_key)
        page.update()

    # --- 6. RETURN FULL VIEW ---
    return ft.Column(
        expand=True, spacing=30,
        controls=[
            # Header with Download Button
            ft.Row(
                alignment="spaceBetween",
                controls=[
                    ft.Column(
                        spacing=4,
                        controls=[
                            ft.Row(spacing=8, controls=[ft.Icon(ft.Icons.ANALYTICS_ROUNDED, size=20, color=TEXT_MUTED), ft.Text("System Reports", size=14, color=TEXT_MUTED, weight="bold")]),
                            ft.Text("Reports & Analytics", size=28, weight="bold", color=TEXT_PRIMARY),
                            ft.Text("Comprehensive overview of your supply chain, inventory, and sales.", size=12, color=TEXT_MUTED),
                        ]
                    ),
                    ft.ElevatedButton(
                        content=ft.Row(spacing=6, controls=[ft.Icon(ft.Icons.DOWNLOAD_ROUNDED, size=16), ft.Text("Export to Excel (CSV)")]),
                        bgcolor=ACCENT, color=PANEL_LEFT_BG, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6), padding=ft.Padding.symmetric(horizontal=15, vertical=15)),
                        on_click=export_clicked
                    )
                ]
            ),
            
            # Summary Metrics
            ft.Row(spacing=20, controls=[_summary_card("Total Inventory Value", f"P {total_inventory_value:,.2f}", f"Across {total_items_tracked} items"), _summary_card("Low Stock Alerts", str(low_stock_count), "Items needing replenishment"), _summary_card("Recent Sales Revenue", f"P {total_sales_revenue:,.2f}", f"From last {len(recent_sales)} transactions")]),
            
            # Custom Tab System
            ft.Column(expand=True, spacing=0, controls=[tab_buttons_row, ft.Divider(height=20, color=ft.Colors.TRANSPARENT), active_content_container])
        ]
    )