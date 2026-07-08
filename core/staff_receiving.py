import flet as ft
from core.theme import *
from core.dashboard import build_sidebar, panel_header, badge

# ---------- Header ----------


def build_header():
    title = ft.Text("Receiving/Stock-In", size=28,
                    color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text(
        "Log incoming deliveries to add them into inventory", size=13, color=TEXT_SECONDARY)
    return ft.Column([title, subtitle], spacing=4)


# ---------- Top Metric Counters Row ----------
def metric_card(label, value):
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=11, color=TEXT_SECONDARY,
                    weight=ft.FontWeight.W_500),
            ft.Text(value, size=24, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
        ], spacing=4),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=ft.padding.only(left=16, top=12, right=16, bottom=12),
        expand=True,
    )


def build_metrics_row():
    return ft.Row([
        metric_card("Out of Stock", "1"),
        metric_card("Critical", "1"),
        metric_card("Low", "4"),
        metric_card("Items to Watch", "5"),
    ], spacing=16)


# ---------- Main Functional View Function ----------
def staff_receiving_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout,
                            "Receiving/Stock-In", on_nav)

    # --- Sample Mock Database State ---
    deliveries_db = {
        "PO-1008": {
            "date": "Approved Jul 3, 2026",
            "items_count": "2 Items",
            "ingredients": [
                {"name": "Arabica Coffee Beans",
                    "ordered": "5 kg", "verified": False},
                {"name": "Black Coffee Beans", "ordered": "5 kg", "verified": False}
            ]
        }
    }

    selected_po = {"id": "PO-1008"}

    # --- UI Layout Component Architecture ---
    incoming_list_column = ft.Column(spacing=12)
    verify_items_column = ft.Column(spacing=12, expand=True)

    # Accent gold main button
    verify_stock_button = ft.Container(
        content=ft.Text("Verify Stock", size=13,
                        color="#000000", weight=ft.FontWeight.BOLD),
        bgcolor=ACCENT_GOLD,
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        alignment=ft.alignment.Alignment(0, 0),
        ink=True,
        disabled=True,
        opacity=0.5
    )

    def check_global_verification_status():
        """Enables global button only when every item in the current PO is checked."""
        po_id = selected_po["id"]
        if po_id and po_id in deliveries_db:
            all_good = all(item["verified"]
                           for item in deliveries_db[po_id]["ingredients"])
            verify_stock_button.disabled = not all_good
            verify_stock_button.opacity = 1.0 if all_good else 0.5
        page.update()

    def build_verify_pane():
        """Generates the right side verification panel workspace."""
        verify_items_column.controls.clear()
        po_id = selected_po["id"]

        if not po_id or po_id not in deliveries_db:
            verify_items_column.controls.append(
                ft.Text("Select an incoming delivery order to verify items.",
                        size=13, color=TEXT_SECONDARY)
            )
            verify_stock_button.disabled = True
            verify_stock_button.opacity = 0.5
            return

        po_data = deliveries_db[po_id]

        for item in po_data["ingredients"]:
            # State closures for individual row check toggling
            def make_toggle_handler(target_item):
                def handler(e):
                    target_item["verified"] = not target_item["verified"]
                    build_verify_pane()
                    check_global_verification_status()
                return handler

            item_row = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(item["name"], size=16,
                                color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Ordered: {item['ordered']}",
                                size=13, color=TEXT_SECONDARY),
                    ], spacing=4, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CHECK_CIRCLE_ROUNDED if item[
                            "verified"] else ft.Icons.RADIO_BUTTON_UNCHECKED_ROUNDED,
                        icon_color=STATUS_GREEN if item["verified"] else TEXT_SECONDARY,
                        icon_size=24,
                        on_click=make_toggle_handler(item)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
                padding=ft.padding.only(bottom=16, top=4)
            )
            verify_items_column.controls.append(item_row)

    def handle_po_selection(po_id):
        selected_po["id"] = po_id
        build_incoming_pane()
        build_verify_pane()
        check_global_verification_status()

    def build_incoming_pane():
        """Generates selectable PO items card stack."""
        incoming_list_column.controls.clear()
        for po_id, data in deliveries_db.items():
            is_active = selected_po["id"] == po_id

            def make_click_handler(pid):
                return lambda e: handle_po_selection(pid)

            incoming_list_column.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(po_id, size=18, color=TEXT_PRIMARY,
                                    weight=ft.FontWeight.BOLD),
                            ft.Text(data["date"], size=13,
                                    color=TEXT_SECONDARY),
                        ], spacing=4, expand=True),
                        ft.Container(
                            content=ft.Text(
                                data["items_count"], size=12, color=TEXT_PRIMARY),
                            border=ft.Border.all(1, BORDER_COLOR),
                            border_radius=12,
                            padding=ft.padding.symmetric(
                                horizontal=12, vertical=4)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=CARD_COLOR if is_active else "transparent",
                    border=ft.Border.all(
                        1, ACCENT_GOLD if is_active else BORDER_COLOR),
                    border_radius=8,
                    padding=16,
                    ink=True,
                    on_click=make_click_handler(po_id)
                )
            )

    # --- Global Stock In Submission Handler ---
    def submit_verified_stock(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"Inventory updated! {selected_po['id']} logged successfully."),
            bgcolor=STATUS_GREEN
        )
        page.snack_bar.open = True
        selected_po["id"] = None
        build_incoming_pane()
        build_verify_pane()
        check_global_verification_status()

    verify_stock_button.on_click = submit_verified_stock

    # Initialize dynamic component frames
    build_incoming_pane()
    build_verify_pane()

    # --- Core Workspace Layout Grid Blocks ---
    incoming_deliveries_card = ft.Container(
        content=ft.Column([
            ft.Text("Incoming Deliveries", size=20,
                    color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Container(height=4),
            incoming_list_column
        ], spacing=12),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=8,
        padding=24,
        expand=5,  # FIXED: Changed from 1 to 5
    )

    verify_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Verify", size=24, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                verify_stock_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=8),
            verify_items_column
        ], spacing=12),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=8,
        padding=24,
        expand=6,  # FIXED: Changed from 1.2 to 6
    )

    middle_workspace_row = ft.Row(
        [incoming_deliveries_card, verify_card],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH
    )

    # --- Bottom Timeline Logger Panel ---
    recently_received_card = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text("Recently\nReceived", size=20,
                                color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                width=160,
                alignment=ft.alignment.Alignment(-1, 0)
            ),
            ft.VerticalDivider(color=BORDER_COLOR, width=1),
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text("Coffee Beans", size=16,
                                color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                        ft.Text("PO-1008 received | Marco (Staff)",
                                size=13, color=TEXT_SECONDARY),
                    ], spacing=4, expand=True),
                    ft.Column([
                        ft.Text("+ 20 kg", size=14, color=TEXT_SECONDARY,
                                weight=ft.FontWeight.W_500),
                        ft.Text("Jul 15, 5:00 PM", size=12,
                                color=TEXT_SECONDARY),
                    ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.END)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                padding=ft.padding.only(left=16)
            )
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=8,
        padding=20,
        height=90
    )

    # --- Assembler View Layout Wrapper ---
    main_content = ft.Container(
        content=ft.Column([
            build_header(),
            build_metrics_row(),
            ft.Container(content=middle_workspace_row, expand=True),
            recently_received_card
        ], spacing=20),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )
