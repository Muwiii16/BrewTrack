import flet as ft
from core.theme import *
from core.inventory_monitoring import build_sidebar, badge
from models import inventory_model


def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Low-Stocks Alert", size=14, color=TEXT_SECONDARY),
    ], spacing=4,)

    title = ft.Text("Low-Stocks Alert", size=28, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Items running low, ranked by urgency. Log usage as you go and flag items for your manager to reorder",
        size=13, color=TEXT_SECONDARY)

    return ft.Column([breadcrumb, title, subtitle], spacing=6,)


def stat_card(label, value):
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=12, color=TEXT_SECONDARY),
            ft.Text(value, size=22, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
        ], spacing=6,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=True,
    )


def _qty_fmt(v, uom=""):
    try:
        v = float(v)
        if v == int(v):
            v = int(v)
        return f"{v} {uom}".strip()
    except (TypeError, ValueError):
        return f"{v} {uom}".strip()


def _item_urgency(current_quantity, reorder_level):
    """Bucket each low-stock item into Out of Stock / Critical / Low."""
    current_quantity = float(current_quantity)
    reorder_level = float(reorder_level) if reorder_level else 0
    if current_quantity <= 0:
        return "Out of Stock"
    if reorder_level > 0 and (current_quantity / reorder_level) <= 0.34:
        return "Critical"
    return "Low"


URGENCY_COLORS = {
    "Out of Stock": (STATUS_RED, "#ffffff", "Stock-Out"),
    "Critical": (STATUS_TEAL, "#ffffff", "Critical"),
    "Low": (STATUS_LOW, "#000000", "Low"),
}


def filter_chip(label, count, selected=False, on_click=None):
    return ft.Container(
        content=ft.Text(f"{label}  {count}", size=13,
                        color=TEXT_PRIMARY if selected else TEXT_SECONDARY,
                        weight=ft.FontWeight.BOLD if selected else ft.FontWeight.NORMAL),
        bgcolor="#2a2a2a" if selected else None,
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=20,
        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
        on_click=on_click,
        ink=True,
    )


def get_low_stock_data():
    """Pulls live low-stock rows and tags each with an urgency bucket."""
    items = inventory_model.get_low_stock_items()
    enriched = []
    for i in items:
        urgency = _item_urgency(i["current_quantity"], i["reorder_level"])
        enriched.append({**i, "urgency": urgency})
    return enriched


def low_stock_item_card(item, on_flag_manager=None, on_record_usage=None):
    urgency = item["urgency"]
    badge_bg, badge_text_color, badge_label = URGENCY_COLORS[urgency]

    on_hand = _qty_fmt(item["current_quantity"], item["unit_of_measurement"])
    threshold = _qty_fmt(item["reorder_level"], item["unit_of_measurement"])

    header_row = ft.Row([
        ft.Column([
            ft.Text(item["item_name"], size=18, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text(item["supplier_name"] or "-",
                    size=12, color=TEXT_SECONDARY),
        ], spacing=2,),
        ft.Container(expand=True),
        badge(badge_label, badge_bg, badge_text_color),
    ], vertical_alignment=ft.CrossAxisAlignment.START,)

    stock_row = ft.Row([
        ft.Text(f"{on_hand} On Hand", size=15,
                color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        ft.Container(expand=True),
        ft.Text(f"threshold {threshold}", size=12, color=TEXT_SECONDARY),
    ],)

    progress_pct = 0
    try:
        cq = float(item["current_quantity"])
        rl = float(item["reorder_level"])
        if rl > 0:
            progress_pct = max(0.0, min(1.0, cq / rl))
    except (TypeError, ValueError, ZeroDivisionError):
        progress_pct = 0

    progress_bar = ft.ProgressBar(
        value=progress_pct, bgcolor=BORDER_COLOR, color=TEXT_SECONDARY, height=4,
    )

    flag_button = ft.Container(
        content=ft.Text("Flag for Manager", size=13, color="#ffffff",
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        bgcolor=STATUS_RED,
        border_radius=6,
        padding=ft.Padding.symmetric(vertical=10, horizontal=12),
        on_click=on_flag_manager,
        ink=True,
        alignment=ft.alignment.Alignment(0, 0),
    )

    record_usage_button = ft.Container(
        content=ft.Text("Record Usage", size=13, color="#000000",
                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        bgcolor=ACCENT_GOLD,
        border_radius=6,
        padding=ft.Padding.symmetric(vertical=10, horizontal=12),
        on_click=on_record_usage,
        ink=True,
        alignment=ft.alignment.Alignment(0, 0),
    )

    return ft.Container(
        content=ft.Column([
            header_row,
            ft.Container(height=4),
            stock_row,
            progress_bar,
            ft.Container(height=8),
            flag_button,
            record_usage_button,
        ], spacing=8,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=8,
        padding=16,
        expand=True,
    )


def build_stats_row(items):
    out_of_stock = sum(1 for i in items if i["urgency"] == "Out of Stock")
    critical = sum(1 for i in items if i["urgency"] == "Critical")
    low = sum(1 for i in items if i["urgency"] == "Low")
    watch = len(items)

    return ft.Row([
        stat_card("Out of Stock", str(out_of_stock)),
        stat_card("Critical", str(critical)),
        stat_card("Low", str(low)),
        stat_card("Items to Watch", str(watch)),
    ], spacing=16,)


def build_filter_row(items):
    all_count = len(items)
    out_count = sum(1 for i in items if i["urgency"] == "Out of Stock")
    critical_count = sum(1 for i in items if i["urgency"] == "Critical")
    low_count = sum(1 for i in items if i["urgency"] == "Low")

    return ft.Row([
        filter_chip("All", all_count, selected=True),
        filter_chip("Out of Stock", out_count),
        filter_chip("Critical", critical_count),
        filter_chip("Low", low_count),
    ], spacing=10,)


def build_item_grid(items, on_nav=None):
    """Lays cards out two-per-row, matching the mock's grid."""
    def flag_click(e):
        # Intentionally left without a handler for now.
        pass

    def usage_click(e):
        if on_nav:
            on_nav("Stock-Out/Usage")

    rows = []
    for idx in range(0, len(items), 2):
        pair = items[idx:idx + 2]
        row_cards = [
            low_stock_item_card(
                item, on_flag_manager=flag_click, on_record_usage=usage_click)
            for item in pair
        ]
        if len(row_cards) == 1:
            row_cards.append(ft.Container(expand=True))
        rows.append(ft.Row(row_cards, spacing=16,))

    return ft.Column(rows, spacing=16,)


def low_stock_alerts_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Low-Stock Alerts", on_nav)

    items = get_low_stock_data()

    header = build_header()
    stats_row = build_stats_row(items)
    filter_row = build_filter_row(items)
    item_grid = build_item_grid(items, on_nav=on_nav)

    main_content = ft.Container(
        content=ft.Column([
            header, stats_row, filter_row, item_grid,
        ], spacing=20, scroll=ft.ScrollMode.AUTO,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )
