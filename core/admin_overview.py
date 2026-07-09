import flet as ft
from core.theme import *
from core.components import _summary_card, _low_stock_row, _movement_row
from models import inventory_model, purchase_order_model, sales_model, stock_movement_model
from datetime import datetime

def AdminOverview(page: ft.Page):
    def _border():
        return ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER))

    def _safe_float(val):
        try: return float(val) if val is not None else 0.0
        except: return 0.0

    # --- 1. FETCH DATA ---
    try:
        inventory = inventory_model.get_inventory_overview() or []
        pending_pos = purchase_order_model.get_purchase_orders() or []
        sales = sales_model.get_recent_sales(limit=100) or []
        movements = stock_movement_model.get_recent_movements(limit=6) or []
    except Exception:
        inventory, pending_pos, sales, movements = [], [], [], []

    # --- 2. CALCULATE STATS SAFELY ---
    low_stock_items = [i for i in inventory if _safe_float(i.get('current_quantity')) <= _safe_float(i.get('reorder_level')) and _safe_float(i.get('current_quantity')) > 0]
    out_of_stock_items = [i for i in inventory if _safe_float(i.get('current_quantity')) <= 0]
    total_attention = len(low_stock_items) + len(out_of_stock_items)
    
    pending_count = sum(1 for po in pending_pos if po.get('po_status') == 'Pending')
    
    today_str = datetime.now().date()
    today_sales = []
    for s in sales:
        try:
            s_date = s.get('sales_date')
            if isinstance(s_date, str):
                s_date = datetime.fromisoformat(s_date)
            if s_date and s_date.date() == today_str:
                today_sales.append(s)
        except: pass
        
    today_revenue = sum(_safe_float(s.get('line_total')) for s in today_sales)
    total_inv_value = sum(_safe_float(i.get('value')) for i in inventory)

    # --- 3. BUILD UI COMPONENTS ---
    cards_row = ft.Row(
        spacing=20,
        controls=[
            _summary_card("Inventory Value", f"P {total_inv_value:,.2f}", f"{len(inventory)} tracked items"),
            _summary_card("Low/ Out of Stock", str(total_attention), "Needs attention"),
            _summary_card("Pending Approval", str(pending_count), f"{pending_count} open orders"),
            _summary_card("Sales Today", f"P {today_revenue:,.2f}", f"{len(today_sales)} recent total")
        ]
    )

    # Low Stock List
    low_stock_list = []
    attention_items = out_of_stock_items + low_stock_items
    for item in attention_items[:6]:
        qty = _safe_float(item.get('current_quantity'))
        uom = item.get('unit_of_measurement', '')
        ro = _safe_float(item.get('reorder_level'))
        desc = f"{qty:g} {uom} on hand * reorder at {ro:g}"
        low_stock_list.append(_low_stock_row(item.get('item_name', 'Unknown'), desc))
        
    if not low_stock_list:
        low_stock_list.append(ft.Container(padding=20, content=ft.Text("All inventory levels are healthy! ✅", color=TEXT_MUTED)))

    low_stock_panel = ft.Container(
        expand=1, border=_border(), border_radius=8, padding=20,
        content=ft.Column(spacing=15, controls=[
            ft.Row(alignment="spaceBetween", controls=[
                ft.Text("Low-Stock Alerts", size=18, weight="bold", color=TEXT_PRIMARY),
                ft.Row(spacing=4, controls=[ft.Text("View all", size=11, color=TEXT_MUTED), ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=TEXT_MUTED)])
            ]),
            ft.Column(spacing=10, controls=low_stock_list)
        ])
    )

    # Movements List
    mov_list = []
    for mov in movements:
        m_type = mov.get('movement_type', '')
        qty_val = _safe_float(mov.get('quantity'))
        
        if m_type == "Stock-In":
            bg, fg = "#0A290A", "#4CAF50"
            qty = f"+ {qty_val:g} units"
        elif m_type == "Sale":
            bg, fg = "#002b2b", "#00BCD4"
            qty = f"- {qty_val:g} units"
        else: # Stock-Out
            bg, fg = "#332400", ACCENT
            qty = f"- {qty_val:g} units"
            
        try:
            m_date = mov.get('movement_date')
            if isinstance(m_date, str):
                m_date = datetime.fromisoformat(m_date)
            date_str = m_date.strftime('%b %d, %I:%M %p') if m_date else ""
        except:
            date_str = ""

        desc = f"{mov.get('full_name', 'System')} | {date_str}"
        mov_list.append(_movement_row(m_type, bg, fg, f"{mov.get('item_name', 'Unknown')}", desc, qty, fg))

    if not mov_list:
        mov_list.append(ft.Container(padding=20, content=ft.Text("No recent movements found.", color=TEXT_MUTED)))

    mov_panel = ft.Container(
        expand=1, border=_border(), border_radius=8, padding=20,
        content=ft.Column(spacing=15, controls=[
            ft.Row(alignment="spaceBetween", controls=[
                ft.Text("Recent Stock Movements", size=18, weight="bold", color=TEXT_PRIMARY),
                ft.Row(spacing=4, controls=[ft.Text("View all", size=11, color=TEXT_MUTED), ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=TEXT_MUTED)])
            ]),
            ft.Column(spacing=10, controls=mov_list)
        ])
    )

    # --- 4. RETURN FULL LAYOUT ---
    return ft.Column(
        expand=True, scroll="auto", spacing=30,
        controls=[
            ft.Column(spacing=4, controls=[
                ft.Row(spacing=8, controls=[ft.Icon(ft.Icons.DASHBOARD_ROUNDED, size=20, color=TEXT_MUTED), ft.Text("Dashboard", size=14, color=TEXT_MUTED, weight="bold")]),
                ft.Text("Good day, Administrator!", size=28, weight="bold", color=TEXT_PRIMARY),
                ft.Text("Here is the current state of your brewery inventory and procurement", size=12, color=TEXT_MUTED),
            ]),
            cards_row,
            ft.Row(spacing=20, vertical_alignment="start", controls=[low_stock_panel, mov_panel])
        ]
    )