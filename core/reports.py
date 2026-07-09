import flet as ft
from core.theme import *
from models import report_model
from models import inventory_model
from core.purchase_order import build_sidebar


def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Reports", size=14, color=TEXT_SECONDARY),
    ], spacing=4)
    return ft.Column([
        breadcrumb,
        ft.Text("Reports", size=28, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        ft.Text("Consolidated inventory, procurement, and sales analytics.", size=13, color=TEXT_SECONDARY),
    ], spacing=6)


def _money_fmt(v):
    try:
        return f"P {float(v):,.2f}"
    except (TypeError, ValueError):
        return "P 0.00"

def stat_card(label, value):
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=12, color=TEXT_SECONDARY),
            ft.Text(value, size=22, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        ], spacing=6),
        border=ft.Border.all(1, BORDER_COLOR), border_radius=6, padding=16, expand=True,
    )
# ---------------------------------------------------------------------------
# Lightweight bar chart built from Containers - Flet 0.85 has no chart
# controls, so bars are just height-scaled rectangles with a label/value.
# ---------------------------------------------------------------------------
def bar_chart(items, label_key, value_key, value_fmt=lambda v: str(v), color=ACCENT_GOLD, chart_height=220):
    if not items:
        return ft.Container(
            content=ft.Text("No data yet.", color=TEXT_SECONDARY, size=13),
            alignment=ft.Alignment.CENTER,
            height=chart_height,
        )

    max_val = max(float(i[value_key]) for i in items) or 1
    bars = []
    for i in items:
        val = float(i[value_key])
        bar_h = max(4, (val / max_val) * (chart_height - 50))
        bars.append(
            ft.Column(
                [
                    ft.Text(value_fmt(val), size=11, color=TEXT_SECONDARY),
                    ft.Container(width=32, height=bar_h, bgcolor=color, border_radius=4),
                    ft.Text(str(i[label_key]), size=11, color=TEXT_SECONDARY,
                             max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, width=60,
                             text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.END,
                spacing=6,
            )
        )
    return ft.Container(
        content=ft.Row(bars, alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=ft.CrossAxisAlignment.END, spacing=10),
        height=chart_height,
        padding=ft.Padding.only(top=10),
    )


def report_panel(title, subtitle, chart_control):
    return ft.Container(
        content=ft.Column([
            ft.Text(title, size=20, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Text(subtitle, size=12, color=TEXT_SECONDARY),
            ft.Container(height=10),
            chart_control,
        ], spacing=2),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=20,
        expand=True,
    )





def reports_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Reports", on_nav)

    inventory_value = inventory_model.get_inventory_overview()
    inventory_value_total = sum(float(i["value"]) for i in inventory_value)
    sales_revenue = report_model.get_total_sales_revenue()
    low_stock_items = inventory_model.get_low_stock_count()
    receiving_accuracy = report_model.get_receiving_accuracy()

    stats_row = ft.Row([
        stat_card("Inventory Value", _money_fmt(inventory_value_total)),
        stat_card("Sales Revenue", _money_fmt(sales_revenue)),
        stat_card("Low-Stock Items", str(low_stock_items)),
        stat_card("Receiving Accuracy", f"{receiving_accuracy:.1f} %"),
    ], spacing=16)

    # Panel 1: Inventory Value by category
    category_data = report_model.get_inventory_value_by_category()
    inventory_chart = bar_chart(category_data, "category", "value", value_fmt=_money_fmt, color=ACCENT_GOLD)
    inventory_panel = report_panel("Inventory Value", "Current on-hand value by category", inventory_chart)

    # Panel 2: Revenue and Sales Performance (last 7 days)
    revenue_data = report_model.get_revenue_by_day(days=7)
    for r in revenue_data:
        r["day_label"] = r["day"].strftime("%b %d")
    revenue_chart = bar_chart(revenue_data, "day_label", "revenue", value_fmt=_money_fmt, color=STATUS_TEAL)
    revenue_panel = report_panel("Revenue and Sales Performance", "Revenue and units sold", revenue_chart)

    charts_row = ft.Row([inventory_panel, revenue_panel], spacing=16)

    main_content = ft.Container(
        content=ft.Column(
            [build_header(), stats_row, charts_row],
        #build_detailed_reports_bar(on_view_reports
            spacing=20, scroll=ft.ScrollMode.AUTO,
        ),
        expand=True, padding=24,
    )

    return ft.Row([sidebar, main_content], expand=True, spacing=0)