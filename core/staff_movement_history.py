import flet as ft
from core.theme import *
from core.components import _sidebar_section_title, _badge, _cell
from models import stock_movement_model

def staff_movement_history_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    
    sidebar_container = ft.Container(
        width=240, bgcolor=PANEL_LEFT_BG, padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )
    
    main_content = ft.Container(expand=True, padding=40, bgcolor=BG_COLOR)

    def navigate_to(e, view_name):
        if global_navigate_to:
            global_navigate_to(view_name)

    def build_sidebar(active_view: str):
        user_name = user["full_name"] if user else "Juan Dela Cruz"
        user_role = user["role"] if user else "Owner / Admin"

        def _sidebar_link(title: str):
            is_active = (title == active_view)
            return ft.Container(
                padding=ft.Padding.symmetric(vertical=6, horizontal=10), border_radius=6,
                bgcolor="#1A1A1A" if is_active else ft.Colors.TRANSPARENT, ink=True,
                on_click=lambda e: navigate_to(e, title),
                content=ft.Text(title, size=13, color=TEXT_PRIMARY if is_active else "#CCCCCC", weight="bold" if is_active else "normal"),
            )

        return ft.Column(
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

    data_table = ft.DataTable(
        expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8,
        heading_row_color="#1A1A1A", heading_row_height=50, data_row_min_height=60, data_row_max_height=60, column_spacing=40,
        columns=[
            ft.DataColumn(ft.Text("Date", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Item", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Type", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Qty Changed", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Resulting Stock", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("By", size=13, weight="bold", color=TEXT_MUTED)),
        ],
        rows=[]
    )

    def load_data():
        movements = stock_movement_model.get_recent_movements(limit=200)
        data_table.rows.clear()
        
        for mov in movements:
            m_type = mov['movement_type']
            
            if m_type == "Stock-In":
                badge_bg, badge_fg = "#0A290A", "#4CAF50"
                qty_str = f"+ {float(mov['quantity']):g}"
                qty_color = "#4CAF50"
            elif m_type == "Sale":
                badge_bg, badge_fg = "#002b2b", "#00BCD4"
                qty_str = f"- {float(mov['quantity']):g}"
                qty_color = "#00BCD4"
            elif m_type == "Stock-Out": # Stock-Out
                badge_bg, badge_fg = "#332400", ACCENT
                qty_str = f"- {float(mov['quantity']):g}"
                qty_color = ACCENT

            data_table.rows.append(ft.DataRow(cells=[
                _cell(mov['movement_date'].strftime("%b %d, %Y %I:%M %p")),
                _cell(mov['item_name'], is_bold=True),
                ft.DataCell(_badge(m_type, badge_bg, badge_fg)),
                _cell(qty_str, is_bold=True, text_color=qty_color),
                _cell(f"{float(mov['resulting_stock']):g}"),
                _cell(mov.get('full_name', 'System')),
            ]))
        page.update()

    main_content.content = ft.Column(
        expand=True, scroll="auto", spacing=30,
        controls=[
            ft.Column(spacing=4, controls=[
                ft.Row(spacing=8, controls=[ft.Icon(ft.Icons.HISTORY, size=20, color=TEXT_MUTED), ft.Text("Movement History", size=14, color=TEXT_MUTED, weight="bold")]),
                ft.Container(height=10),
                ft.Text("Movement History", size=28, weight="bold", color=TEXT_PRIMARY),
                ft.Text("Complete audit trail of every stock-in, stock-out, sale, and adjustment", size=12, color=TEXT_MUTED),
            ]),
            ft.TextField(hint_text="Search movements", prefix_icon=ft.Icons.SEARCH, bgcolor=INPUT_BG, border_color=ft.Colors.TRANSPARENT, border_radius=8, height=40, width=350, text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13), hint_style=ft.TextStyle(color=TEXT_MUTED, size=13), content_padding=ft.Padding.symmetric(horizontal=14, vertical=10)),
            ft.Container(expand=True, content=ft.Column(scroll="auto", controls=[data_table]))
        ]
    )

    sidebar_container.content = build_sidebar("Movement History")
    load_data()

    return ft.Container(expand=True, bgcolor=BG_COLOR, content=ft.Row(expand=True, spacing=0, controls=[sidebar_container, main_content]))