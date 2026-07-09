import flet as ft
from core.theme import *
from models import purchase_order_model
from models import supplier_model
from models import ingredient_model

# ==========================================
# UTILITIES & DATE FORMATTER
# ==========================================
def format_date(d):
    if not d: 
        return "N/A"
    try:
        return d.strftime("%b %d, %Y")
    except AttributeError:
        return str(d)[:10]

def _money_fmt(v):
    try:
        return f"P {float(v):,.2f}"
    except (TypeError, ValueError):
        return "P 0.00"

STATUS_MAP = {
    "pending": STATUS_LOW, 
    "approved": STATUS_GREEN, 
    "received": STATUS_GREEN, 
    "cancelled": STATUS_RED
}

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
# UI COMPONENTS (Summary & List Item)
# ==========================================
def _po_summary_card_small(title, value):
    return ft.Container(
        content=ft.Column([
            ft.Text(title, size=12, color=TEXT_SECONDARY),
            ft.Text(value, size=22, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        ], spacing=6),
        border=ft.Border.all(1, BORDER_COLOR), border_radius=6, padding=16, expand=True,
    )

def _po_list_item(po_num, status, supplier, date_created, expected_date, amount, items_count, chips, on_approve, on_cancel):
    status_bg = STATUS_MAP.get(status.lower(), STATUS_LOW)
    
    if status.lower() == "pending":
        menu_items = [
            ft.PopupMenuItem(text="Approve", on_click=on_approve),
            ft.PopupMenuItem(text="Cancel Order", on_click=on_cancel),
        ]
    else:
        menu_items = [ft.PopupMenuItem(text="No actions available", disabled=True)]

    chip_widgets = [
        ft.Container(
            content=ft.Text(c, size=12, color=TEXT_PRIMARY),
            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            border=ft.Border.all(1, BORDER_COLOR), border_radius=8,
        ) for c in chips
    ]

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Row([
                    ft.Text(po_num, size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                    ft.Container(
                        ft.Text(status, size=12, weight=ft.FontWeight.BOLD, color="#000000"),
                        bgcolor=status_bg, padding=ft.Padding.symmetric(horizontal=10, vertical=4), border_radius=20
                    ),
                ], spacing=10),
                ft.Row([
                    ft.Column([
                        ft.Text(amount, size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text(f"{items_count} line item(s)", size=12, color=TEXT_SECONDARY),
                    ], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=0),
                    ft.PopupMenuButton(icon=ft.Icons.MORE_HORIZ, items=menu_items),
                ], spacing=4),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text(f"{supplier} | Created {date_created} | Expected: {expected_date}", size=12, color=TEXT_SECONDARY),
            ft.Row(chip_widgets, wrap=True, spacing=10, run_spacing=10),
        ], spacing=10),
        border=ft.Border.all(1, BORDER_COLOR), border_radius=6, padding=16,
    )

