import flet as ft
from core.theme import *
from core.components import _sidebar_section_title, _badge, _cell
from models import ingredient_model, supplier_model

def ingredients_supply_view(page: ft.Page, user=None, show_login=None, global_navigate_to=None):
    
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

    data_table = ft.DataTable(
        expand=True, bgcolor=ft.Colors.TRANSPARENT, border=ft.Border.all(1, CARD_BORDER), border_radius=8,
        heading_row_color="#1A1A1A", heading_row_height=50, data_row_min_height=60, data_row_max_height=60, column_spacing=25,
        columns=[
            ft.DataColumn(ft.Text("P-ID", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Item", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Category", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Unit", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Unit Cost", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Reorder At", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Supplier", size=13, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("Actions", size=13, weight="bold", color=TEXT_MUTED)),
        ],
        rows=[]
    )

    def load_data():
        ingredients = ingredient_model.get_ingredients()
        data_table.rows.clear()
        for i in ingredients:
            sup_name = i.get('supplier_name', 'Unassigned')
            data_table.rows.append(ft.DataRow(cells=[
                _cell(f"P-{i['item_id']:04d}", is_bold=True),
                _cell(i["item_name"], is_bold=True),
                _cell(i["category"]),
                _cell(i["unit_of_measurement"]),
                _cell(f"P {float(i['cost_per_unit']):.2f}"),
                _cell(f"{float(i['reorder_level']):g} {i['unit_of_measurement']}"),
                _cell(sup_name),
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE, icon_color="#F44336", tooltip="Delete Item",
                        on_click=lambda e, iid=i["item_id"]: delete_item(iid)
                    )
                )
            ]))
        page.update()

    def delete_item(item_id):
        # Add deletion logic here mapped to your model
        snack = ft.SnackBar(content=ft.Text("Item deleted successfully (mock)."), bgcolor=ft.Colors.GREEN_800)
        page.overlay.append(snack)
        snack.open = True
        load_data()

    def dialog_field(hint=""):
        return ft.TextField(
            hint_text=hint, bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY,
            hint_style=ft.TextStyle(color=TEXT_MUTED, size=13), text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13),
            border_radius=8, content_padding=ft.Padding.symmetric(horizontal=14, vertical=10), height=40,
        )

    item_name_field = dialog_field("e.g. Coffee Beans")
    reorder_at_field = dialog_field("e.g. 150")
    unit_field = dialog_field("e.g. kg, L, pcs")
    unit_cost_field = dialog_field("e.g. 100.00")
    
    category_dropdown = ft.Dropdown(
        hint_text="Select a category",
        options=[ft.dropdown.Option(c) for c in ["Coffee", "Dairy", "Syrup", "Packaging", "Powder"]],
        bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=45
    )
    
    supplier_dropdown = ft.Dropdown(
        hint_text="Assign Supplier",
        options=[], # Loaded dynamically
        bgcolor=INPUT_BG, border_color=INPUT_BORDER, focused_border_color=ACCENT, color=TEXT_PRIMARY, border_radius=8, height=45
    )

    def close_dialog(e=None):
        add_item_dialog.open = False
        page.update()

    def create_item(e=None):
        if not item_name_field.value or not category_dropdown.value:
            snack = ft.SnackBar(content=ft.Text("Item Name and Category are required."), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            return
            
        try:
            ingredient_model.add_ingredient(
                int(supplier_dropdown.value) if supplier_dropdown.value else None,
                item_name_field.value,
                category_dropdown.value,
                unit_field.value,
                float(unit_cost_field.value or 0),
                float(reorder_at_field.value or 0)
            )
            item_name_field.value = reorder_at_field.value = unit_field.value = unit_cost_field.value = ""
            category_dropdown.value = supplier_dropdown.value = None
            
            snack = ft.SnackBar(content=ft.Text("Item added successfully!"), bgcolor=ft.Colors.GREEN_800)
            page.overlay.append(snack)
            snack.open = True
            
            close_dialog()
            load_data()
        except Exception as ex:
            snack = ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED_800)
            page.overlay.append(snack)
            snack.open = True
            page.update()

    add_item_dialog = ft.AlertDialog(
        modal=True, bgcolor=PANEL_RIGHT_BG, shape=ft.RoundedRectangleBorder(radius=10),
        title=ft.Column(spacing=4, controls=[
            ft.Text("Add Item", size=24, color=TEXT_PRIMARY, weight="bold"),
            ft.Text("Define catalog details and reorder thresholds.", size=12, color=TEXT_MUTED),
        ]),
        content=ft.Container(
            width=500,
            content=ft.Column(spacing=15, tight=True, controls=[
                ft.Column(spacing=4, controls=[ft.Text("Item Name *", size=12, weight="bold", color=TEXT_PRIMARY), item_name_field]),
                ft.Row(spacing=15, controls=[
                    ft.Column(expand=1, spacing=4, controls=[ft.Text("Category *", size=12, weight="bold", color=TEXT_PRIMARY), category_dropdown]),
                    ft.Column(expand=1, spacing=4, controls=[ft.Text("Supplier", size=12, weight="bold", color=TEXT_PRIMARY), supplier_dropdown]),
                ]),
                ft.Row(spacing=15, controls=[
                    ft.Column(expand=1, spacing=4, controls=[ft.Text("Unit of Measure", size=12, weight="bold", color=TEXT_PRIMARY), unit_field]),
                    ft.Column(expand=1, spacing=4, controls=[ft.Text("Unit Cost", size=12, weight="bold", color=TEXT_PRIMARY), unit_cost_field]),
                    ft.Column(expand=1, spacing=4, controls=[ft.Text("Reorder Level", size=12, weight="bold", color=TEXT_PRIMARY), reorder_at_field]),
                ]),
            ])
        ),
        actions=[
            ft.TextButton("Cancel", style=ft.ButtonStyle(color=TEXT_MUTED), on_click=close_dialog),
            ft.Container(bgcolor=ACCENT, padding=ft.Padding.symmetric(horizontal=20, vertical=10), border_radius=8, ink=True, on_click=create_item, content=ft.Text("Create Item", size=13, weight="bold", color=PANEL_LEFT_BG))
        ]
    )

    def open_add_item_dialog(e=None):
        # Fetch real suppliers for the dropdown
        try:
            sups = supplier_model.get_suppliers()
            supplier_dropdown.options = [ft.dropdown.Option(key=str(s['supplier_id']), text=s['supplier_name']) for s in sups]
        except:
            pass
            
        if add_item_dialog not in page.overlay:
            page.overlay.append(add_item_dialog)
        add_item_dialog.open = True
        page.update()

    main_content.content = ft.Column(
        expand=True, scroll="auto", spacing=30,
        controls=[
            ft.Row(
                alignment="spaceBetween", vertical_alignment="start",
                controls=[
                    ft.Column(spacing=4, controls=[
                        ft.Row(spacing=8, controls=[ft.Icon(ft.Icons.KITCHEN, size=20, color=TEXT_MUTED), ft.Text("Ingredients & Supplies", size=14, color=TEXT_MUTED, weight="bold")]),
                        ft.Container(height=10),
                        ft.Text("Ingredients & Supplies", size=28, weight="bold", color=TEXT_PRIMARY),
                        ft.Text("Master catalog of raw materials, packaging, and supplies", size=12, color=TEXT_MUTED),
                    ]),
                    ft.Container(bgcolor=ACCENT, border_radius=8, padding=ft.Padding.symmetric(horizontal=16, vertical=10), ink=True, on_click=open_add_item_dialog, content=ft.Text("+ Add Item", size=13, weight="bold", color=PANEL_LEFT_BG))
                ]
            ),
            ft.TextField(hint_text="Search items", prefix_icon=ft.Icons.SEARCH, bgcolor=INPUT_BG, border_color=ft.Colors.TRANSPARENT, border_radius=8, height=40, width=350, text_style=ft.TextStyle(color=TEXT_PRIMARY, size=13), hint_style=ft.TextStyle(color=TEXT_MUTED, size=13), content_padding=ft.Padding.symmetric(horizontal=14, vertical=10)),
            ft.Container(expand=True, content=ft.Column(scroll="auto", controls=[data_table]))
        ]
    )

    sidebar_container.content = build_sidebar("Ingredients & Supplies")
    load_data()

    return ft.Container(expand=True, bgcolor=BG_COLOR, content=ft.Row(expand=True, spacing=0, controls=[sidebar_container, main_content]))