import flet as ft
from core.theme import *
from core.components import _sidebar_section_title, _badge
from models import inventory_model, ingredient_model, stock_movement_model

def receiving_stock_in_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    
    sidebar_container = ft.Container(
        width=240, bgcolor=PANEL_LEFT_BG, padding=ft.Padding.symmetric(vertical=20, horizontal=20),
        border=ft.Border(right=ft.BorderSide(1, CARD_BORDER))
    )
    
    main_content = ft.Container(expand=True, padding=40, bgcolor=BG_COLOR)
    
    ingredients = ingredient_model.get_ingredients()

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
                        _sidebar_section_title("Master Records"), _sidebar_link("User Management"), _sidebar_link("Suppliers"), _sidebar_link("Ingredients & Supplies"),
                        _sidebar_section_title("Operations"), _sidebar_link("Inventory Monitoring"), _sidebar_link("Low-Stock Items"), _sidebar_link("Purchase Orders"), _sidebar_link("Movement History"),
                        _sidebar_section_title("Transactions"), _sidebar_link("Receiving/ Stock-In"), _sidebar_link("Stock-Out/ Usage"), _sidebar_link("Daily Sales"),
                        _sidebar_section_title("Insights"), _sidebar_link("Reports"),
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

    item_dropdown = ft.Dropdown(
        hint_text="Select Item",
        options=[ft.dropdown.Option(key=str(i['item_id']), text=i['item_name']) for i in ingredients],
        bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=45
    )
    quantity_field = ft.TextField(hint_text="0", bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=45)
    source_field = ft.TextField(hint_text="e.g. PO-1043 or Supplier Name", bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=45)

    recent_list_container = ft.Column(spacing=15)

    def load_recent_stock_ins():
        movements = stock_movement_model.get_recent_movements(limit=10)
        stock_ins = [m for m in movements if m['movement_type'] == 'Stock-In']
        
        recent_list_container.controls.clear()
        for s in stock_ins:
            recent_list_container.controls.append(
                ft.Row(
                    alignment="spaceBetween", vertical_alignment="start",
                    controls=[
                        ft.Column(spacing=4, controls=[
                            ft.Text(s['item_name'], size=14, color=TEXT_PRIMARY, weight="bold"),
                            ft.Text(s.get('notes', s.get('reference_type', 'No reference provided')), size=11, color=TEXT_MUTED),
                        ]),
                        ft.Column(horizontal_alignment="end", spacing=4, controls=[
                            ft.Text(f"+ {float(s['quantity']):g}", size=14, color="#4CAF50", weight="bold"),
                            ft.Text(s['movement_date'].strftime("%b %d, %I:%M %p"), size=11, color=TEXT_MUTED),
                        ])
                    ]
                )
            )
        page.update()

    def handle_stock_in(e):
        if not item_dropdown.value or not quantity_field.value:
            snack = ft.SnackBar(content=ft.Text("Item and Quantity are required."), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return
            
        try:
            inventory_model.stock_in(
                int(item_dropdown.value),
                float(quantity_field.value),
                user['user_id'] if user else 1,
                "Delivery",
                None,
                source_field.value
            )
            # Clear fields
            item_dropdown.value = None
            quantity_field.value = ""
            source_field.value = ""
            
            snack = ft.SnackBar(content=ft.Text("Inventory successfully updated!"), bgcolor=ft.Colors.GREEN_800)
            page.overlay.append(snack)
            snack.open = True
            load_recent_stock_ins()
        except Exception as ex:
            snack = ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    form_card = ft.Container(
        expand=1, padding=30, border=ft.Border.all(1, CARD_BORDER), border_radius=8,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text("Record Delivery", size=18, color=TEXT_PRIMARY, weight="bold"),
                ft.Container(height=5),
                ft.Column(spacing=4, controls=[ft.Text("Item *", size=12, weight="bold", color=TEXT_PRIMARY), item_dropdown]),
                ft.Column(spacing=4, controls=[ft.Text("Quantity Received *", size=12, weight="bold", color=TEXT_PRIMARY), quantity_field]),
                ft.Column(spacing=4, controls=[ft.Text("Source / Reference", size=12, weight="bold", color=TEXT_PRIMARY), source_field]),
                ft.Container(height=20),
                ft.Container(
                    bgcolor="#0A290A", padding=ft.Padding.symmetric(vertical=15), border_radius=8, ink=True, on_click=handle_stock_in,
                    content=ft.Row(alignment="center", controls=[ft.Text("Add to Inventory", size=13, weight="bold", color="#4CAF50")])
                )
            ]
        )
    )

    recent_card = ft.Container(
        expand=1, padding=30, border=ft.Border.all(1, CARD_BORDER), border_radius=8,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Recent Stock-In", size=18, color=TEXT_PRIMARY, weight="bold"),
                recent_list_container
            ]
        )
    )

    main_content.content = ft.Column(
        expand=True, scroll="auto", spacing=30,
        controls=[
            ft.Column(spacing=4, controls=[
                ft.Row(spacing=8, controls=[ft.Icon(ft.Icons.INPUT_ROUNDED, size=20, color=TEXT_MUTED), ft.Text("Receiving / Stock-In", size=14, color=TEXT_MUTED, weight="bold")]),
                ft.Container(height=10),
                ft.Text("Receiving / Stock-In", size=28, weight="bold", color=TEXT_PRIMARY),
                ft.Text("Log incoming deliveries to add them into inventory", size=12, color=TEXT_MUTED),
            ]),
            ft.Row(spacing=20, vertical_alignment="start", controls=[form_card, recent_card])
        ]
    )

    sidebar_container.content = build_sidebar("Receiving/ Stock-In")
    load_recent_stock_ins()

    return ft.Container(expand=True, bgcolor=BG_COLOR, content=ft.Row(expand=True, spacing=0, controls=[sidebar_container, main_content]))