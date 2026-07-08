import flet as ft
from core.theme import *
from core.components import _summary_card, _cell, _badge
from models import inventory_model, purchase_order_model, sales_model, supplier_model, stock_movement_model

def AdminReports(page: ft.Page):
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

    # --- 3. CHART GENERATION HELPER ---
    def _build_line_chart(data_points, line_color, max_y, max_x):
        if not data_points or len(data_points) < 2:
            return ft.Container(
                content=ft.Text("Not enough data points to generate chart.", color=TEXT_MUTED), 
                height=150, 
                alignment=ft.alignment.center
            )
            
        chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=data_points,
                    stroke_width=3,
                    color=line_color,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_bgcolor=ft.colors.with_opacity(0.1, line_color)
                )
            ],
            border=ft.border.all(1, CARD_BORDER),
            min_y=0,
            max_y=max_y * 1.2 if max_y > 0 else 10,
            min_x=0,
            max_x=max_x if max_x > 0 else 1,
            tooltip_bgcolor=CARD_COLOR,
            expand=True,
            left_axis=ft.ChartAxis(labels_size=40),
            bottom_axis=ft.ChartAxis(labels_size=20, show_labels=False), # Hiding bottom labels for a clean trendline look
        )
        return ft.Container(content=chart, height=220, padding=ft.padding.symmetric(vertical=10))

    # --- 4. BUILD HELPER TABLES & CHARTS ---
    
    # Table A: Inventory & Low Stock
    inventory_rows = []
    inv_pts = []
    max_inv_qty = 0

    for i, item in enumerate(inventory_data):
        qty = float(item['current_quantity'])
        reorder = float(item['reorder_level'])
        uom = item['unit_of_measurement']
        cost = float(item['cost_per_unit'])
        total_val = float(item['value'] or 0)
        
        # Data for chart
        inv_pts.append(ft.LineChartDataPoint(i, qty))
        if qty > max_inv_qty: max_inv_qty = qty
        
        # Flag low stock items automatically
        status_cell = _badge("Low Stock", "#332400", ACCENT) if qty <= reorder else _badge("Healthy", "#0f2e16", "#22c55e")
        
        inventory_rows.append(ft.DataRow(cells=[
            _cell(item['item_name'], True),
            _cell(f"{qty:g} {uom}"),
            _cell(f"P {cost:,.2f}"),
            _cell(f"P {total_val:,.2f}", is_bold=True),
            ft.DataCell(status_cell)
        ]))
        
    inv_chart = _build_line_chart(inv_pts, ACCENT, max_inv_qty, len(inventory_data)-1)

    inventory_table = ft.DataTable(
        expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8,
        heading_row_color="#1A1A1A", column_spacing=40,
        columns=[
            ft.DataColumn(ft.Text("Item", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Stock Level", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Unit Cost", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Total Value", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Status", size=13, weight="bold", color=TEXT_MUTED)),
        ],
        rows=inventory_rows
    )

    # Table B: Sales Activities
    sales_rows = []
    sales_pts = []
    max_sale_val = 0
    
    # Reverse slice to get chronological order for the trend chart (oldest to newest left-to-right)
    recent_20_sales = list(reversed(recent_sales[:20])) if recent_sales else []

    for i, sale in enumerate(recent_20_sales):
        val = float(sale['line_total'])
        sales_pts.append(ft.LineChartDataPoint(i, val))
        if val > max_sale_val: max_sale_val = val

    for sale in recent_sales:
        sales_rows.append(ft.DataRow(cells=[
            _cell(sale['sales_date'].strftime("%Y-%m-%d %H:%M")),
            _cell(sale['product_name'], True),
            _cell(str(sale['quantity_sold'])),
            _cell(f"P {float(sale['line_total']):,.2f}", is_bold=True, text_color=ACCENT),
            _cell(sale['full_name']),
        ]))
        
    sales_chart = _build_line_chart(sales_pts, STATUS_GREEN, max_sale_val, len(recent_20_sales)-1)

    sales_table = ft.DataTable(
        expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8,
        heading_row_color="#1A1A1A", column_spacing=40,
        columns=[
            ft.DataColumn(ft.Text("Date & Time", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Product Sold", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Qty", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Revenue", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Cashier", size=13, weight="bold", color=TEXT_MUTED)),
        ],
        rows=sales_rows
    )

    # Table C: Stock Movement History
    movement_rows = []
    mov_pts = []
    max_mov_qty = 0
    
    # Reverse slice for chronological chart
    recent_20_movs = list(reversed(movements[:20])) if movements else []

    for i, mov in enumerate(recent_20_movs):
        val = float(mov['quantity'])
        mov_pts.append(ft.LineChartDataPoint(i, val))
        if val > max_mov_qty: max_mov_qty = val

    for mov in movements:
        m_type = mov['movement_type']
        color = "#22c55e" if m_type == "Stock-In" else ACCENT
        movement_rows.append(ft.DataRow(cells=[
            _cell(mov['movement_date'].strftime("%Y-%m-%d %H:%M")),
            _cell(mov['item_name'], True),
            _cell(m_type, text_color=color),
            _cell(str(float(mov['quantity']))),
            _cell(str(float(mov['resulting_stock']))),
            _cell(mov['reference_type'] or "N/A"),
        ]))
        
    mov_chart = _build_line_chart(mov_pts, ft.colors.BLUE_400, max_mov_qty, len(recent_20_movs)-1)
        
    movements_table = ft.DataTable(
        expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8,
        heading_row_color="#1A1A1A", column_spacing=40,
        columns=[
            ft.DataColumn(ft.Text("Date", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Item", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Type", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Qty Changed", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Resulting Stock", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Reference", size=13, weight="bold", color=TEXT_MUTED)),
        ],
        rows=movement_rows
    )

    # --- 5. CUSTOM TAB SYSTEM WITH CHARTS ---
    
    # Pre-build the content containers
    tab_contents = {
        "Inventory": ft.Column(scroll="auto", controls=[
            ft.Text("Inventory Levels (All Items)", size=16, weight="bold", color=TEXT_PRIMARY),
            inv_chart,
            ft.Container(height=10),
            inventory_table
        ]),
        "Sales": ft.Column(scroll="auto", controls=[
            ft.Text("Recent Sales Revenue Trend (Last 20)", size=16, weight="bold", color=TEXT_PRIMARY),
            sales_chart,
            ft.Container(height=10),
            sales_table
        ]),
        "Movements": ft.Column(scroll="auto", controls=[
            ft.Text("Stock Movement Volume (Last 20)", size=16, weight="bold", color=TEXT_PRIMARY),
            mov_chart,
            ft.Container(height=10),
            movements_table
        ])
    }
    
    # This container holds the active table and chart
    active_content_container = ft.Container(
        expand=True,
        padding=ft.Padding.only(top=20),
        content=tab_contents["Inventory"] # Default view
    )

    # Define the tab buttons
    def create_tab_button(title, icon_name, view_key, is_active=False):
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=20, vertical=10),
            border_radius=8,
            bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT,
            border=ft.Border.all(1, ACCENT if is_active else CARD_BORDER),
            ink=True,
            on_click=lambda e: switch_tab(view_key),
            content=ft.Row(
                spacing=8,
                controls=[
                    ft.Icon(icon_name, size=16, color=ACCENT if is_active else TEXT_MUTED),
                    ft.Text(title, size=13, weight="bold" if is_active else "normal", color=TEXT_PRIMARY if is_active else TEXT_MUTED)
                ]
            )
        )
        
    # Container for the buttons
    tab_buttons_row = ft.Row(spacing=15)
    
    def render_tab_buttons(active_key):
        tab_buttons_row.controls = [
            create_tab_button("Inventory & Valuation", ft.Icons.INVENTORY_2_OUTLINED, "Inventory", active_key == "Inventory"),
            create_tab_button("Sales Revenue", ft.Icons.POINT_OF_SALE_OUTLINED, "Sales", active_key == "Sales"),
            create_tab_button("Stock Movements", ft.Icons.SWAP_HORIZ_OUTLINED, "Movements", active_key == "Movements"),
        ]

    # Initialize buttons
    render_tab_buttons("Inventory")

    def switch_tab(view_key):
        # Update content
        active_content_container.content = tab_contents[view_key]
        # Update button highlights
        render_tab_buttons(view_key)
        page.update()


    # --- 6. RETURN FULL VIEW ---
    return ft.Column(
        expand=True,
        spacing=30,
        controls=[
            # Header
            ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.ANALYTICS_ROUNDED, size=20, color=TEXT_MUTED),
                            ft.Text("System Reports", size=14, color=TEXT_MUTED, weight="bold")
                        ]
                    ),
                    ft.Container(height=10),
                    ft.Text("Reports & Analytics", size=28, weight="bold", color=TEXT_PRIMARY),
                    ft.Text("Comprehensive overview of your supply chain, inventory, and sales.", size=12, color=TEXT_MUTED),
                ]
            ),
            
            # Summary Metrics
            ft.Row(
                spacing=20,
                controls=[
                    _summary_card("Total Inventory Value", f"P {total_inventory_value:,.2f}", f"Across {total_items_tracked} items"),
                    _summary_card("Low Stock Alerts", str(low_stock_count), "Items needing replenishment"),
                    _summary_card("Recent Sales Revenue", f"P {total_sales_revenue:,.2f}", f"From last {len(recent_sales)} transactions"),
                ]
            ),
            
            # Custom Tab System
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    tab_buttons_row,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # spacer
                    active_content_container
                ]
            )
        ]
    )