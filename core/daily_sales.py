import flet as ft
from core.theme import *
from core.components import _summary_card, _sidebar_section_title
from models import sales_model
from datetime import datetime

def DailySales(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    
    # --- SIDEBAR CONFIGURATION ---
    sidebar_container = ft.Container(
        width=240, bgcolor=PANEL_LEFT_BG, padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )
    
    main_content = ft.Container(expand=True, padding=40, bgcolor=BG_COLOR)

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
                ft.Column(spacing=2, controls=[
                    ft.Icon(ft.Icons.COFFEE, size=24, color=ACCENT),
                    ft.Text("BUT FIRST, COFFEE", size=10, weight="bold", color=ACCENT, style=ft.TextStyle(letter_spacing=1.5)),
                    ft.Text("BREWTRACK", size=22, weight="bold", color=TEXT_PRIMARY, font_family=FONT_HEADING),
                ]),
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
                        ft.Row(spacing=12, controls=[
                            ft.CircleAvatar(bgcolor=TEXT_PRIMARY, color=PANEL_LEFT_BG, radius=18, content=ft.Icon(ft.Icons.PERSON, size=20)),
                            ft.Column(spacing=0, controls=[ft.Text(user_name, size=13, weight="bold", color=TEXT_PRIMARY), ft.Text(user_role, size=11, color=TEXT_MUTED)])
                        ]),
                        ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ACCENT, icon_size=20, tooltip="Log Out", on_click=lambda e: show_login() if show_login else None)
                    ]
                )
            ]
        )

    try:
        raw_sales_data = sales_model.get_recent_sales(limit=100)
    except Exception:
        raw_sales_data = []

    today_str = datetime.now().date()
    today_sales = [s for s in raw_sales_data if s['sales_date'].date() == today_str]
    today_revenue = sum(float(s['line_total']) for s in today_sales)
    today_units = sum(int(s['quantity_sold']) for s in today_sales)
    
    stats_row = ft.Row(
        spacing=20,
        controls=[
            _summary_card("Today's Revenue", f"P {today_revenue:,.2f}"),
            _summary_card("Units Sold Today", str(today_units)),
            _summary_card("Transactions Today", str(len(today_sales))),
        ]
    )

    state = {"selected_id": None, "queue": []}
    for i, s in enumerate(raw_sales_data[:15]): 
        state["queue"].append({
            "id": f"SO-{1008 + i}", "product_name": s['product_name'], "qty": s['quantity_sold'],
            "total": float(s['line_total']), "date": s['sales_date'].strftime("%b %d, %I:%M %p"), "cashier": s['full_name']
        })

    left_panel_content = ft.Column(spacing=10, scroll="auto")
    right_panel_content = ft.Column(spacing=15)
    
    def select_order(order_id):
        state["selected_id"] = order_id
        refresh_panels()

    def verify_order(e):
        state["queue"] = [order for order in state["queue"] if order["id"] != state["selected_id"]]
        state["selected_id"] = None
        snack = ft.SnackBar(content=ft.Text("Sales Order Verified Successfully!"), bgcolor=ft.Colors.GREEN_800)
        page.overlay.append(snack)
        snack.open = True
        refresh_panels()

    def refresh_panels():
        left_panel_content.controls.clear()
        if not state["queue"]:
            left_panel_content.controls.append(ft.Container(padding=20, content=ft.Text("No pending sales orders.", color=TEXT_MUTED)))
            
        for order in state["queue"]:
            is_selected = (state["selected_id"] == order["id"])
            card = ft.Container(
                padding=15, border_radius=8, bgcolor="#1A1A1A" if not is_selected else "#2A2A2A",
                border=ft.Border(top=ft.BorderSide(1, ACCENT if is_selected else CARD_BORDER), bottom=ft.BorderSide(1, ACCENT if is_selected else CARD_BORDER), left=ft.BorderSide(1, ACCENT if is_selected else CARD_BORDER), right=ft.BorderSide(1, ACCENT if is_selected else CARD_BORDER)),
                ink=True, on_click=lambda e, oid=order["id"]: select_order(oid),
                content=ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Column(spacing=4, controls=[ft.Text(order["id"], size=16, weight="bold", color=TEXT_PRIMARY), ft.Text(f"Purchased {order['date']}", size=11, color=TEXT_MUTED)]),
                        ft.Container(padding=8, border_radius=16, border=ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER)), content=ft.Text(f"{order['qty']} Order/s", size=11, color=TEXT_MUTED))
                    ]
                )
            )
            left_panel_content.controls.append(card)

        right_panel_content.controls.clear()
        selected_order = next((o for o in state["queue"] if o["id"] == state["selected_id"]), None)
        
        if not selected_order:
            right_panel_content.controls.append(ft.Container(expand=True, alignment=ft.Alignment.CENTER, padding=40, content=ft.Text("Select an order to verify.", color=TEXT_MUTED)))
        else:
            right_panel_content.controls.extend([
                ft.Text("Verify", size=20, weight="bold", color=TEXT_PRIMARY),
                ft.Container(
                    padding=20, border_radius=8, border=ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER)),
                    content=ft.Row(alignment="spaceBetween", controls=[ft.Column(spacing=4, controls=[ft.Text(selected_order["product_name"], size=16, weight="bold", color=TEXT_PRIMARY), ft.Text(f"x{selected_order['qty']}  |  Logged by {selected_order['cashier']}", size=13, color=TEXT_MUTED)]), ft.Text(f"P {selected_order['total']:,.2f}", size=16, weight="bold", color=TEXT_PRIMARY)])
                ),
                ft.Container(expand=True), 
                ft.ElevatedButton(content=ft.Text("Verify Sales Order", weight="bold"), bgcolor=ACCENT, color=PANEL_LEFT_BG, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6), padding=15), width=float("inf"), on_click=verify_order)
            ])
        page.update()

    left_card = ft.Container(expand=1, border=ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER)), border_radius=8, padding=24, content=ft.Column(expand=True, spacing=15, controls=[ft.Text("Recent Sales Orders", size=18, weight="bold", color=TEXT_PRIMARY), left_panel_content]))
    right_card = ft.Container(expand=1, border=ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER)), border_radius=8, padding=24, content=right_panel_content)
    refresh_panels()

    main_content = ft.Container(
        expand=True, padding=40, bgcolor=BG_COLOR,
        content=ft.Column(
            expand=True, spacing=25,
            controls=[
                ft.Column(spacing=4, controls=[ft.Text("Daily Sales Recording", size=28, weight="bold", color=TEXT_PRIMARY), ft.Text("Verify recent sales orders logged by staff.", size=12, color=TEXT_MUTED)]),
                stats_row,
                ft.Row(expand=True, vertical_alignment="start", spacing=20, controls=[left_card, right_card])
            ]
        )
    )
    sidebar_container.content = build_sidebar("Daily Sales")
    return ft.Row(expand=True, spacing=0, controls=[sidebar_container, main_content])