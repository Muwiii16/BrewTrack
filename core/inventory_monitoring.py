import flet as ft
from core.theme import *
from core.components import _sidebar_section_title, _summary_card, _badge, _cell
from models import inventory_model, purchase_order_model
from datetime import datetime, timedelta

def inventory_monitoring_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    
    sidebar_container = ft.Container(
        width=240, bgcolor=PANEL_LEFT_BG, padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )
    
    main_content = ft.Container(expand=True, padding=40, bgcolor=BG_COLOR)

    # --- Quick PO Modal Setup ---
    selected_item_for_po = {}
    
    po_supplier_display = ft.TextField(label="Assigned Supplier", read_only=True, bgcolor=INPUT_BG, border_color=CARD_BORDER, text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13), label_style=ft.TextStyle(color=TEXT_MUTED))
    po_qty_input = ft.TextField(label="Quantity to Order", keyboard_type=ft.KeyboardType.NUMBER, bgcolor=INPUT_BG, border_color=CARD_BORDER, text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13), label_style=ft.TextStyle(color=TEXT_MUTED))
    
    po_expected_date_display = ft.Text(size=13, color=TEXT_PRIMARY, weight="bold")
    po_unit_cost_display = ft.Text(size=13, color=TEXT_PRIMARY)
    po_total_display = ft.Text("Total: ₱ 0.00", size=16, weight="bold", color=ACCENT)

    def update_po_total(e):
        try:
            qty = float(po_qty_input.value)
            cost = float(selected_item_for_po.get("cost_per_unit", 0))
            po_total_display.value = f"Total: ₱ {qty * cost:,.2f}"
        except ValueError:
            po_total_display.value = "Total: ₱ 0.00"
        page.update()

    po_qty_input.on_change = update_po_total

    def close_quick_po(e):
        page.close(quick_po_modal)
        
    def submit_quick_po(e):
        if not po_qty_input.value: return
        try:
            qty = float(po_qty_input.value)
        except ValueError:
            return
            
        supplier_id = selected_item_for_po.get("supplier_id")
        if not supplier_id:
            page.open(ft.SnackBar(ft.Text("Cannot create PO: No supplier assigned to this item!"), bgcolor=ft.Colors.RED_800))
            return
            
        # Format the date for the database (YYYY-MM-DD)
        expected_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        line_items = [{
            "item_id": selected_item_for_po["item_id"],
            "qty": qty,
            "unit_cost": selected_item_for_po["cost_per_unit"]
        }]
        
        # Create the purchase order using the logged-in user
        uid = user["user_id"] if user else 1
        purchase_order_model.create_purchase_order(supplier_id, uid, expected_date, line_items)
        
        page.close(quick_po_modal)
        page.open(ft.SnackBar(ft.Text(f"Purchase Order created for {selected_item_for_po['item_name']}!"), bgcolor=ft.Colors.GREEN_800))
        load_data()  # Refresh the table stats

    quick_po_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("New Purchase Order", size=20, weight="bold", color=TEXT_PRIMARY),
        content=ft.Container(
            width=350,
            content=ft.Column(
                tight=True,  # This prevents the modal from stretching vertically
                spacing=15,
                controls=[
                    po_supplier_display,
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Expected Date:", size=13, color=TEXT_MUTED), po_expected_date_display]),
                    ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Unit Cost:", size=13, color=TEXT_MUTED), po_unit_cost_display]),
                    po_qty_input,
                    ft.Divider(color=CARD_BORDER),
                    po_total_display
                ]
            )
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_quick_po, style=ft.ButtonStyle(color=TEXT_MUTED)),
            ft.ElevatedButton("Confirm Order", bgcolor=ACCENT, color=PANEL_LEFT_BG, on_click=submit_quick_po)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=PANEL_RIGHT_BG,
        shape=ft.RoundedRectangleBorder(radius=8)
    )

    def open_quick_po(e, item):
        selected_item_for_po.clear()
        selected_item_for_po.update(item)
        quick_po_modal.title.value = f"New PO: {item['item_name']}"
        po_supplier_display.value = item["supplier_name"] or "No Supplier Assigned"
        po_qty_input.value = ""
        
        # Display the expected date in mm-dd-yyyy format
        exp_date = datetime.now() + timedelta(days=3)
        po_expected_date_display.value = exp_date.strftime("%m-%d-%Y")
        
        # Display Unit Cost and Reset Total
        cost = float(item.get("cost_per_unit", 0))
        po_unit_cost_display.value = f"₱ {cost:,.2f}"
        po_total_display.value = "Total: ₱ 0.00"
        
        page.open(quick_po_modal)
    # ----------------------------

    def navigate_to(e, view_name):
        if global_navigate_to:
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

    sidebar_container.content = build_sidebar("Inventory Monitoring")

    # --- Search + Column Filtering Setup ---
    all_items_cache = []
    filters = {"search": "", "category": "All", "supplier": "All", "status": "All"}
    filter_state = {}

    def compute_status(i):
        qty = float(i["current_quantity"])
        rl = float(i["reorder_level"]) if i["reorder_level"] else 0
        if qty <= 0:
            return "Out of Stock"
        elif qty <= rl:
            return "Low"
        else:
            return "In Stock"

    def set_filter(key, value):
        filters[key] = value
        state = filter_state[key]
        if value == "All":
            state["text_ctrl"].value = state["label"]
            state["text_ctrl"].color = TEXT_MUTED
            state["icon_ctrl"].color = TEXT_MUTED
        else:
            state["text_ctrl"].value = f"{state['label']}: {value}"
            state["text_ctrl"].color = ACCENT
            state["icon_ctrl"].color = ACCENT
        apply_and_render()

    def make_filter_column(label, filter_key):
        text_ctrl = ft.Text(label, color=TEXT_MUTED, weight="bold", size=13)
        icon_ctrl = ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=TEXT_MUTED, size=16)

        def build_items():
            if filter_key == "status":
                values = ["All", "In Stock", "Low", "Out of Stock"]
            elif filter_key == "category":
                values = ["All"] + sorted({(i.get("category") or "-") for i in all_items_cache})
            else:  # supplier
                values = ["All"] + sorted({(i["supplier_name"] or "-") for i in all_items_cache})
            return [
                ft.PopupMenuItem(content=v, on_click=lambda e, val=v: set_filter(filter_key, val))
                for v in values
            ]

        btn = ft.PopupMenuButton(
            tooltip=f"Filter by {label}",
            content=ft.Row(spacing=2, vertical_alignment="center", controls=[text_ctrl, icon_ctrl]),
            items=[]
        )
        filter_state[filter_key] = {"label": label, "btn": btn, "text_ctrl": text_ctrl, "icon_ctrl": icon_ctrl, "build_items": build_items}
        return ft.DataColumn(btn)

    def refresh_filter_menus():
        for state in filter_state.values():
            state["btn"].items = state["build_items"]()

    def matches_filters(i):
        if filters["category"] != "All" and (i.get("category") or "-") != filters["category"]:
            return False
        if filters["supplier"] != "All" and (i["supplier_name"] or "-") != filters["supplier"]:
            return False
        if filters["status"] != "All" and compute_status(i) != filters["status"]:
            return False
        if filters["search"]:
            q = filters["search"].strip().lower()
            haystack = f"{i['item_name']} {i.get('category') or ''} {i['supplier_name'] or ''}".lower()
            if q not in haystack:
                return False
        return True

    def apply_and_render():
        filtered = [i for i in all_items_cache if matches_filters(i)]
        render_rows(filtered)

    def on_search_change(e):
        filters["search"] = e.control.value or ""
        apply_and_render()
    # ----------------------------------------

    # Removed numeric=True to prevent header/cell visual misalignment quirk in Flet
    data_table = ft.DataTable(
        column_spacing=30,
        columns=[
            ft.DataColumn(ft.Text("Item Name", color=TEXT_MUTED, weight="bold")),
            make_filter_column("Category", "category"),
            make_filter_column("Supplier", "supplier"),
            ft.DataColumn(ft.Text("Current Stock", color=TEXT_MUTED, weight="bold")),
            ft.DataColumn(ft.Text("Value", color=TEXT_MUTED, weight="bold")),
            make_filter_column("Status", "status"),
            ft.DataColumn(ft.Text("Orders", color=TEXT_MUTED, weight="bold")),
            ft.DataColumn(ft.Text("Action", color=TEXT_MUTED, weight="bold")),
        ],
        heading_row_color=ft.Colors.TRANSPARENT,
        divider_thickness=1,
        border=ft.Border(
            top=ft.BorderSide(1, CARD_BORDER),
            bottom=ft.BorderSide(1, CARD_BORDER),
            left=ft.BorderSide(1, CARD_BORDER),
            right=ft.BorderSide(1, CARD_BORDER)
        ),
        border_radius=8,
    )

    stats_row = ft.Row(spacing=20, controls=[])

    def build_data_row(i):
        qty = float(i["current_quantity"])
        val = float(i["value"] or 0)
        uom = i["unit_of_measurement"]
        label = compute_status(i)

        if label == "Out of Stock":
            bg, txt = "#330000", "#F44336"
        elif label == "Low":
            bg, txt = "#332400", ACCENT
        else:
            bg, txt = "#0f2e16", "#22c55e"

        status_badge = _badge(label, bg, txt)
        qty_color = txt if label != "In Stock" else TEXT_PRIMARY

        pending_count = i.get("pending_po_count", 0)
        orders_text = "no pending PO" if pending_count == 0 else f"{pending_count} pending"
        orders_color = TEXT_MUTED if pending_count == 0 else ACCENT

        action_btn = ft.ElevatedButton(
            "New PO",
            bgcolor=ACCENT,
            color=PANEL_LEFT_BG,
            height=30,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6), padding=ft.Padding.symmetric(horizontal=12)),
            on_click=lambda e, itm=i: open_quick_po(e, itm)
        )

        # Disable the button if there isn't a supplier linked to this item
        if not i.get("supplier_id"):
            action_btn.disabled = True
            action_btn.tooltip = "No assigned supplier"

        return ft.DataRow(cells=[
            _cell(i["item_name"], is_bold=True),
            _cell(i.get("category", "-")),
            _cell(i["supplier_name"] or "-"),
            _cell(f"{qty:g} {uom}", is_bold=True, text_color=qty_color),
            _cell(f"₱ {val:,.2f}"),
            ft.DataCell(status_badge),
            _cell(orders_text, text_color=orders_color, is_bold=(pending_count > 0)),
            ft.DataCell(action_btn)
        ])

    def render_rows(items):
        data_table.rows.clear()
        for i in items:
            data_table.rows.append(build_data_row(i))
        page.update()

    def load_data():
        try:
            items = inventory_model.get_inventory_overview() or []
        except Exception:
            items = []

        all_items_cache.clear()
        all_items_cache.extend(items)

        total_items = len(items)
        low_stock = sum(1 for i in items if compute_status(i) != "In Stock")
        total_val = sum(float(i["value"] or 0) for i in items)

        stats_row.controls.clear()
        stats_row.controls.extend([
            _summary_card("Total Items Tracked", str(total_items)),
            _summary_card("Low Stock Alerts", str(low_stock)),
            _summary_card("Total Inventory Value", f"₱ {total_val:,.2f}"),
        ])

        refresh_filter_menus()
        apply_and_render()

    load_data()

    main_content.content = ft.Column(
        expand=True, scroll="auto", spacing=30,
        controls=[
            ft.Column(spacing=4, controls=[
                ft.Row(spacing=8, controls=[ft.Icon(ft.Icons.INVENTORY_2, size=20, color=TEXT_MUTED), ft.Text("Inventory Monitoring", size=14, color=TEXT_MUTED, weight="bold")]),
                ft.Container(height=10),
                ft.Text("Inventory Monitoring", size=28, weight="bold", color=TEXT_PRIMARY),
                ft.Text("Live view of stock levels across all tracked items", size=12, color=TEXT_MUTED),
            ]),
            stats_row,
            ft.TextField(hint_text="Search by item name, category, or supplier", prefix_icon=ft.Icons.SEARCH, bgcolor=INPUT_BG, border_color=ft.Colors.TRANSPARENT, border_radius=8, height=40, width=350, text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13), hint_style=ft.TextStyle(color=TEXT_MUTED, size=13), content_padding=ft.Padding.symmetric(horizontal=14, vertical=10), on_change=on_search_change),
            # Wrap the data_table in an auto-scrolling Row to handle horizontal overflow
            ft.Container(
                expand=True, 
                content=ft.Column(
                    scroll="auto", 
                    controls=[
                        ft.Row(scroll="auto", controls=[data_table])
                    ]
                )
            )
        ]
    )

    return ft.Container(
        expand=True,
        bgcolor=BG_COLOR,
        content=ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar_container,
                main_content
            ]
        )
    )