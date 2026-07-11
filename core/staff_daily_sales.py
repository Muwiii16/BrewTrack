import flet as ft
from core.theme import *
from core.components import _sidebar_section_title
from models import sales_model

def staff_daily_sales_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    # --- SIDEBAR LOGIC ---
    def build_sidebar(active_view: str):
        user_name = user["full_name"] if user else "Staff Member"
        user_role = user["role"] if user else "Staff"

        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10), border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.colors.TRANSPARENT, ink=True,
                on_click=lambda e: global_navigate_to(title) if global_navigate_to else None,
                content=ft.Text(title, size=13, color=TEXT_PRIMARY if is_active else "#CCCCCC", weight="bold" if is_active else "normal"),
            )

        return ft.Container(
            width=240, bgcolor=PANEL_LEFT_BG, padding=20, border=ft.Border.only(right=ft.Border.BorderSide(1, CARD_BORDER)),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Column(spacing=2, controls=[
                        ft.Icon(ft.Icons.COFFEE, size=24, color=ACCENT),
                        ft.Text("BUT FIRST, COFFEE", size=10, weight="bold", color=ACCENT, style=ft.TextStyle(letter_spacing=1.5)),
                        ft.Text("BREWTRACK", size=22, weight="bold", color=TEXT_PRIMARY, font_family=FONT_HEADING),
                    ]),
                    ft.Divider(height=30, color=CARD_BORDER),
                    ft.Column(
                        expand=True, spacing=2, scroll=ft.ScrollMode.HIDDEN,
                        controls=[
                            _sidebar_section_title("Overview"), _sidebar_link("Dashboard"),
                            _sidebar_section_title("Operations"), _sidebar_link("Inventory Monitoring"), _sidebar_link("Low-Stock Alerts"), _sidebar_link("Movement History"),
                            _sidebar_section_title("Transactions"), _sidebar_link("Receiving/ Stock-In"), _sidebar_link("Stock-Out/ Usage"), _sidebar_link("Daily Sales"),
                        ]
                    ),
                    ft.Divider(height=20, color=CARD_BORDER),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(spacing=12, controls=[
                                ft.CircleAvatar(bgcolor=TEXT_PRIMARY, color=PANEL_LEFT_BG, radius=18, content=ft.Icon(ft.Icons.PERSON, size=20)),
                                ft.Column(spacing=0, controls=[ft.Text(user_name, size=13, weight="bold", color=TEXT_PRIMARY), ft.Text(user_role, size=11, color=TEXT_MUTED)])
                            ]),
                            ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ACCENT, icon_size=20, tooltip="Log Out", on_click=lambda e: show_login() if show_login else None)
                        ]
                    )
                ]
            )
        )

    sidebar = build_sidebar("Daily Sales")

    # --- FETCH REAL DATA FROM DB ---
    try:
        menu_items = sales_model.get_products()
    except Exception as e:
        print(f"Error fetching products: {e}")
        menu_items = []

    # Map state using 'product_id'
    order_state = {item["product_id"]: 0 for item in menu_items}
    qty_refs = {item["product_id"]: {} for item in menu_items}

    # --- DYNAMIC STAT CARDS ---
    revenue_text = ft.Text("P 0.00", size=22, color=TEXT_PRIMARY, weight="bold")
    
    def stat_card(label, value_control, sub):
        return ft.Container(
            expand=True, border=ft.Border.all(1, CARD_BORDER), border_radius=6, padding=16, 
            content=ft.Column([ft.Text(label, size=12, color=TEXT_MUTED), value_control, ft.Text(sub, size=11, color=TEXT_MUTED)], spacing=4)
        )

    stats_row = ft.Row([
        stat_card("Today's Revenue", revenue_text, "Gross sales"), 
        stat_card("Units Sold Today", ft.Text("N/A", size=22, color=TEXT_PRIMARY, weight="bold"), "Total Products"), 
        stat_card("Orders Today", ft.Text("N/A", size=22, color=TEXT_PRIMARY, weight="bold"), "Checkouts")
    ], spacing=16)

    def update_dashboard_stats():
        try:
            total = sales_model.get_daily_sales_total()
            # Handle case where total might be None if no sales exist
            total_val = float(total) if total is not None else 0.0
            revenue_text.value = f"P {total_val:,.2f}"
            page.update()
        except Exception as e:
            print(f"Error fetching sales total: {e}")

    # Fetch initial stats
    update_dashboard_stats()

    order_list_col = ft.Column(spacing=8)
    
    # Use native ElevatedButton for complete button
    complete_btn = ft.ElevatedButton(
        content=ft.Text("Complete Order", weight="bold"),
        bgcolor=ACCENT,
        color="#000000",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6), 
            padding=ft.Padding.all(16)
        ),
        disabled=True,
        width=float("inf")
    )

    def refresh_order_list():
        order_list_col.controls.clear()
        active = [(item, order_state[item["product_id"]]) for item in menu_items if order_state[item["product_id"]] > 0]
        
        if not active:
            order_list_col.controls.append(ft.Column([ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, size=32, color=TEXT_MUTED), ft.Text("Tap menu items to start.", size=12, color=TEXT_MUTED)], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
            complete_btn.disabled = True
        else:
            total_cost = 0.0
            for item, qty in active:
                price = float(item['selling_price'])
                line_total = price * qty
                total_cost += line_total
                order_list_col.controls.append(
                    ft.Container(
                        border=ft.Border.all(1, CARD_BORDER), border_radius=6, padding=12, 
                        content=ft.Row([
                            ft.Column([ft.Text(item["product_name"], size=13, weight="bold", color=TEXT_PRIMARY), ft.Text(f"{qty}x @ P{price:.2f}", size=11, color=TEXT_MUTED)], spacing=2, expand=True),
                            ft.Text(f"P{line_total:.2f}", size=13, weight="bold", color=TEXT_PRIMARY)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    )
                )
            # Optional: Add a total row at the bottom of the cart
            order_list_col.controls.append(
                ft.Container(
                    margin=ft.margin.only(top=10),
                    content=ft.Row([
                        ft.Text("Total:", size=16, weight="bold", color=TEXT_PRIMARY),
                        ft.Text(f"P{total_cost:,.2f}", size=16, weight="bold", color=ACCENT)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            )
            complete_btn.disabled = False
        page.update()

    def handle_complete(e):
        user_id = user["user_id"] if user else 1
        active_items = [(i, order_state[i["product_id"]]) for i in menu_items if order_state[i["product_id"]] > 0]
        
        if not active_items: return # Safety check
        
        for item, qty in active_items:
            try:
                sales_model.record_sale(
                    product_id=item["product_id"], 
                    quantity_sold=qty, 
                    selling_price=float(item["selling_price"]), 
                    user_id=user_id
                )
            except Exception as ex:
                print(f"Failed to record sale for {item['product_name']}: {ex}")

        # Reset states after processing
        for item in menu_items:
            pid = item["product_id"]
            order_state[pid] = 0
            qty_refs[pid]["control"].value = "0"
            
        # Modern Flet SnackBar handling
        snack = ft.SnackBar(content=ft.Text("Order completed and inventory deducted!"), bgcolor=ft.colors.GREEN_800)
        page.overlay.append(snack)
        snack.open = True
        
        refresh_order_list()
        update_dashboard_stats() 
        page.update()
        
    complete_btn.on_click = handle_complete

    def make_change(item_id, delta):
        def handler(e):
            order_state[item_id] = max(0, order_state[item_id] + delta)
            qty_refs[item_id]["control"].value = str(order_state[item_id])
            refresh_order_list()
        return handler

    # --- RENDER DYNAMIC MENU CARDS ---
    cards = []
    if not menu_items:
        cards.append(ft.Text("No active menu items found.", color=TEXT_MUTED))
    else:
        for item in menu_items:
            pid = item["product_id"]
            price = float(item["selling_price"])
            
            qty_text = ft.Text("0", size=16, weight="bold", color=TEXT_PRIMARY, text_align=ft.TextAlign.CENTER)
            qty_refs[pid]["control"] = qty_text
            
            cards.append(ft.Container(expand=True, border=ft.Border.all(1, CARD_BORDER), border_radius=8, padding=16, content=ft.Column([
                ft.Row([ft.Column([ft.Text(item["product_name"], size=15, weight="bold", color=TEXT_PRIMARY), ft.Text(f"P {price:.2f}", size=12, color=TEXT_MUTED)], spacing=2)]),
                ft.Container(height=4),
                ft.Row([
                    ft.Container(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.REMOVE_ROUNDED, size=16)]), width=32, height=32, border=ft.Border.all(1, CARD_BORDER), border_radius=6, on_click=make_change(pid, -1), ink=True),
                    ft.Container(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[qty_text]), expand=True),
                    ft.Container(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ft.Icons.ADD_ROUNDED, size=16)]), width=32, height=32, border=ft.Border.all(1, CARD_BORDER), border_radius=6, on_click=make_change(pid, 1), ink=True),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
            ], spacing=4)))

    grid_rows = []
    for idx in range(0, len(cards), 2):
        pair = cards[idx:idx + 2]
        if len(pair) == 1: 
            pair.append(ft.Container(expand=True)) # Keep grid aligned if odd number of items
        grid_rows.append(ft.Row(pair, spacing=16))

    refresh_order_list()

    main_content = ft.Container(expand=True, padding=24, content=ft.Column(scroll=ft.ScrollMode.AUTO, spacing=20, controls=[
        ft.Column([ft.Text("Daily Sales Recording", size=28, weight="bold", color=TEXT_PRIMARY), ft.Text("Ring up orders from the menu.", size=13, color=TEXT_MUTED)], spacing=6),
        stats_row,
        ft.Row(spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, controls=[
            ft.Container(expand=2, border=ft.Border.all(1, CARD_BORDER), border_radius=6, padding=16, content=ft.Column([ft.Text("Tap to Add", size=16, weight="bold", color=TEXT_PRIMARY)] + grid_rows, spacing=16)),
            ft.Container(expand=1, border=ft.Border.all(1, CARD_BORDER), border_radius=6, padding=16, content=ft.Column([ft.Text("Current Order", size=16, weight="bold", color=TEXT_PRIMARY), ft.Container(order_list_col, padding=20), complete_btn], spacing=12))
        ])
    ]))
    
    return ft.Row([sidebar, main_content], expand=True, spacing=0)