import flet as ft
from core.theme import *
from core.dashboard import build_sidebar, badge, panel_header, stat_card

# ---------- header ----------


def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Daily Sales Recording", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Daily Sales Recording", size=28, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Ring up orders from the menu - ingredients are deducted from inventory automatically",
        size=13, color=TEXT_SECONDARY,
    )

    return ft.Column([breadcrumb, title, subtitle], spacing=6,)


# ---------- Stats Cards Row ----------

def build_sales_stats_row():
    return ft.Row([
        stat_card("Today's Revenue", "₱0.00", "Gross sales"),
        stat_card("Units Sold Today", "0", "Total drinks served"),
        stat_card("Orders Today", "0", "Completed checkouts"),
    ], spacing=16,)


# ---------- Menu Item (Tappable Stepper) Card ----------

def menu_item_card(item, on_minus, on_plus, qty_text_ref):
    header_row = ft.Row([
        ft.Column([
            ft.Text(item["name"], size=15, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text(f"₱{item['price']:.2f}", size=12, color=TEXT_SECONDARY),
        ], spacing=2),
    ])

    def step_button(icon, on_click):
        return ft.Container(
            content=ft.Icon(icon, size=16, color=TEXT_PRIMARY),
            width=32, height=32,
            border=ft.Border.all(1, BORDER_COLOR),
            border_radius=6,
            alignment=ft.alignment.Alignment(0, 0),
            on_click=on_click,
            ink=True,
        )

    qty_text = ft.Text("0", size=16, color=TEXT_PRIMARY,
                       weight=ft.FontWeight.BOLD)
    qty_text_ref["control"] = qty_text

    stepper_row = ft.Row([
        step_button(ft.Icons.REMOVE_ROUNDED, on_minus),
        ft.Container(qty_text, expand=True,
                     alignment=ft.alignment.Alignment(0, 0)),
        step_button(ft.Icons.ADD_ROUNDED, on_plus),
    ], vertical_alignment=ft.CrossAxisAlignment.CENTER)

    return ft.Container(
        content=ft.Column([header_row, ft.Container(
            height=4), stepper_row], spacing=4,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=8,
        padding=16,
        expand=True,
    )


# ---------- Current Order Panel Elements ----------

def order_list_empty_state():
    return ft.Column([
        ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, size=32, color=TEXT_SECONDARY),
        ft.Text("Tap menu items to start an order.",
                size=12, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
    ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,)


def order_list_row(item, qty):
    return ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(item["name"], size=13, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(f"{qty}x @ ₱{item['price']:.2f}",
                        size=11, color=TEXT_SECONDARY),
            ], spacing=2, expand=True,),
            ft.Text(f"₱{item['price'] * qty:.2f}", size=13, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
    )


# ---------- Recently Orders Bottom Panel ----------

def recent_order_row(row):
    return ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(row["description"], size=14, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(f"{row['staff']} | uses {row['ingredients']}",
                        size=11, color=TEXT_SECONDARY),
            ], spacing=2, expand=True,),
            ft.Column([
                ft.Text(f"₱{row['total']:.2f}", size=14, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(row["time"], size=11, color=TEXT_SECONDARY),
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END,)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=12,
    )


def build_recent_orders_card(rows):
    body = [recent_order_row(r) for r in rows] if rows else [
        ft.Text("No orders recorded today.", size=12, color=TEXT_SECONDARY)]

    return ft.Container(
        content=ft.Column([
            panel_header("Recently Orders"),
            *body
        ], spacing=10,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
    )


# ---------- Main View Function ----------

def daily_sales_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Daily Sales", on_nav)

    # Hardcoded menu items
    menu_items = [
        {"id": 1, "name": "Espresso", "price": 100.00},
        {"id": 2, "name": "Matcha Latte", "price": 180.00},
        {"id": 3, "name": "Spanish Latte", "price": 160.00},
        {"id": 4, "name": "Caramel Macchiato", "price": 160.00},
    ]

    # Sample data for recent orders matching mock design layout
    recent_orders_sample = [
        {
            "description": "2 x Caramel Macchiato",
            "staff": "Marco Reyes (staff)",
            "ingredients": "coffee beans, vanilla syrup, oatmilk",
            "total": 320.00,
            "time": "Jul 15, 5:00 PM"
        }
    ]

    order_state = {item["id"]: 0 for item in menu_items}
    qty_refs = {item["id"]: {} for item in menu_items}

    order_list_column = ft.Column(spacing=8)
    recent_orders_container = ft.Container(
        content=build_recent_orders_card(recent_orders_sample))

    complete_button = ft.Container(
        content=ft.Text("Complete Order", size=14, color="#000000",
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        bgcolor=ACCENT_GOLD,
        border_radius=6,
        padding=ft.Padding.symmetric(vertical=12),
        alignment=ft.alignment.Alignment(0, 0),
        ink=True,
        disabled=True,
        opacity=0.5,
    )

    def refresh_order_list():
        order_list_column.controls.clear()
        active_selections = [(item, order_state[item["id"]])
                             for item in menu_items if order_state[item["id"]] > 0]

        if not active_selections:
            order_list_column.controls.append(order_list_empty_state())
            complete_button.disabled = True
            complete_button.opacity = 0.5
        else:
            for item, qty in active_selections:
                order_list_column.controls.append(order_list_row(item, qty))
            complete_button.disabled = False
            complete_button.opacity = 1
        page.update()

    def make_change_handler(item_id, delta):
        def handler(e):
            new_qty = max(0, order_state[item_id] + delta)
            order_state[item_id] = new_qty
            qty_refs[item_id]["control"].value = str(new_qty)
            refresh_order_list()
        return handler

    def handle_complete_order(e):
        for item in menu_items:
            order_state[item["id"]] = 0
            qty_refs[item["id"]]["control"].value = "0"

        page.snack_bar = ft.SnackBar(
            ft.Text("Order completed successfully."), bgcolor=STATUS_GREEN)
        page.snack_bar.open = True
        refresh_order_list()

    complete_button.on_click = handle_complete_order

    # Build menu selection grid (2 items per row matching stock_out_usage layout)
    cards = []
    for item in menu_items:
        cards.append(
            menu_item_card(
                item,
                on_minus=make_change_handler(item["id"], -1),
                on_plus=make_change_handler(item["id"], 1),
                qty_text_ref=qty_refs[item["id"]]
            )
        )

    grid_rows = []
    for idx in range(0, len(cards), 2):
        pair = cards[idx:idx + 2]
        if len(pair) == 1:
            pair.append(ft.Container(expand=True))
        grid_rows.append(ft.Row(pair, spacing=16))

    tap_to_add_card = ft.Container(
        content=ft.Column(
            [ft.Text("Tap to Add Usage", size=16, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD)] + grid_rows,
            spacing=16,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=2,
    )

    refresh_order_list()

    current_order_card = ft.Container(
        content=ft.Column([
            ft.Text("Current Order", size=16, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Container(
                content=order_list_column,
                padding=ft.Padding.symmetric(vertical=20),
                alignment=ft.alignment.Alignment(0, 0),
            ),
            complete_button
        ], spacing=12,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=1,
    )

    workspace_row = ft.Row([tap_to_add_card, current_order_card],
                           spacing=16, vertical_alignment=ft.CrossAxisAlignment.START)

    main_content = ft.Container(
        content=ft.Column(
            [build_header(), build_sales_stats_row(),
             workspace_row, recent_orders_container],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )
