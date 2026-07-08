import flet as ft
from core.theme import *
from core.components import _sidebar_section_title
from core.admin_overview import AdminOverview
from core.admin_low_stock import AdminLowStock
from core.admin_po import AdminPurchaseOrders
from core.admin_reports import AdminReports
from models import supplier_model, ingredient_model, purchase_order_model
from datetime import datetime

def dashboard_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None, initial_view="Dashboard"):
    
    sidebar_container = ft.Container(
        width=240,
        bgcolor=PANEL_LEFT_BG,
        padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )
    
    main_content = ft.Container(
        expand=True,
        padding=40,
        bgcolor=BG_COLOR
    )

    try:
        suppliers = supplier_model.get_suppliers()
        ingredients = ingredient_model.get_ingredients()
    except Exception as e:
        suppliers = []
        ingredients = []

    supplier_dropdown = ft.Dropdown(
        hint_text="Select Supplier",
        options=[ft.dropdown.Option(key=str(s['supplier_id']), text=s['supplier_name']) for s in suppliers],
        bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=40
    )
    
    expected_date_field = ft.TextField(
        hint_text="YYYY-MM-DD",
        bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=40
    )
    
    line_items_container = ft.Column(spacing=10)
    order_total_text = ft.Text("P 0.00", size=18, weight="bold", color=TEXT_PRIMARY)

    def calculate_totals(e=None):
        total = 0.0
        for line in line_items_container.controls:
            try:
                dropdown = line.controls[0]
                qty_field = line.controls[1]
                total_text = line.controls[2]
                
                qty = float(qty_field.value) if qty_field.value else 0.0
                price = 0.0
                if dropdown.value:
                    for ing in ingredients:
                        if str(ing['item_id']) == dropdown.value:
                            price = float(ing['cost_per_unit'])
                            break
                line_total = qty * price
                total_text.value = f"P {line_total:,.2f}"
                if e:
                    total_text.update()  # <-- Only update if triggered by a user action
                total += line_total
            except Exception:
                pass
        order_total_text.value = f"P {total:,.2f}"
        if e:
            order_total_text.update() # <-- Only update if triggered by a user action

    def delete_line(line_container):
        line_items_container.controls.remove(line_container)
        calculate_totals()
        new_po_dialog.update()
    
    def add_line(e=None):
        item_dropdown = ft.Dropdown(
            hint_text="Choose item",
            options=[ft.dropdown.Option(key=str(ing['item_id']), text=f"{ing['item_name']} (P{ing['cost_per_unit']})") for ing in ingredients],
            bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=40, expand=2
        )
        item_dropdown.on_change = calculate_totals
        
        qty_field = ft.TextField(
            hint_text="Qty",
            bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=40, expand=1
        )
        qty_field.on_change = calculate_totals
        
        line_total_text = ft.Text("P 0.00", size=14, color=TEXT_PRIMARY, weight="bold", width=80, text_align="right")
        
        # 1. Create the empty row first
        line_row = ft.Row(alignment="spaceBetween", vertical_alignment="center")
        
        # 2. Create the delete button, which can now safely reference line_row
        delete_btn = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE, 
            icon_color="#F44336", 
            tooltip="Delete Line", 
            on_click=lambda e: delete_line(line_row)
        )
        
        # 3. Add all controls into the row
        line_row.controls = [item_dropdown, qty_field, line_total_text, delete_btn]
        
        line_items_container.controls.append(line_row)
        if e: 
            new_po_dialog.update()

    def create_po(e=None):
        if not supplier_dropdown.value or not expected_date_field.value:
            snack = ft.SnackBar(content=ft.Text("Please select a supplier and expected date."), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return

        po_items = []
        for line in line_items_container.controls:
            dd = line.controls[0]
            qf = line.controls[1]
            if dd.value and qf.value:
                cost = 0.0
                for ing in ingredients:
                    if str(ing['item_id']) == dd.value:
                        cost = float(ing['cost_per_unit'])
                        break
                po_items.append({
                    "item_id": int(dd.value),
                    "qty": float(qf.value),
                    "unit_cost": cost
                })
        
        if not po_items:
            snack = ft.SnackBar(content=ft.Text("Please add at least one line item."), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return
            
        try:
            purchase_order_model.create_purchase_order(
                int(supplier_dropdown.value),
                user['user_id'] if user else 1,
                expected_date_field.value,
                po_items
            )
            new_po_dialog.open = False
            snack = ft.SnackBar(content=ft.Text("Purchase Order created successfully!"), bgcolor=ft.Colors.GREEN_800)
            page.overlay.append(snack)
            snack.open = True
            
            render_view("Purchase Orders")
        except Exception as ex:
            snack = ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    new_po_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=PANEL_RIGHT_BG,
        shape=ft.RoundedRectangleBorder(radius=10),
        title=ft.Column(
            spacing=4,
            controls=[
                ft.Text("New Purchase Order", size=24, color=TEXT_PRIMARY, weight="bold"),
                ft.Text("Order stock from a supplier. Costs default to each item's unit cost", size=12, color=TEXT_MUTED),
            ]
        ),
        content=ft.Container(
            width=600,
            content=ft.Column(
                spacing=20,
                tight=True,
                controls=[
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Column(expand=1, spacing=4, controls=[ft.Text("Supplier", size=12, weight="bold", color=TEXT_PRIMARY), supplier_dropdown]),
                            ft.Column(expand=1, spacing=4, controls=[ft.Text("Expected Date", size=12, weight="bold", color=TEXT_PRIMARY), expected_date_field]),
                        ]
                    ),
                    ft.Divider(height=1, color=CARD_BORDER),
                    ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text("Line Items", size=12, weight="bold", color=TEXT_PRIMARY),
                            line_items_container,
                            ft.Container(
                                border=ft.Border.all(1, CARD_BORDER), border_radius=6, padding=ft.Padding.symmetric(vertical=6, horizontal=10),
                                ink=True, on_click=add_line, content=ft.Text("+ Add Line", size=11, color=TEXT_MUTED)
                            )
                        ]
                    ),
                    ft.Divider(height=1, color=CARD_BORDER),
                    ft.Row(
                        alignment="spaceBetween",
                        controls=[
                            ft.Text("Order Total", size=16, weight="bold", color=TEXT_PRIMARY),
                            order_total_text
                        ]
                    )
                ]
            )
        ),
        actions=[
            ft.TextButton("Cancel", style=ft.ButtonStyle(color=TEXT_MUTED), on_click=lambda e: setattr(new_po_dialog, 'open', False) or page.update()),
            ft.Container(
                bgcolor=ACCENT, padding=ft.Padding.symmetric(horizontal=20, vertical=10), border_radius=8,
                ink=True, on_click=create_po, content=ft.Text("Create Order", size=13, weight="bold", color=PANEL_LEFT_BG)
            )
        ]
    )

    def open_new_po_modal(e=None):
        # 1. Safely attach the dialog to the page FIRST
        if new_po_dialog not in page.overlay:
            page.overlay.append(new_po_dialog)
            
        # 2. Now it is safe to manipulate controls and run calculations
        line_items_container.controls.clear()
        add_line() # Add one initial empty line
        supplier_dropdown.value = None
        expected_date_field.value = ""
        calculate_totals()
        
        new_po_dialog.open = True
        page.update()

    def navigate_to(e, view_name):
        if view_name in ["Dashboard", "Low-Stock Items", "Purchase Orders", "Reports"]:
            render_view(view_name)
        elif global_navigate_to:
            global_navigate_to(view_name)

    def build_sidebar(active_view: str):
        user_name = user["full_name"] if user else "Juan Dela Cruz"
        user_role = user["role"] if user else "Owner / Admin"

        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10), border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT, ink=True,
                on_click=lambda e: navigate_to(e, title),
                content=ft.Text(title, size=13, color=TEXT_PRIMARY if is_active else "#CCCCCC", weight="bold" if is_active else "normal"),
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
                    expand=True, spacing=2, scroll="hidden",
                    controls=[
                        _sidebar_section_title("Overview"), _sidebar_link("Dashboard"),
                        _sidebar_section_title("Master Records"), _sidebar_link("User Management"), _sidebar_link("Suppliers"), _sidebar_link("Ingredients & Supplies"),
                        _sidebar_section_title("Operations"), _sidebar_link("Inventory Monitoring"), _sidebar_link("Low-Stock Items"), _sidebar_link("Purchase Orders"), _sidebar_link("Movement History"),
                        _sidebar_section_title("Transactions"), _sidebar_link("Receiving/ Stock-In"), _sidebar_link("Stock-Out/ Usage"), _sidebar_link("Daily Sales"),
                        _sidebar_section_title("Insights"), _sidebar_link("Reports"),
                    ]
                ),
                ft.Divider(height=20, color=CARD_BORDER),
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Row(
                            spacing=12,
                            controls=[
                                ft.CircleAvatar(bgcolor=TEXT_PRIMARY, color=PANEL_LEFT_BG, radius=18, content=ft.Icon(ft.Icons.PERSON, size=20)),
                                ft.Column(spacing=0, controls=[ft.Text(user_name, size=13, weight="bold", color=TEXT_PRIMARY), ft.Text(user_role, size=11, color=TEXT_MUTED)])
                            ]
                        ),
                        ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ACCENT, icon_size=20, tooltip="Log Out", on_click=lambda e: show_login() if show_login else None)
                    ]
                )
            ]
        )

    def render_view(view_name: str):
        sidebar_container.content = build_sidebar(view_name)
        
        if view_name == "Dashboard":
            main_content.content = AdminOverview(page)
        elif view_name == "Low-Stock Items":
            main_content.content = AdminLowStock(page, open_new_po_modal)
        elif view_name == "Purchase Orders":
            main_content.content = AdminPurchaseOrders(page, open_new_po_modal)
        elif view_name == "Reports":
            main_content.content = AdminReports(page)
            
        page.update()

    # Load default view on initialization
    render_view(initial_view)

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