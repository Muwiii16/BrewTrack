import flet as ft
from datetime import datetime
from core.theme import *
from core.components import _sidebar_section_title
from models import inventory_model, purchase_order_model, sales_model, stock_movement_model

def staff_dashboard_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    def _border():
        return ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER))

    def build_sidebar(active_view: str):
        user_name = user["full_name"] if user else "Staff Member"
        user_role = user["role"] if user else "Staff"

        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10), border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT, ink=True,
                on_click=lambda e: global_navigate_to(title) if global_navigate_to else None,
                content=ft.Text(title, size=13, color=TEXT_PRIMARY if is_active else "#CCCCCC", weight="bold" if is_active else "normal"),
            )

        return ft.Container(
            width=240, bgcolor=PANEL_LEFT_BG, padding=20, border=ft.Border(right=ft.BorderSide(1, CARD_BORDER)),
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
                        expand=True, spacing=2, scroll="hidden",
                        controls=[
                            _sidebar_section_title("Overview"), _sidebar_link("Dashboard"),
                            _sidebar_section_title("Operations"), _sidebar_link("Inventory Monitoring"), _sidebar_link("Low-Stock Alerts"), _sidebar_link("Movement History"),
                            _sidebar_section_title("Transactions"), _sidebar_link("Receiving/ Stock-In"), _sidebar_link("Stock-Out/ Usage"), _sidebar_link("Daily Sales"),
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
        )

    sidebar = build_sidebar("Dashboard")
    user_first_name = user["full_name"].split(" ")[0] if user else "Staff"

    try:
        inventory = inventory_model.get_inventory_overview()
        low_stock = inventory_model.get_low_stock_items()
        pos = purchase_order_model.get_purchase_orders()
        sales = sales_model.get_recent_sales(limit=100)
        movements = stock_movement_model.get_recent_movements(limit=10)
    except Exception:
        inventory, low_stock, pos, sales, movements = [], [], [], [], []

    total_inv_val = sum(float(i['value'] or 0) for i in inventory)
    low_stock_count = len(low_stock)
    pending_pos_count = sum(1 for p in pos if p['po_status'] == 'Pending')
    
    today_str = datetime.now().date()
    today_sales = sum(float(s['line_total']) for s in sales if s['sales_date'].date() == today_str)

    header = ft.Column([
        ft.Row([ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_MUTED), ft.Text("Dashboard", size=14, color=TEXT_MUTED)], spacing=4),
        ft.Text(f"Good day, {user_first_name}", size=28, color=TEXT_PRIMARY, weight="bold"),
        ft.Text("Your operational tasks and stocks alert today", size=13, color=TEXT_MUTED)
    ], spacing=6)

    def _stat_card(title, value, subtitle):
        return ft.Container(
            expand=True, border=_border(), border_radius=6, padding=16,
            content=ft.Column([
                ft.Text(title, size=12, color=TEXT_MUTED),
                ft.Text(value, size=22, color=TEXT_PRIMARY, weight="bold"),
                ft.Text(subtitle, size=11, color=TEXT_MUTED)
            ], spacing=4)
        )

    stats_row = ft.Row([
        _stat_card("Inventory Value", f"P {total_inv_val:,.0f}", f"{len(inventory)} tracked items"),
        _stat_card("Low/ Out of Stock", str(low_stock_count), "Needs attention"),
        _stat_card("Pending Approval", str(pending_pos_count), f"{len([p for p in pos if p['po_status'] in ['Pending', 'Approved']])} open orders"),
        _stat_card("Sales Today", f"P {today_sales:,.0f}", f"P {sum(float(s['line_total']) for s in sales):,.0f} recent total"),
    ], spacing=16)

    def _badge(text, bg, fg):
        return ft.Container(content=ft.Text(text, size=11, weight="bold", color=fg), bgcolor=bg, padding=ft.Padding.symmetric(horizontal=10, vertical=4), border_radius=12)

    low_stock_list = ft.Column(spacing=10)
    for item in low_stock[:4]:
        qty, ro = float(item['current_quantity']), float(item['reorder_level'])
        is_out = qty <= 0
        bg, fg = ("#330000", "#ef4444") if is_out else ("#332400", ACCENT)
        low_stock_list.controls.append(ft.Container(
            border=_border(), border_radius=6, padding=12,
            content=ft.Row([
                ft.Column([
                    ft.Text(item['item_name'], size=14, color=TEXT_PRIMARY, weight="bold"),
                    ft.Text(f"{qty:g} {item['unit_of_measurement']} on hand * reorder at {ro:g}", size=11, color=TEXT_MUTED)
                ], spacing=2, expand=True),
                _badge("Out of Stock" if is_out else "Low", bg, fg)
            ], alignment="spaceBetween", vertical_alignment="center")
        ))

    movements_list = ft.Column(spacing=10)
    for m in movements[:4]:
        t = m['movement_type']
        if t == "Stock-In": bg, fg, sign = "#0f2e16", "#22c55e", "+"
        elif t == "Stock-Out": bg, fg, sign = "#330000", "#ef4444", "-"
        else: bg, fg, sign = "#082f49", "#3b82f6", "-"
        
        movements_list.controls.append(ft.Container(
            border=_border(), border_radius=6, padding=12,
            content=ft.Row([
                _badge(t, bg, fg),
                ft.Container(width=10),
                ft.Column([
                    ft.Text(f"{m['item_name']} * {m['reference_type'] or 'Manual'}", size=14, color=TEXT_PRIMARY, weight="bold"),
                    ft.Text(f"{m['full_name']} | {m['movement_date'].strftime('%b %d, %I:%M %p')}", size=11, color=TEXT_MUTED)
                ], spacing=2, expand=True),
                ft.Text(f"{sign} {float(m['quantity']):g} units", size=12, weight="bold", color=fg)
            ], vertical_alignment="center")
        ))

    incoming_row = ft.Row(spacing=16, scroll="auto", expand=True)
    for p in [x for x in pos if x['po_status'] in ['Pending', 'Approved']][:4]:
        total = sum(float(i['line_total']) for i in p.get('items', []))
        bg, fg = ("#0f2e16", "#22c55e") if p['po_status'] == 'Approved' else ("#332400", ACCENT)
        incoming_row.controls.append(ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(f"PO-{p['po_id']:04d}", size=14, weight="bold", color=TEXT_PRIMARY),
                    ft.Text(f"P {total:,.2f}", size=12, color=TEXT_MUTED)
                ], spacing=2),
                ft.Container(width=10),
                _badge(p['po_status'], bg, fg)
            ], vertical_alignment="center")
        ))

    incoming_orders_card = ft.Container(
        border=_border(), border_radius=8, padding=20,
        content=ft.Row([
            ft.Text("Incoming\nOrders", size=18, weight="bold", color=TEXT_PRIMARY),
            ft.VerticalDivider(color=CARD_BORDER, width=30),
            incoming_row,
            ft.Text("View all ➔", size=11, color=TEXT_MUTED)
        ], vertical_alignment="center")
    )

    middle_row = ft.Row([
        ft.Container(expand=1, border=_border(), border_radius=8, padding=20, content=ft.Column([
            ft.Row([ft.Text("Low-Stock Alerts", size=18, weight="bold", color=TEXT_PRIMARY), ft.Container(expand=True), ft.Text("View all ➔", size=11, color=TEXT_MUTED)]),
            ft.Container(height=10), low_stock_list
        ])),
        ft.Container(expand=1, border=_border(), border_radius=8, padding=20, content=ft.Column([
            ft.Row([ft.Text("Recent Stock Movements", size=18, weight="bold", color=TEXT_PRIMARY), ft.Container(expand=True), ft.Text("View all ➔", size=11, color=TEXT_MUTED)]),
            ft.Container(height=10), movements_list
        ]))
    ], spacing=20, vertical_alignment="start")

    main_content = ft.Container(
        content=ft.Column([header, stats_row, middle_row, incoming_orders_card], spacing=20, scroll="auto"),
        expand=True, padding=24
    )

    return ft.Row([sidebar, main_content], expand=True, spacing=0)