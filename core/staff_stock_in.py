import flet as ft
from core.theme import *
from core.components import _sidebar_section_title
from models import purchase_order_model, inventory_model

def staff_receiving_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
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
    
    sidebar = build_sidebar("Receiving/ Stock-In")

    approved_pos = purchase_order_model.get_purchase_orders()
    approved_pos = [po for po in approved_pos if po['po_status'] == 'Approved']
    
    deliveries_db = {}
    for po in approved_pos:
        deliveries_db[po["po_id"]] = {
            "date": po["po_date"].strftime("%b %d, %Y") if po["po_date"] else "No Date",
            "items_count": f"{len(po.get('items', []))} Items",
            "supplier": po["supplier_name"],
            "ingredients": [{"id": i["item_id"], "name": i["item_name"], "ordered": f"{i['ordered_quantity']:g}", "verified": False} for i in po.get("items", [])]
        }

    selected_po = {"id": None}
    
    incoming_list_col = ft.Column(spacing=12)
    verify_items_col = ft.Column(spacing=12, expand=True)
    verify_btn = ft.Container(
        content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text("Verify Stock", size=13, color="#000000", weight="bold")]),
        bgcolor=ACCENT, border_radius=6, padding=16, ink=True, disabled=True, opacity=0.5
    )

    def _border(): return ft.Border(top=ft.BorderSide(1, CARD_BORDER), bottom=ft.BorderSide(1, CARD_BORDER), left=ft.BorderSide(1, CARD_BORDER), right=ft.BorderSide(1, CARD_BORDER))

    def check_status():
        pid = selected_po["id"]
        if pid and pid in deliveries_db:
            all_good = all(item["verified"] for item in deliveries_db[pid]["ingredients"])
            verify_btn.disabled = not all_good
            verify_btn.opacity = 1.0 if all_good else 0.5
        page.update()

    def build_verify_pane():
        verify_items_col.controls.clear()
        pid = selected_po["id"]
        if not pid or pid not in deliveries_db:
            verify_items_col.controls.append(ft.Text("Select an incoming delivery order to verify items.", size=13, color=TEXT_MUTED))
            return

        for item in deliveries_db[pid]["ingredients"]:
            def toggle(target):
                def handler(e): target["verified"] = not target["verified"]; build_verify_pane(); check_status()
                return handler
            verify_items_col.controls.append(ft.Container(border=ft.Border(bottom=ft.BorderSide(1, CARD_BORDER)), padding=12, content=ft.Row([
                ft.Column([ft.Text(item["name"], size=16, weight="bold", color=TEXT_PRIMARY), ft.Text(f"Ordered: {item['ordered']}", size=13, color=TEXT_MUTED)], spacing=4, expand=True),
                ft.IconButton(icon=ft.Icons.CHECK_CIRCLE_ROUNDED if item["verified"] else ft.Icons.RADIO_BUTTON_UNCHECKED_ROUNDED, icon_color="#4CAF50" if item["verified"] else TEXT_MUTED, on_click=toggle(item))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)))

    def build_incoming_pane():
        incoming_list_col.controls.clear()
        for pid, data in deliveries_db.items():
            is_active = (selected_po["id"] == pid)
            def click(p): return lambda e: selected_po.update({"id": p}) or build_incoming_pane() or build_verify_pane() or check_status()
            incoming_list_col.controls.append(ft.Container(bgcolor="#2A2A2A" if is_active else "transparent", border=ft.Border(top=ft.BorderSide(1, ACCENT if is_active else CARD_BORDER), bottom=ft.BorderSide(1, ACCENT if is_active else CARD_BORDER), left=ft.BorderSide(1, ACCENT if is_active else CARD_BORDER), right=ft.BorderSide(1, ACCENT if is_active else CARD_BORDER)), border_radius=8, padding=16, ink=True, on_click=click(pid), content=ft.Row([
                ft.Column([ft.Text(f"PO-{pid:04d} | {data['supplier']}", size=16, weight="bold", color=TEXT_PRIMARY), ft.Text(data["date"], size=13, color=TEXT_MUTED)], spacing=4, expand=True),
                ft.Container(content=ft.Text(data["items_count"], size=12), border=_border(), border_radius=12, padding=8)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)))

    def submit_stock(e):
        purchase_order_model.receive_po(selected_po["id"])
        page.snack_bar = ft.SnackBar(ft.Text("Inventory updated! PO received."), bgcolor=ft.Colors.GREEN_800); page.snack_bar.open = True
        if global_navigate_to: global_navigate_to("Receiving/ Stock-In")

    verify_btn.on_click = submit_stock
    build_incoming_pane()
    build_verify_pane()

    main_content = ft.Container(expand=True, padding=24, content=ft.Column(scroll="auto", spacing=20, controls=[
        ft.Column([ft.Text("Receiving/ Stock-In", size=28, weight="bold", color=TEXT_PRIMARY), ft.Text("Verify shipments before adding to inventory.", size=13, color=TEXT_MUTED)], spacing=6),
        ft.Row(spacing=16, vertical_alignment=ft.CrossAxisAlignment.START, controls=[
            ft.Container(expand=5, border=_border(), border_radius=8, padding=24, content=ft.Column([ft.Text("Incoming Deliveries", size=20, weight="bold", color=TEXT_PRIMARY), incoming_list_col], spacing=12)),
            ft.Container(expand=6, border=_border(), border_radius=8, padding=24, content=ft.Column([ft.Row([ft.Text("Verify", size=24, weight="bold", color=TEXT_PRIMARY), verify_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER), verify_items_col], spacing=12))
        ])
    ]))
    return ft.Row([sidebar, main_content], expand=True, spacing=0)