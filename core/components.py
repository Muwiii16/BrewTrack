import flet as ft
from core.theme import *

def _sidebar_section_title(title: str):
    return ft.Container(
        padding=ft.Padding.only(top=10, bottom=5),
        content=ft.Text(title, size=11, color=TEXT_MUTED, weight="w500"),
    )

def _po_summary_card_small(title: str, value: str):
    return ft.Container(
        expand=1,
        padding=20,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(title, size=12, color=TEXT_MUTED),
                ft.Text(value, size=24, weight="bold", color=TEXT_PRIMARY),
            ]
        )
    )

def _badge(text: str, bg_color: str, fg_color: str):
    return ft.Container(
        bgcolor=bg_color,
        border_radius=12,
        padding=ft.Padding.symmetric(horizontal=12, vertical=4),
        content=ft.Text(
            text,
            size=11,
            weight="bold",
            color=fg_color
        )
    )

def _po_list_item(po_num, status, supplier, date_created, expected_date, amount, items_count, chips: list, on_approve=None, on_cancel=None):
    # Dynamic colors based on the actual PO status
    status_bg = "#332400" if status == "Pending" else ("#330000" if status == "Cancelled" else "#0A290A")
    status_fg = ACCENT if status == "Pending" else ("#F44336" if status == "Cancelled" else "#4CAF50")
    
    chip_controls = []
    for chip in chips:
        chip_controls.append(
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                border=ft.Border.all(1, CARD_BORDER),
                border_radius=16,
                content=ft.Text(chip, size=11, color=TEXT_MUTED)
            )
        )
        
    menu_items = []
    # Only show the Approve and Cancel options if the order is still Pending
    if status == "Pending":
        if on_approve:
            menu_items.append(ft.PopupMenuItem(content=ft.Text("Approve", color="#4CAF50"), on_click=on_approve))
        if on_cancel:
            menu_items.append(ft.PopupMenuItem(content=ft.Text("Cancel Order", color="#F44336"), on_click=on_cancel))
            
    # Hide the 3-dot menu entirely if there are no actions available (e.g., already Approved/Cancelled)
    actions_control = ft.PopupMenuButton(
        icon=ft.Icons.MORE_HORIZ,
        icon_color=TEXT_PRIMARY,
        items=menu_items
    ) if menu_items else ft.Container(width=40, height=40)
        
    return ft.Container(
        padding=20,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        content=ft.Row(
            alignment="spaceBetween",
            vertical_alignment="start",
            controls=[
                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.Text(po_num, size=16, weight="bold", color=TEXT_PRIMARY),
                                _badge(status, status_bg, status_fg)
                            ]
                        ),
                        ft.Text(f"{supplier} | Created {date_created} | Expected {expected_date}", size=12, color=TEXT_MUTED),
                        ft.Row(spacing=10, controls=chip_controls)
                    ]
                ),
                ft.Row(
                    spacing=20,
                    vertical_alignment="start",
                    controls=[
                        ft.Column(
                            horizontal_alignment="end",
                            spacing=4,
                            controls=[
                                ft.Text(amount, size=16, weight="bold", color=TEXT_PRIMARY),
                                ft.Text(f"{items_count} line item(s)", size=12, color=TEXT_MUTED)
                            ]
                        ),
                        actions_control
                    ]
                )
            ]
        )
    )

def _cell(text, is_bold=False, text_color=None):
    return ft.DataCell(ft.Text(text, size=13, weight="bold" if is_bold else "normal", color=text_color or TEXT_PRIMARY))

def _summary_card(title: str, value: str, subtitle: str = None):
    controls = [
        ft.Text(title, size=12, color=TEXT_MUTED),
        ft.Text(value, size=24, weight="bold", color=TEXT_PRIMARY),
    ]
    if subtitle:
        controls.append(ft.Text(subtitle, size=11, color=TEXT_MUTED))
        
    return ft.Container(
        expand=1,
        padding=20,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        bgcolor=ft.Colors.TRANSPARENT,
        content=ft.Column(
            spacing=4,
            controls=controls
        )
    )

def _panel_container(title: str, content_controls: list):
    return ft.Container(
        expand=1,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        padding=20,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    alignment="spaceBetween",
                    controls=[
                        ft.Text(title, size=18, weight="bold", color=TEXT_PRIMARY),
                        ft.Row(
                            spacing=4,
                            controls=[
                                ft.Text("View all", size=11, color=TEXT_MUTED),
                                ft.Icon(ft.Icons.ARROW_RIGHT_ALT, size=16, color=TEXT_MUTED)
                            ]
                        )
                    ]
                ),
                ft.Column(spacing=10, controls=content_controls)
            ]
        )
    )

def _low_stock_row(item_name: str, desc: str):
    
    return ft.Container(
        padding=15,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        content=ft.Row(
            alignment="spaceBetween",
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(item_name, size=14, weight="bold", color=TEXT_PRIMARY),
                        ft.Text(desc, size=11, color=TEXT_MUTED),
                    ]
                ),
                _badge("Low", "#332400", ACCENT)
            ]
        )
    )

def _movement_row(badge_text: str, badge_bg: str, badge_fg: str, title: str, desc: str, amount: str, amount_color: str):
    return ft.Container(
        padding=15,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        content=ft.Row(
            alignment="spaceBetween",
            controls=[
                ft.Row(
                    spacing=15,
                    controls=[
                        _badge(badge_text, badge_bg, badge_fg),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(title, size=14, weight="bold", color=TEXT_PRIMARY),
                                ft.Text(desc, size=11, color=TEXT_MUTED),
                            ]
                        )
                    ]
                ),
                ft.Text(amount, size=12, weight="bold", color=amount_color)
            ]
        )
    )

def _po_card(po_num: str, amount: str, status: str):
    return ft.Container(
        padding=15,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        content=ft.Row(
            spacing=15,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(po_num, size=14, weight="bold", color=TEXT_PRIMARY),
                        ft.Text(amount, size=11, color=TEXT_MUTED),
                    ]
                ),
                _badge(status, "#332400" if status == "Pending" else "#0A290A", ACCENT if status == "Pending" else "#4CAF50")
            ]
        )
    )