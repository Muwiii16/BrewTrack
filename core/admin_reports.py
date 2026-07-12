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
    inventory_data = inventory_model.get_inventory_overview() or []
    pending_pos = purchase_order_model.get_pending_orders_count()
    recent_sales = sales_model.get_recent_sales(limit=100) or []
    po_history = purchase_order_model.get_purchase_orders()
    movements = stock_movement_model.get_recent_movements(limit=100) or []
    suppliers = supplier_model.get_suppliers()

    # Create a fast lookup map using the loaded inventory data to fill in missing category/supplier info
    item_lookup = {item.get("item_name"): item for item in inventory_data if item.get("item_name")}

    def _movement_category(mov):
        return item_lookup.get(mov.get("item_name"), {}).get("category") or "Uncategorized"

    def _movement_supplier(mov):
        return item_lookup.get(mov.get("item_name"), {}).get("supplier_name") or "Unknown"

    # --- 2. CALCULATE AGGREGATES ---
    total_inventory_value = sum(float(item.get('value', 0) or 0) for item in inventory_data)
    total_sales_revenue = sum(float(sale.get('line_total', 0) or 0) for sale in recent_sales)
    total_items_tracked = len(inventory_data)
    low_stock_count = sum(1 for item in inventory_data if float(item.get('current_quantity', 0)) <= float(item.get('reorder_level', 0)))

    # --- 3. EXPORT TO CSV ---
    def export_clicked(e):
        try:
            filename = f"BrewTrack_{active_tab_ref[0].replace(' ', '_')}_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                
                if active_tab_ref[0] == "Inventory":
                    writer.writerow(["Item Name", "Stock Level", "UOM", "Unit Cost", "Total Value", "Status"])
                    for item in inventory_data:
                        qty = float(item['current_quantity'])
                        reorder = float(item['reorder_level'])
                        status = "Low Stock" if qty <= reorder else "Healthy"
                        writer.writerow([
                            item['item_name'], f"{qty:g}", item['unit_of_measurement'], 
                            f"{float(item['cost_per_unit']):.2f}", f"{float(item.get('value', 0) or 0):.2f}", status
                        ])
                        
                elif active_tab_ref[0] == "Sales":
                    writer.writerow(["Date & Time", "Product Sold", "Qty", "Revenue", "Cashier"])
                    for sale in recent_sales:
                        writer.writerow([
                            sale['sales_date'].strftime("%Y-%m-%d %H:%M"), sale['product_name'], 
                            sale['quantity_sold'], f"{float(sale['line_total']):.2f}", sale['full_name']
                        ])
                        
                elif active_tab_ref[0] == "Movements":
                    writer.writerow(["Date", "Item", "Category", "Supplier", "Type", "Qty Changed", "Resulting Stock", "Reference"])
                    for mov in movements:
                        if not _movement_matches(mov):
                            continue
                        writer.writerow([
                            mov['movement_date'].strftime("%Y-%m-%d %H:%M"), mov['item_name'], 
                            _movement_category(mov), _movement_supplier(mov),
                            mov['movement_type'], mov['quantity'], mov['resulting_stock'], mov.get('reference_type') or "N/A"
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

    # --- 4. LABELED BAR CHART ---
    def _build_labeled_bar_chart(bars_data, title, value_prefix="", value_suffix="", height=140, bar_width=32, default_color=ACCENT, legend=None):
        if not bars_data:
            return ft.Container(
                padding=20,
                border=ft.Border(bottom=ft.BorderSide(1, CARD_BORDER)),
                content=ft.Column(spacing=10, controls=[
                    ft.Text(title, size=13, weight="bold", color=TEXT_PRIMARY),
                    ft.Row([ft.Text("Not enough data to graph.", color=TEXT_MUTED)], alignment="center")
                ])
            )

        max_val = max(b["value"] for b in bars_data) or 1

        def _truncate(s, n=10):
            s = str(s)
            return s if len(s) <= n else s[:n - 1] + "…"

        bars = []
        for b in bars_data:
            val = b["value"]
            color = b.get("color", default_color)
            bar_h = max(4, (val / max_val) * height) if max_val > 0 else 4
            tooltip = b.get("tooltip", f"{b['label']}: {value_prefix}{val:,.2f}{value_suffix}")
            bars.append(
                ft.Column(
                    width=bar_width + 24,
                    spacing=6,
                    horizontal_alignment="center",
                    controls=[
                        ft.Text(f"{val:,.0f}", size=9, color=TEXT_MUTED),
                        ft.Container(
                            height=height,
                            alignment=ft.alignment.Alignment(0, 1),
                            content=ft.Container(
                                width=bar_width, height=bar_h, bgcolor=color,
                                border_radius=ft.BorderRadius(top_left=4, top_right=4, bottom_left=0, bottom_right=0),
                                tooltip=tooltip
                            )
                        ),
                        ft.Container(
                            width=bar_width + 24,
                            content=ft.Text(_truncate(b["label"]), size=9, color=TEXT_MUTED, text_align="center", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, tooltip=str(b["label"]))
                        )
                    ]
                )
            )

        header_controls = [ft.Text(title, size=13, weight="bold", color=TEXT_PRIMARY)]
        if legend:
            header_controls.append(
                ft.Row(spacing=14, controls=[
                    ft.Row(spacing=6, controls=[ft.Container(width=10, height=10, bgcolor=c, border_radius=3), ft.Text(l, size=11, color=TEXT_MUTED)])
                    for l, c in legend
                ])
            )
        else:
            header_controls.append(ft.Text(f"Peak: {value_prefix}{max_val:,.2f}{value_suffix}", size=11, color=TEXT_MUTED))

        return ft.Container(
            padding=20,
            border=ft.Border(bottom=ft.BorderSide(1, CARD_BORDER)),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(alignment="spaceBetween", controls=header_controls),
                    ft.Row(controls=bars, spacing=15, scroll="auto", vertical_alignment="end")
                ]
            )
        )

    # --- 5. INVENTORY & SALES TABLES ---
    inventory_rows, inv_bars_data = [], []
    for item in inventory_data:
        qty = float(item['current_quantity'])
        reorder = float(item['reorder_level'])
        inv_bars_data.append({"label": item['item_name'], "value": qty})
        status_cell = _badge("Low Stock", "#332400", ACCENT) if qty <= reorder else _badge("Healthy", "#0f2e16", "#22c55e")
        inventory_rows.append(ft.DataRow(cells=[_cell(item['item_name'], True), _cell(f"{qty:g} {item['unit_of_measurement']}"), _cell(f"P {float(item['cost_per_unit']):,.2f}"), _cell(f"P {float(item.get('value', 0) or 0):,.2f}", is_bold=True), ft.DataCell(status_cell)]))

    inv_chart = _build_labeled_bar_chart(inv_bars_data, "Inventory Stock Levels (All Items)", default_color=ACCENT)
    inventory_table = ft.DataTable(expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8, heading_row_color="#1A1A1A", columns=[ft.DataColumn(ft.Text(h, size=13, weight="bold", color=TEXT_MUTED)) for h in ["Item", "Stock Level", "Unit Cost", "Total Value", "Status"]], rows=inventory_rows)

    sales_rows = []
    recent_20_sales = list(reversed(recent_sales[:20])) if recent_sales else []
    sales_bars_data = [{"label": sale['product_name'], "value": float(sale['line_total'])} for sale in recent_20_sales]

    for sale in recent_sales:
        sales_rows.append(ft.DataRow(cells=[_cell(sale['sales_date'].strftime("%Y-%m-%d %H:%M")), _cell(sale['product_name'], True), _cell(str(sale['quantity_sold'])), _cell(f"P {float(sale['line_total']):,.2f}", is_bold=True, text_color=ACCENT), _cell(sale['full_name'])]))

    sales_chart = _build_labeled_bar_chart(sales_bars_data, "Recent Sales Revenue (Last 20)", value_prefix="P ", default_color="#4CAF50")
    sales_table = ft.DataTable(expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8, heading_row_color="#1A1A1A", columns=[ft.DataColumn(ft.Text(h, size=13, weight="bold", color=TEXT_MUTED)) for h in ["Date & Time", "Product Sold", "Qty", "Revenue", "Cashier"]], rows=sales_rows)

    # --- 6. REVISED MOVEMENT FILTERS ---
    movement_filters = {"search": "", "category": "All", "supplier": "All"}

    # Build distinct filter lists from the mapped movements
    distinct_categories = sorted({_movement_category(m) for m in movements})
    distinct_suppliers = sorted({_movement_supplier(m) for m in movements})

    # Create dropdown options
    category_options = [ft.dropdown.Option("All", "All Categories")] + [
        ft.dropdown.Option(cat, cat) for cat in distinct_categories
    ]
    supplier_options = [ft.dropdown.Option("All", "All Suppliers")] + [
        ft.dropdown.Option(sup, sup) for sup in distinct_suppliers
    ]

    # Dropdown widgets
    category_dropdown = ft.Dropdown(
        value="All",
        options=category_options,
        border_color=CARD_BORDER,
        bgcolor=INPUT_BG,
        text_style=ft.TextStyle(size=13, color=TEXT_PRIMARY),
        label="Category",
        label_style=ft.TextStyle(size=12, color=TEXT_MUTED),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
        width=180,
        dense=True,
    )
    supplier_dropdown = ft.Dropdown(
        value="All",
        options=supplier_options,
        border_color=CARD_BORDER,
        bgcolor=INPUT_BG,
        text_style=ft.TextStyle(size=13, color=TEXT_PRIMARY),
        label="Supplier",
        label_style=ft.TextStyle(size=12, color=TEXT_MUTED),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
        width=200,
        dense=True,
    )

    # Filter matching logic
    def _movement_matches(mov):
        if movement_filters["category"] != "All" and _movement_category(mov) != movement_filters["category"]:
            return False
        if movement_filters["supplier"] != "All" and _movement_supplier(mov) != movement_filters["supplier"]:
            return False
        if movement_filters["search"]:
            q = movement_filters["search"].strip().lower()
            if q not in (mov["item_name"] or "").lower():
                return False
        return True

    # Event handlers: Safely pull values directly from e.control.value
    def on_category_change(e):
        movement_filters["category"] = e.control.value
        refresh_movements_view()

    def on_supplier_change(e):
        movement_filters["supplier"] = e.control.value
        refresh_movements_view()

    category_dropdown.on_change = on_category_change
    supplier_dropdown.on_change = on_supplier_change

    def on_movement_search_change(e):
        movement_filters["search"] = e.control.value or ""
        refresh_movements_view()

    movement_search_field = ft.TextField(
        hint_text="Search by item name", prefix_icon=ft.Icons.SEARCH, bgcolor=INPUT_BG,
        border_color=ft.Colors.TRANSPARENT, border_radius=8, height=40, width=280,
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
        hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        on_change=on_movement_search_change
    )

    movement_filters_row = ft.Row(spacing=12, controls=[
        movement_search_field,
        category_dropdown,
        supplier_dropdown,
    ])

    # Movements table & chart
    movements_table = ft.DataTable(expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8, heading_row_color="#1A1A1A",
        columns=[ft.DataColumn(ft.Text(h, size=13, weight="bold", color=TEXT_MUTED)) for h in ["Date", "Item", "Category", "Supplier", "Type", "Qty Changed", "Resulting Stock", "Reference"]],
        rows=[])
    mov_chart_container = ft.Container()

    def build_movement_row(mov):
        color = "#22c55e" if mov['movement_type'] == "Stock-In" else ACCENT
        return ft.DataRow(cells=[
            _cell(mov['movement_date'].strftime("%Y-%m-%d %H:%M")),
            _cell(mov['item_name'], True),
            _cell(_movement_category(mov)),
            _cell(_movement_supplier(mov)),
            _cell(mov['movement_type'], text_color=color),
            _cell(str(float(mov['quantity']))),
            _cell(str(float(mov['resulting_stock']))),
            _cell(mov.get('reference_type') or "N/A")
        ])

    def refresh_movements_view(is_initial=False):
        filtered = [m for m in movements if _movement_matches(m)]
        if not filtered:
            movements_table.rows = []
            mov_chart_container.content = ft.Text("No movement data found with current filters.", color=TEXT_MUTED)
        else:
            chart_source = list(reversed(filtered[:20]))
            bars_data = [
                {
                    "label": m["item_name"],
                    "value": abs(float(m["quantity"])),
                    "color": "#22c55e" if m["movement_type"] == "Stock-In" else ACCENT,
                    "tooltip": f"{m['item_name']}: {m['movement_type']} {float(m['quantity']):+g}"
                }
                for m in chart_source
            ]
            mov_chart_container.content = _build_labeled_bar_chart(
                bars_data, "Stock Movement Volume (Last 20, filtered)",
                legend=[("Stock-In", "#22c55e"), ("Stock-Out / Adjustment", ACCENT)]
            )
            movements_table.rows = [build_movement_row(m) for m in filtered]
            
        # explicitly command Flet to redraw these containers to prevent diff rendering glitches
        if not is_initial:
            if mov_chart_container.page:
                mov_chart_container.update()
            if movements_table.page:
                movements_table.update()
            page.update()

    refresh_movements_view(is_initial=True)   # initial render safely without page.update()

    # --- 7. CUSTOM TAB SYSTEM ---
    tab_contents = {
        "Inventory": ft.Column(scroll="auto", controls=[ft.Text("Inventory Levels (All Items)", size=16, weight="bold", color=TEXT_PRIMARY), inv_chart, ft.Container(height=10), inventory_table]),
        "Sales": ft.Column(scroll="auto", controls=[ft.Text("Recent Sales Revenue Trend (Last 20)", size=16, weight="bold", color=TEXT_PRIMARY), sales_chart, ft.Container(height=10), sales_table]),
        "Movements": ft.Column(scroll="auto", spacing=15, controls=[ft.Text("Stock Movement Volume & History", size=16, weight="bold", color=TEXT_PRIMARY), movement_filters_row, mov_chart_container, ft.Container(height=10), movements_table])
    }
    
    active_content_container = ft.Container(expand=True, padding=20, content=tab_contents["Inventory"])

    def create_tab_button(title, icon_name, view_key, is_active=False):
        return ft.Container(
            padding=ft.Padding.symmetric(horizontal=20, vertical=10), border_radius=8,
            bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT,
            border=ft.Border.all(1, ACCENT if is_active else CARD_BORDER), ink=True,
            on_click=lambda e: switch_tab(view_key),
            content=ft.Row(spacing=8, controls=[
                ft.Icon(icon_name, size=16, color=ACCENT if is_active else TEXT_MUTED),
                ft.Text(title, size=13, weight="bold" if is_active else "normal", color=TEXT_PRIMARY if is_active else TEXT_MUTED)
            ])
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
        active_tab_ref[0] = view_key
        active_content_container.content = tab_contents[view_key]
        render_tab_buttons(view_key)
        page.update()

    # --- RETURN FULL VIEW ---
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
                        bgcolor=ACCENT, color=PANEL_LEFT_BG,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6), padding=ft.Padding.symmetric(horizontal=15, vertical=15)),
                        on_click=export_clicked
                    )
                ]
            ),
            
            # Summary Metrics
            ft.Row(spacing=20, controls=[
                _summary_card("Total Inventory Value", f"P {total_inventory_value:,.2f}", f"Across {total_items_tracked} items"),
                _summary_card("Low Stock Alerts", str(low_stock_count), "Items needing replenishment"),
                _summary_card("Recent Sales Revenue", f"P {total_sales_revenue:,.2f}", f"From last {len(recent_sales)} transactions")
            ]),
            
            # Custom Tab System
            ft.Column(expand=True, spacing=0, controls=[
                tab_buttons_row,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                active_content_container
            ])
        ]
    )