# ==========================================
# CREATE PO DIALOG
# ==========================================
def open_new_po_dialog(page: ft.Page, user, on_created=None):
    """
    Standalone function to create and open the New PO Modal overlay.
    Matches the updated dark-theme design.
    """
    suppliers = supplier_model.get_suppliers()
    ingredients = ingredient_model.get_ingredients()

    # Form Fields
    supplier_dd = ft.Dropdown(
        hint_text="Select Supplier", 
        expand=True,
        border_radius=8,
        bgcolor=INPUT_BG, 
        border_color=BORDER_COLOR,
        options=[ft.dropdown.Option(str(s["supplier_id"]), s["supplier_name"]) for s in suppliers]
    )
    
    expected_date = ft.TextField(
        hint_text="dd/mm/yy", 
        expand=True,
        border_radius=8,
        bgcolor=INPUT_BG,
        border_color=BORDER_COLOR,
        suffix_icon=ft.Icons.CALENDAR_TODAY_OUTLINED
    )

    lines_col = ft.Column(spacing=10)
    error = ft.Text("", color=STATUS_RED, size=12)
    total_text = ft.Text("P 0.00", size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)
    
    # Store tuples of: (item_dd, qty_field, line_data_dict, line_total_text)
    line_widgets = [] 

    def recompute_total(e=None):
        total = 0
        for item_dd, qty_field, line_data, line_total_text in line_widgets:
            row_total = 0.0
            if item_dd.value and qty_field.value:
                try:
                    qty = float(qty_field.value)
                    cost = line_data["unit_cost"]
                    row_total = qty * cost
                    total += row_total
                except ValueError:
                    pass
            line_total_text.value = _money_fmt(row_total)
            
        total_text.value = _money_fmt(total)
        page.update()

    def add_line(e=None):
        # We store the cost invisibly here to calculate the row total
        line_data = {"unit_cost": 0.0}
        
        item_dd = ft.Dropdown(
            hint_text="Choose supplier list", 
            expand=3,
            border_radius=8,
            bgcolor=INPUT_BG,
            border_color=BORDER_COLOR,
            options=[ft.dropdown.Option(str(i["item_id"]), i["item_name"]) for i in ingredients]
        )
        qty_field = ft.TextField(
            hint_text="Qty", 
            expand=1,
            border_radius=8,
            bgcolor=INPUT_BG,
            border_color=BORDER_COLOR,
            on_change=recompute_total
        )
        line_total_text = ft.Text("P 0.00", weight=ft.FontWeight.BOLD, size=16, color=TEXT_PRIMARY)

        def set_default_cost(ev):
            match = next((i for i in ingredients if str(i["item_id"]) == item_dd.value), None)
            if match: 
                line_data["unit_cost"] = float(match["cost_per_unit"])
            recompute_total()

        item_dd.on_change = set_default_cost

        def remove_line(ev, row_to_remove=None):
            lines_col.controls.remove(row_to_remove)
            line_widgets.remove((item_dd, qty_field, line_data, line_total_text))
            recompute_total()

        delete_btn = ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=STATUS_RED)
        
        row = ft.Row([
            item_dd, 
            qty_field, 
            ft.Container(line_total_text, alignment=ft.Alignment.CENTER_RIGHT, width=100),
            delete_btn
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        delete_btn.on_click = lambda ev, r=row: remove_line(ev, r)
        
        lines_col.controls.append(row)
        line_widgets.append((item_dd, qty_field, line_data, line_total_text))
        page.update()

    # Initialize with one empty row
    add_line()

    def close_dialog(e=None):
        dialog.open = False
        if dialog in page.overlay:
            page.overlay.remove(dialog)
        page.update()

    def save(e):
        try:
            if not supplier_dd.value:
                error.value = "Please select a supplier."
                page.update()
                return
            
            line_items = [
                {"item_id": int(i.value), "qty": float(q.value), "unit_cost": d["unit_cost"]}
                for i, q, d, _ in line_widgets if i.value and q.value
            ]
            if not line_items:
                error.value = "Add at least one line item with quantity."
                page.update()
                return
                
            purchase_order_model.create_purchase_order(int(supplier_dd.value), user["user_id"], expected_date.value or None, line_items)
            close_dialog()
            if on_created: 
                on_created()
        except Exception as ex:
            error.value = str(ex)
            page.update()

    # Dialog UI Assembly
    
    dialog = ft.AlertDialog(
        modal=True,
        bgcolor="#212121", 
        shape=ft.RoundedRectangleBorder(radius=12),
        content_padding=0, 
        content=ft.Container(
            width=700,
            height=500,
            padding=30, # Simplified Flet attribute
            content=ft.Column([
                # Header
                ft.Text("New Purchase Order", size=32, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Text("Order stock from a supplier. Costs default to each item's unit cost", size=14, color=TEXT_SECONDARY),
                ft.Container(height=20),
                
                # Supplier & Date Row
                ft.Row([
                    ft.Column([
                        ft.Text("Supplier", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        supplier_dd
                    ], expand=True),
                    ft.Container(width=20), # Spacer
                    ft.Column([
                        ft.Text("Expected Date", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        expected_date
                    ], expand=True),
                ]),
                
                ft.Container(height=20),
                
                # Line Items Header
                ft.Text("Line Items", size=22, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                lines_col,
                
                # Add Line Button
                ft.Container(
                    content=ft.ElevatedButton(
                        "+ Add Line", 
                        bgcolor="#2C2C2C", 
                        color=TEXT_SECONDARY,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        on_click=add_line
                    ),
                    alignment=ft.Alignment.CENTER_LEFT,
                    margin=ft.Margin.only(top=10, bottom=10) # Fixed lowercase margin attribute
                ),
                
                # Order Total Box
                ft.Container(
                    content=ft.Row([
                        ft.Text("Order Total", size=18, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        total_text
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor="#1A1A1A", # Darker inset background
                    padding=20, # Simplified Flet attribute
                    border_radius=8,
                    margin=ft.Margin.only(top=10) # Fixed lowercase margin attribute
                ),
                error,
            ], spacing=0, scroll=ft.ScrollMode.AUTO, tight=True)
        ),
        actions_padding=ft.Padding.only(bottom=30, right=30), # Fixed lowercase padding attribute
        actions=[
            ft.ElevatedButton(
                "Cancel", 
                bgcolor="#2C2C2C", 
                color=TEXT_PRIMARY, 
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                on_click=close_dialog
            ),
            ft.ElevatedButton(
                "Create Order", 
                bgcolor=ACCENT_GOLD, 
                color="#000000", 
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                on_click=save
            ),
        ],
    )
    
    page.overlay.append(dialog)
    dialog.open = True
    page.update()

# ==========================================
# MAIN VIEW
# ==========================================
def purchase_order_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Purchase Orders", on_nav)

    # Main container that holds dynamic content
    main_container = ft.Column(expand=True, scroll="auto", spacing=30)
    
    # --- Action Handlers ---
    def handle_approve(po_id):
        purchase_order_model.approve_po(po_id)
        snack = ft.SnackBar(content=ft.Text(f"Purchase Order PO-{po_id:04d} Approved!"), bgcolor=ft.colors.GREEN_800)
        page.overlay.append(snack)
        snack.open = True
        load_data() 
        
    def handle_cancel(po_id):
        purchase_order_model.cancel_po(po_id)
        snack = ft.SnackBar(content=ft.Text(f"Purchase Order PO-{po_id:04d} Cancelled."), bgcolor=ft.colors.RED_800)
        page.overlay.append(snack)
        snack.open = True
        load_data() 

    # --- Dynamic UI Loader ---
    def load_data():
        main_container.controls.clear() 
        all_pos = purchase_order_model.get_purchase_orders()
        
        # Metrics
        open_count = sum(1 for po in all_pos if po['po_status'] in ['Pending', 'Approved'])
        pending_count = sum(1 for po in all_pos if po['po_status'] == 'Pending')
        approved_count = sum(1 for po in all_pos if po['po_status'] == 'Approved')
        received_count = sum(1 for po in all_pos if po['po_status'] == 'Received')

        action_bar = ft.Row(
            alignment="spaceBetween",
            controls=[
                ft.TextField(
                    hint_text="Search",
                    hint_style=ft.TextStyle(color=TEXT_SECONDARY, size=13),
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
                    bgcolor=ACCENT_GOLD,
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                    ink=True,
                    on_click=lambda e: open_new_po_dialog(page, user, on_created=load_data),
                    content=ft.Text(
                        "New Purchase Order",
                        size=13,
                        weight="bold",
                        color="#000000", 
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
                    content=ft.Text("No Purchase Orders found. Create a new one to get started.", color=TEXT_SECONDARY)
                )
            )
        else:
            for po in all_pos:
                items = po.get('items', [])
                total_amount = sum(float(i['line_total']) for i in items)
                items_count = len(items)
                
                chips = [
                    f"{i['item_name']} * {float(i['ordered_quantity']):g} * P{float(i['unit_cost']):,.2f}"
                    for i in items
                ]
                    
                po_list_controls.append(
                    _po_list_item(
                        po_num=f"PO-{po['po_id']:04d}",
                        status=po['po_status'],
                        supplier=po['supplier_name'] or "Unknown",
                        date_created=format_date(po['po_date']),
                        expected_date=format_date(po['expected_delivery_date']),
                        amount=f"P {total_amount:,.2f}",
                        items_count=str(items_count),
                        chips=chips,
                        on_approve=lambda e, pid=po['po_id']: handle_approve(pid),
                        on_cancel=lambda e, pid=po['po_id']: handle_cancel(pid)
                    )
                )

        main_container.controls.extend([
            ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.RECEIPT_LONG, size=20, color=TEXT_SECONDARY),
                            ft.Text("Purchase Order", size=14, color=TEXT_SECONDARY, weight="bold")
                        ]
                    ),
                    ft.Container(height=10),
                    ft.Text("Purchase Order", size=28, weight="bold", color=TEXT_PRIMARY),
                    ft.Text("Raise and track orders to your suppliers", size=12, color=TEXT_SECONDARY),
                ]
            ),
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
            ft.Column(
                spacing=15,
                controls=po_list_controls
            )
        ])
        page.update()

    # Trigger the first data load when the view is initialized
    load_data()
    
    content_area = ft.Container(
        content=main_container,
        expand=True,
        padding=24,
    )
    
    return ft.Row([sidebar, content_area], expand=True, spacing=0)