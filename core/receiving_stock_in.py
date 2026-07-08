import flet as ft
from datetime import datetime

from core.theme import *
from core.inventory_monitoring import build_sidebar
from models import inventory_model, ingredient_model, purchase_order_model
from models import stock_movement_model


def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Receiving/ Stock-In", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Receiving/ Stock- In", size=28, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Log incoming deliveries to add them into inventory",
        size=13, color=TEXT_SECONDARY)

    return ft.Column([breadcrumb, title, subtitle], spacing=6,)


def _qty_fmt(v, uom=""):
    try:
        v = float(v)
        if v == int(v):
            v = int(v)
        return f"{v} {uom}".strip()
    except (TypeError, ValueError):
        return f"{v} {uom}".strip()


def _date_fmt(dt):
    if not dt:
        return ""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return dt
    day = dt.strftime("%d").lstrip("0") or "0"
    return dt.strftime(f"%b {day}, %I:%M %p").replace(" 0", " ")


def _first_name(full_name):
    return (full_name or "").split(" ")[0] if full_name else "-"


def field_label(text):
    return ft.Text(text, size=14, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD)


def get_item_options():
    """Dropdown options for every active ingredient/supply."""
    items = ingredient_model.get_ingredients()
    return items, [
        ft.dropdown.Option(key=str(i["item_id"]), text=i["item_name"])
        for i in items
    ]


def get_awaiting_delivery():
    """Most recent approved PO that hasn't been marked received yet."""
    approved = purchase_order_model.get_approved_pos()
    return approved[0] if approved else None


def build_awaiting_delivery_box(po):
    if po:
        label = "Awaiting Delivery"
        value = f"PO-{po['po_id']} | {po['supplier_name']}"
    else:
        label = "Awaiting Delivery"
        value = "No purchase orders pending delivery"

    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=12, color=TEXT_SECONDARY),
            ft.Text(value, size=15, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
        ], spacing=4,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=14,
        bgcolor=CARD_COLOR,
    )


def build_recent_stock_in_row(m):
    amount = f"+ {_qty_fmt(m['quantity'], m.get('unit_of_measurement', ''))}"
    subtitle = f"{m['remarks'] or '-'} | {_first_name(m['full_name'])} ({m.get('role', '')})"

    return ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(m["item_name"], size=15, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=12, color=TEXT_SECONDARY),
            ], spacing=2, expand=True,),
            ft.Column([
                ft.Text(amount, size=13, color=TEXT_SECONDARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(_date_fmt(m["movement_date"]),
                        size=11, color=TEXT_SECONDARY),
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END,),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
        padding=ft.Padding.only(bottom=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def build_recent_stock_in_card():
    rows = [build_recent_stock_in_row(m)
            for m in stock_movement_model.get_recent_stock_in(limit=6)]

    if not rows:
        rows = [ft.Text("No stock-in activity yet.",
                        size=13, color=TEXT_SECONDARY)]

    return ft.Container(
        content=ft.Column(
            [ft.Text("Recent Stock-In", size=18, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD)] + rows,
            spacing=14,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=20,
        expand=True,
    )


def build_record_delivery_card(page: ft.Page, user, on_nav):
    items, item_options = get_item_options()
    awaiting_po = get_awaiting_delivery()

    item_dropdown = ft.Dropdown(
        options=item_options,
        hint_text="Select Item",
        bgcolor=CARD_COLOR,
        border_color=BORDER_COLOR,
        color=TEXT_PRIMARY,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
    )

    qty_field = ft.TextField(
        hint_text="0",
        value="0",
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor=CARD_COLOR,
        border_color=BORDER_COLOR,
        color=TEXT_PRIMARY,
        hint_style=ft.TextStyle(color=TEXT_SECONDARY),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
    )

    reference_field = ft.TextField(
        hint_text="e.g. PO-1043 or supplier delivery",
        bgcolor=CARD_COLOR,
        border_color=BORDER_COLOR,
        color=TEXT_PRIMARY,
        hint_style=ft.TextStyle(color=TEXT_SECONDARY),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
    )

    error_text = ft.Text("", size=12, color=STATUS_RED)

    def add_to_inventory(e):
        if not item_dropdown.value:
            error_text.value = "Please select an item."
            page.update()
            return
        try:
            qty = float(qty_field.value)
            if qty <= 0:
                raise ValueError
        except (TypeError, ValueError):
            error_text.value = "Please enter a valid quantity."
            page.update()
            return

        item_id = int(item_dropdown.value)
        source_ref = reference_field.value.strip(
        ) if reference_field.value else "Manual entry"
        user_id = user.get("user_id", 1)

        inventory_model.manual_stock_in(item_id, qty, user_id, source_ref)

        # Refresh the whole page so the recent stock-in list and stats update
        on_nav("Receiving/Stock-In")

    add_button = ft.Container(
        content=ft.Text("Add to Inventory", size=14, color="#000000",
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        bgcolor=ACCENT_GOLD,
        border_radius=6,
        padding=ft.Padding.symmetric(vertical=12, horizontal=12),
        on_click=add_to_inventory,
        ink=True,
        alignment=ft.alignment.Alignment(0, 0),
    )

    form = ft.Column([
        field_label("Item"),
        item_dropdown,
        ft.Container(height=6),
        field_label("Quantity Received"),
        qty_field,
        ft.Container(height=6),
        field_label("Source/ Reference"),
        reference_field,
        ft.Container(height=6),
        build_awaiting_delivery_box(awaiting_po),
        error_text,
        ft.Container(height=6),
        add_button,
    ], spacing=8,)

    return ft.Container(
        content=ft.Column(
            [ft.Text("Record Delivery", size=18, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD), ft.Container(height=8), form],
            spacing=0,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=20,
        expand=True,
    )


def receiving_stock_in_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout,
                            "Receiving/Stock-In", on_nav)

    header = build_header()
    record_delivery_card = build_record_delivery_card(page, user, on_nav)
    recent_stock_in_card = build_recent_stock_in_card()

    cards_row = ft.Row(
        [record_delivery_card, recent_stock_in_card],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    main_content = ft.Container(
        content=ft.Column([
            header, cards_row], spacing=20, scroll=ft.ScrollMode.AUTO,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )
