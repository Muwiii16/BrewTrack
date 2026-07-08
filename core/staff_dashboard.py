# core/staff_dashboard.py
import flet as ft
from core.theme import *
from core.dashboard import (
    build_sidebar,
    build_header,
    build_stats_row,
    build_low_stock_card,
    build_purchase_orders_bar,
    stat_card,
)


def build_staff_header(user_name):
    breadcrumb = ft.Row([
        ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=18, color=TEXT_SECONDARY),
        ft.Text("Receiving/Stock-In", size=14, color=TEXT_PRIMARY),
    ], spacing=4,)

    title = ft.Text("Receiving/Stock-In", size=28,
                    color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD)

    subtitle = ft.Text(
        "Items running low, ranked by urgency. Log usage as you go and flag items for your manager to reorder",
        size=13, color=TEXT_SECONDARY,
    )

    return ft.Column([breadcrumb, title, subtitle], spacing=6,)


def build_staff_stats_row():
    """TEMP placeholder numbers - swap for real model queries later."""
    return ft.Row([
        stat_card("Out of Stock", "1", ""),
        stat_card("Critical", "1", ""),
        stat_card("Low", "4", ""),
        stat_card("Items to Watch", "5", ""),
    ], spacing=16,)


def staff_dashboard_view(page: ft.Page, user, on_logout, on_nav):
    sidebar = build_sidebar(page, user, on_logout, "Dashboard", on_nav)

    header = build_header(user["full_name"])
    stats_row = build_stats_row()
    low_stock_card = build_low_stock_card()
    po_bar = build_purchase_orders_bar()

    cards_row = ft.Row(
        [low_stock_card],
        spacing=16,
    )

    main_content = ft.Container(
        content=ft.Column(
            [header, stats_row, cards_row, po_bar],
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
