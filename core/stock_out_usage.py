import flet as ft
from datetime import datetime

from core.theme import *
from core.dashboard import build_sidebar, badge, panel_header
from models import inventory_model
from models import stock_movement_model


def _qty_fmt(v):
    try:
        v = float(v)
        if v == int(v):
            return str(int(v))
        return f"{v:g}"
    except (TypeError, ValueError):
        return str(v)


def _step_for(uom):
    """Bigger units move in whole numbers, smaller units move in chunks."""
    return {
        "kg": 0.5, "l": 0.5, "L": 0.5,
        "g": 50, "ml": 50,
    }.get(uom, 1)


def _date_fmt(dt):
    if not dt:
        return ""
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return dt
    return dt.strftime("%b %d, %I:%M %p")


# ---------- header ----------

def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Stock-Out/ Usage", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Stock- Out/ Usage", size=28, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Tap items as you use them through your shift, then log the whole batch at once.",
        size=13, color=TEXT_SECONDARY,
    )

    return ft.Column([breadcrumb, title, subtitle], spacing=6,)


# ---------- "Tap to Add Usage" card ----------

def usage_stepper_card(item, on_minus, on_plus, qty_text_ref):
    is_low = float(item["current_quantity"]) <= float(item["reorder_level"])

    header_row = ft.Row(
        [
            ft.Text(item["item_name"], size=15, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
        ] + ([badge("Low", STATUS_LOW, "#000000")] if is_low else []),
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

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

    qty_text = ft.Text(_qty_fmt(0), size=16, color=TEXT_PRIMARY,
                       weight=ft.FontWeight.BOLD)
    qty_text_ref["control"] = qty_text

    stepper_row = ft.Row(
        [
            step_button(ft.Icons.REMOVE_ROUNDED, on_minus),
            ft.Container(qty_text, expand=True,
                         alignment=ft.alignment.Alignment(0, 0)),
            step_button(ft.Icons.ADD_ROUNDED, on_plus),
            ft.Container(width=8),
            ft.Text(item["unit_of_measurement"],
                    size=13, color=TEXT_SECONDARY),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column([header_row, ft.Container(
            height=10), stepper_row], spacing=4,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=8,
        padding=16,
        expand=True,
    )


# ---------- "Usage List" card ----------

def usage_list_empty_state():
    return ft.Column(
        [
            ft.Icon(ft.Icons.TOUCH_APP_ROUNDED, size=32, color=TEXT_SECONDARY),
            ft.Text("Tap items on the left to build your usage list",
                    size=12, color=TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def usage_list_row(item, qty, on_remove):
    return ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(item["item_name"], size=13, color=TEXT_PRIMARY,
                                weight=ft.FontWeight.BOLD),
                        ft.Text(f"{_qty_fmt(qty)} {item['unit_of_measurement']}",
                                size=11, color=TEXT_SECONDARY),
                    ],
                    spacing=2, expand=True,
                ),
                ft.IconButton(ft.Icons.CLOSE_ROUNDED, icon_size=16,
                              icon_color=TEXT_SECONDARY, on_click=on_remove),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
    )


# ---------- "Recently Usage" card ----------

def recent_usage_row(row):
    qty = row["quantity"]  # stored negative for Stock-Out
    return ft.Container(
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(row["item_name"], size=14, color=TEXT_PRIMARY,
                                weight=ft.FontWeight.BOLD),
                        ft.Text(f"{row.get('remarks') or 'Manual'} | {row['full_name']}",
                                size=11, color=TEXT_SECONDARY),
                    ],
                    spacing=2, expand=True,
                ),
                ft.Column(
                    [
                        ft.Text(f"{_qty_fmt(qty)} {row.get('unit_of_measurement', '')}".strip(),
                                size=13, color=STATUS_RED, weight=ft.FontWeight.BOLD),
                        ft.Text(_date_fmt(row["movement_date"]),
                                size=11, color=TEXT_SECONDARY),
                    ],
                    spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=12,
    )


def build_recent_usage_card(rows):
    if not rows:
        body = [ft.Text("No usage logged yet.", size=12, color=TEXT_SECONDARY)]
    else:
        body = [recent_usage_row(r) for r in rows]

    return ft.Container(
        content=ft.Column(
            [panel_header("Recently Usage")] + body, spacing=10,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
    )


# ---------- data ----------

def get_recent_usage(limit=5):
    """Recent Stock-Out movements, enriched with unit of measurement."""
    rows = stock_movement_model.get_recent_stock_out(limit=limit)
    units = {i["item_id"]: i["unit_of_measurement"]
             for i in inventory_model.get_inventory_overview()}
    for r in rows:
        r["unit_of_measurement"] = units.get(r["item_id"], "")
    return rows


# ---------- main view ----------

def stock_out_usage_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Stock-Out/Usage", on_nav)

    items = inventory_model.get_inventory_overview()

    usage_state = {i["item_id"]: 0 for i in items}
    qty_refs = {i["item_id"]: {} for i in items}

    usage_list_column = ft.Column(spacing=8)
    recent_usage_container = ft.Container(
        content=build_recent_usage_card(get_recent_usage()))

    reference_dropdown = ft.Dropdown(
        value="Ingredient Usage",
        options=[
            ft.dropdown.Option("Ingredient Usage"),
            ft.dropdown.Option("Waste / Spoilage"),
            ft.dropdown.Option("Sample / Tasting"),
        ],
        border_color=BORDER_COLOR,
        color=TEXT_PRIMARY,
        bgcolor=CARD_COLOR,
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=8),
    )

    log_button = ft.Container(
        content=ft.Text("Log Shift Usage", size=14, color="#000000",
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        bgcolor=ACCENT_GOLD,
        border_radius=6,
        padding=ft.Padding.symmetric(vertical=12),
        alignment=ft.alignment.Alignment(0, 0),
        ink=True,
        disabled=True,
        opacity=0.5,
    )

    def refresh_usage_list():
        usage_list_column.controls.clear()
        active = [(item, usage_state[item["item_id"]]) for item in items
                  if usage_state[item["item_id"]] > 0]

        if not active:
            usage_list_column.controls.append(usage_list_empty_state())
            log_button.disabled = True
            log_button.opacity = 0.5
        else:
            for item, qty in active:
                usage_list_column.controls.append(
                    usage_list_row(
                        item, qty, on_remove=make_remove_handler(item["item_id"]))
                )
            log_button.disabled = False
            log_button.opacity = 1
        page.update()

    def make_change_handler(item_id, delta):
        def handler(e):
            item = next(i for i in items if i["item_id"] == item_id)
            step = _step_for(item["unit_of_measurement"])
            new_val = usage_state[item_id] + delta * step
            new_val = round(max(0, new_val), 2)
            usage_state[item_id] = new_val
            qty_refs[item_id]["control"].value = _qty_fmt(new_val)
            refresh_usage_list()
        return handler

    def make_remove_handler(item_id):
        def handler(e):
            usage_state[item_id] = 0
            qty_refs[item_id]["control"].value = "0"
            refresh_usage_list()
        return handler

    def log_shift_usage(e):
        user_id = user.get("user_id", 1)
        ref_type = reference_dropdown.value
        any_logged = False

        for item in items:
            qty = usage_state[item["item_id"]]
            if qty > 0:
                inventory_model.stock_out(
                    item["item_id"], qty, user_id,
                    reference_type=ref_type, remarks=ref_type,
                )
                usage_state[item["item_id"]] = 0
                qty_refs[item["item_id"]]["control"].value = "0"
                any_logged = True

        if any_logged:
            recent_usage_container.content = build_recent_usage_card(
                get_recent_usage())
            page.snack_bar = ft.SnackBar(
                ft.Text("Shift usage logged."), bgcolor=STATUS_GREEN)
            page.snack_bar.open = True

        refresh_usage_list()

    log_button.on_click = log_shift_usage

    # build the tappable ingredient grid, 2 per row
    cards = []
    for item in items:
        cards.append(
            usage_stepper_card(
                item,
                on_minus=make_change_handler(item["item_id"], -1),
                on_plus=make_change_handler(item["item_id"], 1),
                qty_text_ref=qty_refs[item["item_id"]],
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

    refresh_usage_list()  # populate empty state on first render

    usage_list_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("Usage List", size=16, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=usage_list_column,
                    padding=ft.Padding.symmetric(vertical=20),
                    alignment=ft.alignment.Alignment(0, 0),
                ),
                reference_dropdown,
                log_button,
            ],
            spacing=12,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=1,
    )

    cards_row = ft.Row([tap_to_add_card, usage_list_card], spacing=16,)

    main_content = ft.Container(
        content=ft.Column(
            [build_header(), cards_row, recent_usage_container],
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
