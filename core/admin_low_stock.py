import flet as ft
from core.theme import *
from core.components import _summary_card, _badge, _cell

def AdminLowStock(page: ft.Page, open_new_po_modal):
    action_bar = ft.Row(
        alignment="spaceBetween",
        controls=[
            ft.TextField(
                hint_text="Search",
                hint_style=ft.TextStyle(color=TEXT_MUTED, size=13),
                prefix_icon=ft.Icons.SEARCH,
                bgcolor=INPUT_BG,
                border_color=ft.Colors.TRANSPARENT,
                border_radius=8,
                content_padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
                height=40,
                width=300,
            ),
            ft.Container(
                bgcolor=ACCENT,
                border_radius=8,
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                ink=True,
                on_click=open_new_po_modal,
                content=ft.Text(
                    "New Purchase Order",
                    size=13,
                    weight="bold",
                    color=PANEL_LEFT_BG, 
                )
            )
        ]
    )

    table = ft.DataTable(
        expand=True,
        bgcolor=ft.Colors.TRANSPARENT,
        border=ft.Border.all(1, CARD_BORDER),
        border_radius=8,
        heading_row_color="#1A1A1A",
        heading_row_height=50,
        data_row_min_height=60,
        data_row_max_height=60,
        column_spacing=40,
        columns=[
            ft.DataColumn(ft.Text("Item", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Supplier", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("On Hand", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Reorder At", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Suggested Qty.", size=15, weight="bold", color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Status", size=15, weight="bold", color=TEXT_PRIMARY)),
        ],
        rows=[
            ft.DataRow(cells=[_cell("Coffee Bean", True), _cell("ABC Company"), _cell("145 kg"), _cell("150 kg"), _cell("350 kg"), ft.DataCell(_badge("Low", "#332400", ACCENT))]),
            ft.DataRow(cells=[_cell("Matcha Powder", True), _cell("ABC Company"), _cell("120 g"), _cell("150 g"), _cell("250 g"), ft.DataCell(_badge("Low", "#332400", ACCENT))]),
            ft.DataRow(cells=[_cell("Oatmilk", True), _cell("ABC Company"), _cell("1 L"), _cell("3 L"), _cell("5 boxes"), ft.DataCell(_badge("Low", "#332400", ACCENT))]),
            ft.DataRow(cells=[_cell("Vanilla Syrup", True), _cell("ZXC Farm"), _cell("2 L"), _cell("5 L"), _cell("10 bottles"), ft.DataCell(_badge("Low", "#332400", ACCENT))]),
        ]
    )

    return ft.Column(
        expand=True,
        scroll="auto",
        spacing=30,
        controls=[
            ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=20, color=TEXT_MUTED),
                            ft.Text("Low-Stocks Alert", size=14, color=TEXT_MUTED, weight="bold")
                        ]
                    ),
                    ft.Container(height=10),
                    ft.Text("Low-Stocks Alert", size=28, weight="bold", color=TEXT_PRIMARY),
                    ft.Text("Items at or below their reorder level. Replenish these to avoid production stoppages", size=12, color=TEXT_MUTED),
                ]
            ),
            ft.Row(
                spacing=20,
                controls=[
                    _summary_card("Items Needing Attention", "7"),
                    _summary_card("Out of Stock", "0"),
                    _summary_card("Estimated Replenishment Cost", "P 33,470.7"),
                ]
            ),
            action_bar,
            ft.Container(
                expand=True,
                content=ft.Column(
                    scroll="auto",
                    controls=[table]
                )
            )
        ]
    )