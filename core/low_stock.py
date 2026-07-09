import flet as ft
from core.theme import *
from core.components import _summary_card, _badge, _cell
from models import inventory_model

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
def nav_section_label(text):
    return ft.Text(text.upper(), size=11, color=TEXT_SECONDARY, weight=ft.FontWeight.BOLD)

def nav_item(text, selected=False, on_nav=None):
    return ft.Container(
        content=ft.Text(text, size=13, color=TEXT_PRIMARY if selected else TEXT_SECONDARY, weight=ft.FontWeight.NORMAL),
        on_click=lambda e: on_nav(text) if on_nav else None,
        padding=ft.Padding.symmetric(vertical=6, horizontal=12), border_radius=6, ink=True,
    )

def build_sidebar(page, user, on_logout, current_page, on_nav):
    logo_block = ft.Column([
        ft.Image(src='assets/LOGO.png', width=319, fit=ft.BoxFit.CONTAIN, align=ft.Alignment.CENTER),
    ], spacing=6)
    
    nav_column = ft.Column([
        nav_section_label("Overview"),
        nav_item("Dashboard", selected=(current_page == "Dashboard"), on_nav=on_nav),
        ft.Container(height=12),
        nav_section_label("Master Records"),
        nav_item("User Management", selected=(current_page == "User Management"), on_nav=on_nav),
        nav_item("Suppliers", selected=(current_page == "Suppliers"), on_nav=on_nav),
        nav_item("Ingredients & Supplies", selected=(current_page == "Ingredients & Supplies"), on_nav=on_nav),
        ft.Container(height=12),
        nav_section_label("Operations"),
        nav_item("Inventory Monitoring", selected=(current_page == "Inventory Monitoring"), on_nav=on_nav),
        nav_item("Low-Stock Items", selected=(current_page == "Low-Stock Items"), on_nav=on_nav),
        nav_item("Purchase Orders", selected=(current_page == "Purchase Orders"), on_nav=on_nav),
        nav_item("Movement History", selected=(current_page == "Movement History"), on_nav=on_nav),
        ft.Container(height=12),
        nav_section_label("Transactions"),
        nav_item("Receiving/Stock-In", selected=(current_page == "Receiving/Stock-In"), on_nav=on_nav),
        nav_item("Stock-Out/Usage", selected=(current_page == "Stock-Out/Usage"), on_nav=on_nav),
        nav_item("Daily Sales", selected=(current_page == "Daily Sales"), on_nav=on_nav),
        ft.Container(height=12),
        nav_section_label("Insights"),
        nav_item("Reports", selected=(current_page == "Reports"), on_nav=on_nav),
    ], spacing=4, scroll=ft.ScrollMode.AUTO, expand=True)
    
    profile_block = ft.Row([
        ft.Icon(ft.Icons.ACCOUNT_CIRCLE_ROUNDED, size=36, color=TEXT_SECONDARY),
        ft.Column([
            ft.Text(user["full_name"], size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Text(user["role"], size=11, color=TEXT_SECONDARY),
        ], spacing=0),
        ft.Container(expand=True),
        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color=ACCENT_GOLD, on_click=lambda e: on_logout()),
    ], spacing=8)
    
    return ft.Container(
        content=ft.Column([logo_block, ft.Container(height=20), nav_column, profile_block], expand=True),
        width=260, bgcolor=SIDEBAR_COLOR, padding=20,
    )

# ==========================================
# MAIN VIEW
# ==========================================
def low_stock_view(page: ft.Page, user, on_logout, on_nav):
    # 1. Initialize Sidebar
    sidebar = build_sidebar(page, user, on_logout, "Low-Stock Items", on_nav)

    # 2. Main container for dynamic updates
    main_container = ft.Column(expand=True, scroll="auto", spacing=30)

    # 3. Dynamic Data Loader
    def load_data(search_query=""):
        main_container.controls.clear()

        # Fetch real data from the database
        all_low_stock_items = inventory_model.get_low_stock_items()
        
        # Apply Search Filter
        if search_query:
            low_stock_items = [
                item for item in all_low_stock_items 
                if search_query.lower() in item['item_name'].lower() 
                or (item['supplier_name'] and search_query.lower() in item['supplier_name'].lower())
            ]
        else:
            low_stock_items = all_low_stock_items

        needs_attention_count = len(low_stock_items)
        out_of_stock_count = sum(1 for item in low_stock_items if float(item['current_quantity']) <= 0)
        
        # Calculate estimated replenishment cost
        replenishment_cost = 0.0
        for item in low_stock_items:
            curr_qty = float(item['current_quantity'])
            ro_level = float(item['reorder_level'])
            cost = float(item['cost_per_unit'])
            
            shortage = max(ro_level - curr_qty, 0)
            suggested_qty = max(shortage, ro_level) # Minimum order of reorder_level
            replenishment_cost += suggested_qty * cost

        action_bar = ft.Row(
            alignment="spaceBetween",
            controls=[
                ft.TextField(
                    hint_text="Search items or suppliers...",
                    hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                    prefix_icon=ft.Icons.SEARCH,
                    bgcolor=INPUT_BG,
                    border_color=ft.colors.TRANSPARENT,
                    border_radius=8,
                    content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                    height=40,
                    width=300,
                    on_change=lambda e: load_data(e.control.value) # Wires up the live search!
                ),
                ft.Container(
                    bgcolor=ACCENT_GOLD,
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                    ink=True,
                    on_click=lambda e: on_nav("Purchase Orders"), # Jumps to PO view to create order
                    content=ft.Text(
                        "New Purchase Order",
                        size=13,
                        weight="bold",
                        color="#000000", 
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
            status_fg = "#F44336" if is_out else ACCENT_GOLD

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
            bgcolor=ft.colors.TRANSPARENT,
            border=ft.border.all(1, CARD_BORDER),
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
        
        # Handle empty state with FIXED lowercase alignment attribute
        if not table_rows:
            table_container = ft.Container(
                padding=40,
                alignment=ft.alignment.center, 
                content=ft.Text("All inventory levels are healthy! No low stock alerts.", color=TEXT_MUTED)
            )
        else:
            table_container = table

        # Repopulate Main Container
        main_container.controls.extend([
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
        ])
        
        page.update()

    # 4. Trigger initial data load
    load_data()

    # 5. Return the combined view
    content_area = ft.Container(
        content=main_container,
        expand=True,
        padding=24,
    )
    
    return ft.Row([sidebar, content_area], expand=True, spacing=0)