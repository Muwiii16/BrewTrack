import flet as ft
from core.theme import *
from models import ingredient_model
from models import inventory_model
from models import purchase_order_model
from models import sales_model
from models import stock_movement_model
#initialize the dashboard view


def nav_section_label(text):
    """Small gray section label for sidebar navigation"""
    return ft.Text(text.upper(), size=11, color=TEXT_SECONDARY, weight=ft.FontWeight.BOLD)


def nav_item(text, selected=False, on_nav=None):
    """A single sidebar nav link. Bold+White if selected, muted gray otherwise."""
    return ft.Container(
        content=ft.Text(
            text, 
            size=13, 
            color=TEXT_PRIMARY if selected else TEXT_SECONDARY, 
            weight=ft.FontWeight.NORMAL
        ),
        on_click=lambda e: on_nav(text) if on_nav else None,
        padding=ft.Padding.symmetric(vertical=6, horizontal=12),
        border_radius=6,
        ink=True,
    )


def build_sidebar(page: ft.Page, user, on_logout, current_page, on_nav):
    logo_block = ft.Column([
        ft.Image(src='assets/LOGO.png', width=319, fit=ft.BoxFit.CONTAIN, align=ft.Alignment.CENTER),
    ], spacing=6,)

    nav_column = ft.Column([
        nav_section_label("Overview"),
        nav_item("Dashboard", selected=(current_page == "Dashboard"), on_nav=on_nav),

        ft.Container(height=12),  # spacer
        nav_section_label("Master Records"),
        nav_item("User Management", selected=(current_page == "User Management"), on_nav=on_nav),
        nav_item("Supplier Management", selected=(current_page == "Supplier Management"), on_nav=on_nav),
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
        nav_item("Usage/Stock-Out", selected=(current_page == "Usage/Stock-Out"), on_nav=on_nav),
        nav_item("Daily Sales", selected=(current_page == "Daily Sales"), on_nav=on_nav),

        ft.Container(height=12),
        nav_section_label("Insights"),
        nav_item("Reports", selected=(current_page == "Reports"), on_nav=on_nav),
    ], spacing=2, scroll=ft.ScrollMode.AUTO, expand=True,)

    profile_block = ft.Row([
        ft.Icon(ft.Icons.ACCOUNT_CIRCLE_ROUNDED,
                size=36, color=TEXT_SECONDARY),
        ft.Column([
            ft.Text(user["full_name"], size=13, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text(user["role"], size=11, color=TEXT_SECONDARY),
        ], spacing=0),
        ft.Container(expand=True),  # spacer
        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color=ACCENT_GOLD, 
                on_click=lambda e: on_logout(), alignment=ft.Alignment.CENTER_RIGHT),
    ], spacing=8,)

    return ft.Container(
        content=ft.Column([
            logo_block,
            ft.Container(height=20),
            nav_column,
            profile_block,
        ], expand=True,),
        width=260,
        bgcolor=SIDEBAR_COLOR,
        padding=20,
    )
    

def build_header(user_name):
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_PRIMARY),
        ft.Text("Dashboard", size=14, color=TEXT_PRIMARY),
    ], spacing=4,)

    greeting = ft.Text(f'Good day, {user_name}!', size=28,
                       color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        'Here is the current state of your brewery inventory and procurement', size=13, color=TEXT_SECONDARY)

    return ft.Column([
        breadcrumb,
        greeting,
        subtitle,
    ], spacing=6,)


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


def build_stats_row():
    """Each number comes from the model file that owns that table."""
    total_ingredients = ingredient_model.get_total_ingredients()
    low_stock = inventory_model.get_low_stock_count()
    pending_orders = purchase_order_model.get_pending_orders_count()
    daily_sales = sales_model.get_daily_sales_total()
    return ft.Row([
        stat_card("Total Ingredients", f"{total_ingredients:,}", "As of today"),
        stat_card("Low Stock Items", str(low_stock), "Needs attention"),
        stat_card("Pending Orders", str(pending_orders), "Awaiting approval"),
        stat_card("Daily Sales", f"₱{daily_sales:,.2f}", "Today so far")
    ], spacing=16,)


def badge(text, bg_color, text_color='#000000'):
    return ft.Container(
        content=ft.Text(
            text, size=11, weight=ft.FontWeight.BOLD, color=text_color),
        bgcolor=bg_color,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=20,
    )


STATUS_COLORS = {
    "low": STATUS_LOW,
    "pending": STATUS_LOW,
    "approved": STATUS_GREEN,
    "stock-in": STATUS_GREEN,
    "stock-out": STATUS_RED,
    "sale": STATUS_TEAL,
}


def stock_list_row(name, info, status_text, status_color, text_color='#000000'):
    return ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(name, size=14, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(info, size=11, color=TEXT_SECONDARY),
            ], spacing=2),
            badge(status_text, status_color, text_color),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=12,
    )


