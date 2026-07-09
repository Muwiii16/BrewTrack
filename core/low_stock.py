import flet as ft
from core.theme import *
from models import inventory_model

def nav_section_label(text):
    return ft.Text(text.upper(), size=11, color=TEXT_SECONDARY, weight=ft.FontWeight.BOLD)

def nav_item(text, selected=False, on_nav=None):
    return ft.Container(
        content=ft.Text(text, size=13, color=TEXT_PRIMARY if selected else TEXT_SECONDARY, weight=ft.FontWeight.NORMAL),
        on_click=lambda e: on_nav(text) if on_nav else None,
        padding=ft.Padding.symmetric(vertical=6, horizontal=12), border_radius=6, ink=True,
    )

def build_sidebar(page, user, on_logout, current_page, on_nav):
    logo_block = ft.Column([
        ft.Image(src='assets/LOGO.png', width=319, fit=ft.BoxFit.CONTAIN, align=ft.Alignment.CENTER),
    ], spacing=6)
    
    nav_column = ft.Column([
        nav_section_label("Overview"),
        nav_item("Dashboard", selected=(current_page == "Dashboard"), on_nav=on_nav),
        ft.Container(height=12),
        nav_section_label("Master Records"),
        nav_item("User Management", selected=(current_page == "User Management"), on_nav=on_nav),
        nav_item("Suppliers", selected=(current_page == "Suppliers"), on_nav=on_nav),
        nav_item("Ingredients & Supplies", selected=(current_page == "Ingredients & Supplies"), on_nav=on_nav),
        ft.Container(height=12),
        nav_section_label("Operations"),
        nav_item("Inventory Monitoring", selected=(current_page == "Inventory Monitoring"), on_nav=on_nav),
        nav_item("Low-Stock Items", selected=(current_page == "Low-Stock Items"), on_nav=on_nav),
        nav_item("Purchase Orders", selected=(current_page == "Purchase Orders"), on_nav=on_nav),
        nav_item("Movement History", selected=(current_page == "Movement History"), on_nav=on_nav),
        ft.Container(height=12),
        nav_section_label("Transactions"),
        nav_item("Receiving/Stock-In", selected=(current_page == "Receiving/Stock-In"), on_nav=on_nav),
        nav_item("Stock-Out/Usage", selected=(current_page == "Stock-Out/Usage"), on_nav=on_nav),
        nav_item("Daily Sales", selected=(current_page == "Daily Sales"), on_nav=on_nav),
        ft.Container(height=12),
        nav_section_label("Insights"),
        nav_item("Reports", selected=(current_page == "Reports"), on_nav=on_nav),
    ], spacing=4, scroll=ft.ScrollMode.AUTO, expand=True)
    
    profile_block = ft.Row([
        ft.Icon(ft.Icons.ACCOUNT_CIRCLE_ROUNDED, size=36, color=TEXT_SECONDARY),
        ft.Column([
            ft.Text(user["full_name"], size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Text(user["role"], size=11, color=TEXT_SECONDARY),
        ], spacing=0),
        ft.Container(expand=True),
        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color=ACCENT_GOLD, on_click=lambda e: on_logout()),
    ], spacing=8)
    
    return ft.Container(
        content=ft.Column([logo_block, ft.Container(height=20), nav_column, profile_block], expand=True),
        width=260, bgcolor=SIDEBAR_COLOR, padding=20,
    )
def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Low-Stocks Alert", size=14, color=TEXT_SECONDARY),
    ], spacing=4)
    return ft.Column([
        breadcrumb,
        ft.Text("Low-Stocks Alert", size=28, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        ft.Text("Items at or below their reorder level. Replenish these to avoid production stoppages",
                size=13, color=TEXT_SECONDARY),
    ], spacing=6)


def badge(text, bg_color, text_color='#000000'):
    return ft.Container(
        content=ft.Text(text, size=13, weight=ft.FontWeight.BOLD, color=text_color),
        bgcolor=bg_color, padding=ft.Padding.symmetric(horizontal=12, vertical=6), border_radius=20,
    )


def table_header_row():
    def col(text, width):
        return ft.Container(ft.Text(text, size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD), width=width)
    return ft.Container(
        content=ft.Row([col("Item", 180), col("Supplier", 160), col("On Hand", 130),
                        col("Reorder At", 130), col("Suggested Qty.", 140), col("Status", 120)],
                       alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        padding=ft.Padding.only(left=16, right=16, top=14, bottom=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def low_stock_row(item, supplier, on_hand, reorder_at, suggested, status):
    def cell(text, width, color=TEXT_SECONDARY, bold=False):
        return ft.Container(ft.Text(text, size=14, color=color,
                                     weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
                                     max_lines=1, overflow=ft.TextOverflow.ELLIPSIS), width=width)
    return ft.Container(
        content=ft.Row([
            cell(item, 180, color=TEXT_PRIMARY, bold=True),
            cell(supplier, 160),
            cell(on_hand, 130, color=STATUS_LOW, bold=True),
            cell(reorder_at, 130),
            cell(suggested, 140),
            ft.Container(badge(status, STATUS_LOW, "#000000"), width=120, alignment=ft.alignment.Alignment(-1, 0)),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def _qty_fmt(v, uom=""):
    try:
        v = float(v)
        if v == int(v):
            v = int(v)
        return f"{v} {uom}".strip()
    except (TypeError, ValueError):
        return f"{v} {uom}".strip()


def _money_fmt(v):
    try:
        return f"P {float(v):,.2f}"
    except (TypeError, ValueError):
        return "P 0.00"


def get_low_stock_data():
    items = inventory_model.get_low_stock_items()
    rows = [{
        "item": i["item_name"], "supplier": i["supplier_name"] or "-",
        "on_hand": _qty_fmt(i["current_quantity"], i["unit_of_measurement"]),
        "reorder_at": _qty_fmt(i["reorder_level"], i["unit_of_measurement"]),
        "suggested": _qty_fmt(float(i["reorder_level"]) * 2, i["unit_of_measurement"]),
        "status": "Low",
    } for i in items]
    replenish_cost = sum(float(i["reorder_level"]) * 2 * float(i["cost_per_unit"]) for i in items)
    out_of_stock = sum(1 for i in items if float(i["current_quantity"]) <= 0)
    return rows, len(items), out_of_stock, replenish_cost

def stat_card(label, value, caption):
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=12, color=TEXT_SECONDARY),
            ft.Text(value, size=26, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text(caption, size=11, color=TEXT_SECONDARY),
        ], spacing=4,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=True,
    )
    
def build_search_bar():
    return ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SEARCH_ROUNDED, size=16, color=TEXT_SECONDARY),
            ft.TextField(
                hint_text="Search",
                border=ft.InputBorder.NONE,
                height=45,
                text_size=13,
                color=TEXT_PRIMARY,
                hint_style=ft.TextStyle(color=TEXT_SECONDARY, size=13),
                content_padding=ft.Padding.symmetric(horizontal=0, vertical=8),
                expand=True,
            ),
        ], spacing=8),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=12, vertical=2),
        width=340,
    )

def low_stock_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Low-Stock Items", on_nav)

    def refresh():
        page.controls.clear()
        page.add(low_stock_view(page, user, on_logout, on_nav))
        page.update()

    rows_data, needing_attention, out_of_stock, replenish_cost = get_low_stock_data()

    header_row = ft.Row(
        [build_header(),
         ft.ElevatedButton("Go to Purchase Orders", bgcolor=ACCENT_GOLD, color="#000000",
                            on_click=lambda e: on_nav("Purchase Orders"))],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START,
    )

    stats_row = ft.Row([
        stat_card("Items Needing Attention", str(needing_attention), "Items with low stock levels"),
        stat_card("Out of Stock", str(out_of_stock), "Items currently out of stock"),
        stat_card("Estimated Replenishment Cost", _money_fmt(replenish_cost), "Cost to replenish all low-stock items"),
    ], spacing=16)

    table_rows = [table_header_row()] + [
        low_stock_row(r["item"], r["supplier"], r["on_hand"], r["reorder_at"], r["suggested"], r["status"])
        for r in rows_data
    ]
    table = ft.Container(content=ft.Column(table_rows, spacing=0), border=ft.Border.all(1, BORDER_COLOR), border_radius=6)

    main_content = ft.Container(
        content=ft.Column([header_row, stats_row, build_search_bar(), table], spacing=20, scroll=ft.ScrollMode.AUTO),
        expand=True, padding=24,
    )

    return ft.Row([sidebar, main_content], expand=True, spacing=0)