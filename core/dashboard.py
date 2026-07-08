import flet as ft
from core.theme import *
from core.components import _sidebar_section_title
from core.admin_overview import AdminOverview
from core.admin_low_stock import AdminLowStock
from core.admin_po import AdminPurchaseOrders
from models import supplier_model, ingredient_model, purchase_order_model

def dashboard_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    
    sidebar_container = ft.Container(
        width=240,
        bgcolor=PANEL_LEFT_BG,
        padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )
    
    main_content = ft.Container(
        expand=True,
        padding=40
    )
    
    # --- NEW PO MODAL LOGIC & STATE ---
    ingredients_map = {}
    
    supplier_dropdown = ft.Dropdown(
        hint_text="Select Supplier",
        hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
        bgcolor=INPUT_BG,
        border_color=INPUT_BORDER,
        border_radius=8,
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
    )
    
    expected_date_field = ft.TextField(
        hint_text="YYYY-MM-DD",
        hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
        bgcolor=INPUT_BG,
        border_color=INPUT_BORDER,
        border_radius=8,
        suffix_icon=ft.Icons.CALENDAR_TODAY,
        text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
    )
    
    lines_container = ft.Column(spacing=10)
    grand_total_text = ft.Text("P 0.00", size=18, weight="bold", color=TEXT_PRIMARY)

    def calculate_totals(e=None):
        total = 0.0
        for row in lines_container.controls:
            item_id = row.controls[0].value
            qty_str = row.controls[1].value or "0"
            line_total_text = row.controls[2]
            
            try:
                qty = float(qty_str)
            except ValueError:
                qty = 0.0
                
            if item_id and item_id in ingredients_map:
                unit_price = float(ingredients_map[item_id]["cost_per_unit"])
                line_total = qty * unit_price
                line_total_text.value = f"P {line_total:,.2f}"
                total += line_total
            else:
                line_total_text.value = "P 0.00"
                
        grand_total_text.value = f"P {total:,.2f}"
        page.update()

    def add_line(e=None):
        def remove_line(e_remove):
            lines_container.controls.remove(row)
            calculate_totals()
        
        options = [
            ft.dropdown.Option(key=str(item_id), text=f"{data['item_name']} (P{data['cost_per_unit']})")
            for item_id, data in ingredients_map.items()
        ]
        
        item_dropdown = ft.Dropdown(
            expand=2,
            hint_text="Choose item",
            hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
            bgcolor=INPUT_BG,
            border_color=INPUT_BORDER,
            border_radius=8,
            text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
            options=options
        )
        item_dropdown.on_change = calculate_totals
        
        qty_field = ft.TextField(
            expand=1,
            hint_text="Qty",
            hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
            bgcolor=INPUT_BG,
            border_color=INPUT_BORDER,
            border_radius=8,
            text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13)
        )
        qty_field.on_change = calculate_totals
        
        row = ft.Row(
            vertical_alignment="center",
            controls=[
                item_dropdown,
                qty_field,
                ft.Text("P 0.00", size=14, weight="bold", color=TEXT_PRIMARY, text_align="right", width=80),
                ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color="#F44336", on_click=remove_line)
            ]
        )
        lines_container.controls.append(row)
        if e: # if triggered by button click
            page.update()

    def open_new_po_modal(e):
        # Fetch fresh data
        suppliers = supplier_model.get_suppliers()
        ingredients = ingredient_model.get_ingredients()
        
        # Map ingredients for quick price lookup
        ingredients_map.clear()
        for i in ingredients:
            ingredients_map[str(i['item_id'])] = i
            
        supplier_dropdown.options = [
            ft.dropdown.Option(key=str(s['supplier_id']), text=s['supplier_name']) 
            for s in suppliers
        ]
        supplier_dropdown.value = None
        expected_date_field.value = ""
        
        # Reset lines
        lines_container.controls.clear()
        add_line() # Add one initial empty line
        calculate_totals()

        if new_po_dialog not in page.overlay:
            page.overlay.append(new_po_dialog)
        new_po_dialog.open = True
        page.update()

    def close_new_po_modal(e):
        new_po_dialog.open = False
        page.update()
        
    def submit_purchase_order(e):
        supplier_id = supplier_dropdown.value
        expected_date = expected_date_field.value
        
        if not supplier_id or not expected_date:
            snack = ft.SnackBar(content=ft.Text("Please select a supplier and expected date (YYYY-MM-DD)."), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return
            
        line_items = []
        for row in lines_container.controls:
            item_id = row.controls[0].value
            qty_str = row.controls[1].value
            if item_id and qty_str:
                try:
                    qty = float(qty_str)
                    if qty > 0:
                        unit_cost = float(ingredients_map[item_id]["cost_per_unit"])
                        line_items.append({
                            "item_id": int(item_id),
                            "qty": qty,
                            "unit_cost": unit_cost
                        })
                except ValueError:
                    pass
                    
        if not line_items:
            snack = ft.SnackBar(content=ft.Text("Please add at least one valid line item with a quantity."), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return
            
        try:
            # Create the order in the database
            uid = user["user_id"] if user and "user_id" in user else 1 
            purchase_order_model.create_purchase_order(supplier_id, uid, expected_date, line_items)
            
            # Show success message
            snack = ft.SnackBar(content=ft.Text("Purchase Order created successfully!"), bgcolor=ft.Colors.GREEN_800)
            page.overlay.append(snack)
            snack.open = True
            
            close_new_po_modal(None)
            
            # Auto-route them to the PO tab to see their new order!
            render_view("Purchase Orders")
            
        except Exception as ex:
            snack = ft.SnackBar(content=ft.Text(f"Database error: {str(ex)}"), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    new_po_dialog = ft.AlertDialog(
        bgcolor=PANEL_RIGHT_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        title=ft.Column(
            spacing=4,
            controls=[
                ft.Text("New Purchase Order", size=24, weight="bold", color=TEXT_PRIMARY),
                ft.Text("Order stock from a supplier. Costs default to each item's unit cost", size=12, color=TEXT_MUTED)
            ]
        ),
        content=ft.Container(
            width=600,
            content=ft.Column(
                tight=True,
                spacing=20,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                expand=1,
                                controls=[
                                    ft.Text("Supplier", size=14, weight="bold", color=TEXT_PRIMARY),
                                    supplier_dropdown
                                ]
                            ),
                            ft.Column(
                                expand=1,
                                controls=[
                                    ft.Text("Expected Date", size=14, weight="bold", color=TEXT_PRIMARY),
                                    expected_date_field
                                ]
                            )
                        ]
                    ),
                    ft.Text("Line Items", size=14, weight="bold", color=TEXT_PRIMARY),
                    lines_container,
                    ft.Container(
                        padding=ft.Padding.symmetric(vertical=10, horizontal=20),
                        border=ft.Border.all(1, INPUT_BORDER),
                        border_radius=8,
                        ink=True,
                        on_click=add_line,
                        content=ft.Text("+ Add Line", size=12, color=TEXT_MUTED)
                    ),
                    ft.Divider(color=CARD_BORDER),
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Text("Order Total", size=18, weight="bold", color=TEXT_PRIMARY),
                            grand_total_text
                        ]
                    )
                ]
            )
        ),
        actions=[
            ft.TextButton(
                "Cancel", 
                style=ft.ButtonStyle(color=TEXT_MUTED),
                on_click=close_new_po_modal
            ),
            ft.Container(
                bgcolor=ACCENT,
                padding=ft.Padding.symmetric(horizontal=20, vertical=10),
                border_radius=8,
                ink=True,
                on_click=submit_purchase_order,
                content=ft.Text("Create Order", size=13, weight="bold", color=PANEL_LEFT_BG)
            )
        ]
    )

    def navigate_to(e, view_name):
        # Local rendering for dashboard sub-views
        if view_name in ["Dashboard", "Low-Stock Alerts", "Purchase Orders"]:
            render_view(view_name)
            page.update()
        # Global routing for other main modules (e.g., User Management)
        elif global_navigate_to:
            global_navigate_to(view_name)

    def build_sidebar(active_view: str):
        
        # Get dynamic user info or fallback to defaults
        user_name = user["full_name"] if user else "Juan Dela Cruz"
        user_role = user["role"] if user else "Owner / Admin"

        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10),
                border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT,
                ink=True,
                on_click=lambda e: navigate_to(e, title),
                content=ft.Text(
                    title,
                    size=13,
                    color=TEXT_PRIMARY if is_active else "#CCCCCC",
                    weight="bold" if is_active else "normal",
                ),
            )

        return ft.Column(
            expand=True,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Icon(ft.Icons.COFFEE, size=24, color=ACCENT),
                        ft.Text("BUT FIRST, COFFEE", size=10, weight="bold", color=ACCENT, style=ft.TextStyle(letter_spacing=1.5)),
                        ft.Text("BREWTRACK", size=22, weight="bold", color=TEXT_PRIMARY, font_family=FONT_HEADING),
                    ]
                ),
                ft.Divider(height=30, color=CARD_BORDER),
                
                ft.Column(
                    expand=True,
                    spacing=2,
                    scroll="hidden",
                    controls=[
                        _sidebar_section_title("Overview"),
                        _sidebar_link("Dashboard"),
                        
                        _sidebar_section_title("Master Records"),
                        _sidebar_link("User Management"),
                        _sidebar_link("Suppliers"),
                        _sidebar_link("Ingredients & Supplies"),
                        
                        _sidebar_section_title("Operations"),
                        _sidebar_link("Inventory Monitoring"),
                        _sidebar_link("Low-Stock Alerts"),
                        _sidebar_link("Purchase Orders"),
                        _sidebar_link("Movement History"),
                        
                        _sidebar_section_title("Transactions"),
                        _sidebar_link("Receiving/ Stock-In"),
                        _sidebar_link("Stock-Out/ Usage"),
                        _sidebar_link("Daily Sales"),
                        
                        _sidebar_section_title("Insights"),
                        _sidebar_link("Reports"),
                    ]
                ),
                
                ft.Divider(height=20, color=CARD_BORDER),
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Row(
                            spacing=12,
                            controls=[
                                ft.CircleAvatar(
                                    bgcolor=TEXT_PRIMARY,
                                    color=PANEL_LEFT_BG,
                                    radius=18,
                                    content=ft.Icon(ft.Icons.PERSON, size=20)
                                ),
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text(user_name, size=13, weight="bold", color=TEXT_PRIMARY),
                                        ft.Text(user_role, size=11, color=TEXT_MUTED),
                                    ]
                                )
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT, 
                            icon_color=ACCENT, 
                            icon_size=20, 
                            tooltip="Log Out",
                            on_click=lambda e: show_login() if show_login else None
                        )
                    ]
                )
            ]
        )

    def render_view(view_name: str):
        sidebar_container.content = build_sidebar(view_name)
        
        # Route to the correct separated file
        if view_name == "Dashboard":
            main_content.content = AdminOverview(page)
        elif view_name == "Low-Stock Alerts":
            main_content.content = AdminLowStock(page, open_new_po_modal)
        elif view_name == "Purchase Orders":
            main_content.content = AdminPurchaseOrders(page, open_new_po_modal)

    # Load default view on initialization
    render_view("Dashboard")

    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        content=ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar_container,
                main_content,
            ]
        )
    )