def panel_header(title):
    return ft.Row([
        ft.Text(title, size=16, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.Text('View All', size=12, color=TEXT_SECONDARY),
            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED,
                    size=14, color=TEXT_SECONDARY),
        ], spacing=4, )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,)

def _qty_fmt(v, uom=""):
    try:
        v = float(v)
        if v == int(v):
            v = int(v)
        return f"{v} {uom}".strip()
    except (TypeError, ValueError):
        return f"{v} {uom}".strip()


def build_low_stock_card():
    """Replaces the old low_stock_data list with a live query."""
    items = inventory_model.get_low_stock_items(limit=4)
    rows = [
        stock_list_row(
            item["item_name"],
            f"{_qty_fmt(item['current_quantity'], item['unit_of_measurement'])} on hand • "
            f"reorder at {_qty_fmt(item['reorder_level'])}",
            "Low",
            STATUS_COLORS["low"],
        )
        for item in items
    ] or [ft.Text("No low-stock items right now.", size=12, color=TEXT_SECONDARY)]
 
    return ft.Container(
        content=ft.Column(
            [panel_header("Low-Stock Alerts")] + rows,
            spacing=10,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=True,
    )


def movement_list_row(tag_text, tag_color, title, subtitle, amount_text, amount_color):
    return ft.Container(
        content=ft.Row([
            badge(tag_text, tag_color, '#ffffff'),
            ft.Column([
                ft.Text(title, size=14, color=TEXT_PRIMARY,
                        weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=11, color=TEXT_SECONDARY),
            ],
                spacing=2,
                expand=True,),
            ft.Text(amount_text, size=13, color=amount_color,
                    weight=ft.FontWeight.BOLD),
        ], spacing=12),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=12,
    )



def build_movements_card():
    """Replaces the old movements_data list with a live query."""
    movements = stock_movement_model.get_recent_movements(limit=4)
    rows = []
    for m in movements:
        tag = m["movement_type"]  # 'Stock-In' / 'Stock-Out' (Sale is logged via reference_type, not shown here)
        qty = m["quantity"]
        amount_color = STATUS_GREEN if qty >= 0 else STATUS_RED
        amount_text = f"{'+' if qty >= 0 else ''}{_qty_fmt(qty)}"
        rows.append(
            movement_list_row(
                tag,
                STATUS_COLORS.get(tag.lower(), STATUS_LOW),
                m["item_name"],
                f"{m['full_name']} | {m['movement_date']:%b %d, %I:%M %p}",
                amount_text,
                amount_color,
            )
        )
    if not rows:
        rows = [ft.Text("No stock movements yet.", size=12, color=TEXT_SECONDARY)]
 
    return ft.Container(
        content=ft.Column(
            [panel_header("Recent Stock Movements")] + rows,
            spacing=10,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
        expand=True,
    )


def po_block(po_number, amount, status_text, status_color, text_color="#000000"):
    return ft.Column(
        [
            ft.Text(po_number, size=13, color=TEXT_PRIMARY,
                    weight=ft.FontWeight.BOLD),
            ft.Text(amount, size=11, color=TEXT_SECONDARY),
            badge(status_text, status_color, text_color),
        ],
        spacing=4,
    )


def build_purchase_orders_bar():
    """Replaces the old purchase_orders_data list with a live query."""
    pos = purchase_order_model.get_recent_purchase_orders(limit=3)
    po_blocks = [
        po_block(
            f"PO-{1000 + item['po_id']}",
            f"P {float(item['total']):,.2f}",
            item["po_status"],
            STATUS_COLORS.get(item["po_status"].lower(), STATUS_LOW),
            "#ffffff" if item["po_status"].lower() == "approved" else "#000000",
        )
        for item in pos
    ]

    return ft.Container(
        content=ft.Row(
            [
                ft.Text("Purchase Orders", size=16,
                        color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
                *po_blocks,
                ft.Row(
                    [
                        ft.Text("View all", size=12, color=TEXT_SECONDARY),
                        ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED,
                                size=14, color=TEXT_SECONDARY),
                    ],
                    spacing=4,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
        padding=16,
    )


def dashboard_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Dashboard", on_nav)

    header = build_header(user["full_name"])
    stats_row = build_stats_row()
    low_stock_card = build_low_stock_card()
    movements_card = build_movements_card()
    po_bar = build_purchase_orders_bar()

    cards_row = ft.Row(
        [low_stock_card, movements_card],
        spacing=16,
    )
    
    header_block = ft.Container(
        content=header, 
        padding=ft.Padding.only(bottom=20), 
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_COLOR))
    )

    main_block = ft.Container(
        content=ft.Column(
            [stats_row, cards_row, po_bar], 
            spacing=20, 
            scroll=ft.ScrollMode.AUTO, 
        ),
        expand=True, 
        bgcolor=INPUT_BG, 
        padding=ft.Padding.only(top=20),
    )

    main_content = ft.Container(
        content=ft.Column(
            [header_block, main_block], 
            spacing=0,
        ),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )