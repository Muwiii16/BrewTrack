import flet as ft
from core.theme import *
from models import supplier_model

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
        nav_item("Low-Stock Alerts", selected=(current_page == "Low-Stock Alerts"), on_nav=on_nav),
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


def build_header():
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_PRIMARY),
        ft.Text("Supplier Management", size=14, color=TEXT_PRIMARY),
    ], spacing=4,)

    title = ft.Text("Supplier Management", size=28, color=TEXT_PRIMARY,
                     weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Maintain vendors that supply your ingredients and packaging.", size=13, color=TEXT_SECONDARY)

    add_supplier_btn = ft.ElevatedButton(
        content=ft.Text("Add Supplier", size=13, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
        bgcolor=ACCENT_GOLD,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            padding=ft.Padding.symmetric(horizontal=18, vertical=18),
        ),
    )

    title_row = ft.Row(
        [
            ft.Column([title, subtitle], spacing=6),
            add_supplier_btn,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    return ft.Column([
        breadcrumb,
        title_row,
    ], spacing=16,)


def badge(text, bg_color, text_color='#000000'):
    return ft.Container(
        content=ft.Text(
            text, size=13, weight=ft.FontWeight.BOLD, color=text_color),
        bgcolor=bg_color,
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
    )


STATUS_COLORS = {
    "active": (STATUS_GREEN, "#ffffff"),
    "inactive": (STATUS_RED, "#ffffff"),
}


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


def table_header_row():
    def col(text, width):
        return ft.Container(
            ft.Text(text, size=18, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD),
            width=width,
        )

    return ft.Container(
        content=ft.Row([
            col("S-ID", 70),
            col("Name", 150),
            col("POC", 120),
            col("Contact #", 140),
            col("Address", 140),
            col("Email", 130),
            col("Status", 100),
            ft.Container(width=80),  # lines up with the action icons below
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        padding=ft.Padding.only(left=16, right=16, top=14, bottom=14),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def supplier_row(sid, name, poc, contact, address, email, status):
    status_bg, status_text = STATUS_COLORS.get(status.lower(), (STATUS_GREEN, "#ffffff"))

    def cell(text, width, color=TEXT_SECONDARY, bold=False):
        return ft.Container(
            ft.Text(
                text, size=15, color=color,
                weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
                max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
            ),
            width=width,
        )

    return ft.Container(
        content=ft.Row([
            cell(sid, 70, color=TEXT_PRIMARY, bold=True),
            cell(name, 150, color=TEXT_PRIMARY, bold=True),
            cell(poc, 120),
            cell(contact, 140),
            cell(address, 140),
            cell(email, 130),
            ft.Container(badge(status, status_bg, status_text), width=100, alignment=ft.alignment.Alignment(-1, 0)),
            ft.Container(
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.EDIT_ROUNDED,
                        icon_size=18,
                        icon_color=TEXT_PRIMARY,
                        tooltip="Edit supplier",
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_ROUNDED,
                        icon_size=18,
                        icon_color=STATUS_RED,
                        tooltip="Delete supplier",
                    ),
                ], spacing=0),
                width=80,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        border=ft.Border(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )


def build_suppliers_table():
    db_suppliers = supplier_model.get_suppliers()
    
    rows = [table_header_row()]
    
    for s in db_suppliers:
        rows.append(
            supplier_row(
                sid=f"S{s['supplier_id']:04d}", # Formats ID 1 as 'S0001'
                name=s["supplier_name"],
                poc=s["contact_person"],
                contact=s["contact_number"],
                address=s["address"],
                email=s["email"],
                status=s.get("status", "Active")
            )
        )

    return ft.Container(
        content=ft.Column(rows, spacing=0),
        border=ft.Border.all(1, BORDER_COLOR),
        border_radius=6,
    )


def supplier_management_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Supplier Management", on_nav)

    header = build_header()
    search_bar = build_search_bar()
    suppliers_table = build_suppliers_table()

    main_content = ft.Container(
        content=ft.Column([
            header, search_bar, suppliers_table], spacing=20, scroll=ft.ScrollMode.AUTO,),
        expand=True,
        padding=24,
    )

    return ft.Row(
        [sidebar, main_content],
        expand=True,
        spacing=0,
    )