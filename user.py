import flet as ft

# Color Palette Definitions
BG_DARK = "#0D0A08"        # Deep black/brown background
BG_CARD = "#16110E"        # Main content area dark brown
TEXT_MAIN = "#FFFFFF"      # Pure white headers
TEXT_MUTED = "#8E837A"     # Muted grey-brown for subtexts/labels
ACCENT_ORANGE = "#F0B440"  # Golden/Orange for "Add User" and brand highlights
COLOR_OWNER = "#473820"    # Dark gold background for Owner badge
TEXT_OWNER = "#F0B440"     # Gold text for Owner badge
COLOR_STAFF = "#122A2F"    # Dark teal background for Staff badge
TEXT_STAFF = "#27C2D6"     # Teal text for Staff badge
COLOR_ACTIVE = "#16331C"   # Dark green background for Active badge
TEXT_ACTIVE = "#4CD964"    # Green text for Active status

def main(page: ft.Page):
    page.title = "ADMIN User Management - BrewTrack"
    page.bgcolor = BG_DARK
    page.padding = 0
    page.window.width = 1200
    page.window.height = 750

    # --- SIDEBAR COMPONENTS ---
    
    # Logo Area (Fixed text, alignment, padding, and borders)
    logo_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("BUT FIRST, COFFEE", size=10, color=ACCENT_ORANGE, weight=ft.FontWeight.BOLD),
                ft.Text("BREWTRACK", size=22, color=TEXT_MAIN, weight=ft.FontWeight.W_900),
            ],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.Alignment(0.0, 0.0), 
        padding=ft.Padding.only(top=30, bottom=30),
        border=ft.Border.only(bottom=ft.BorderSide(1, "#261D17"))
    )

    def sidebar_header(text: str):
        return ft.Container(
            content=ft.Text(text, size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_500),
            padding=ft.Padding.only(left=20, top=15, bottom=5)
        )

    def sidebar_item(text: str, is_active: bool = False):
        return ft.Container(
            content=ft.Text(
                text, 
                size=13, 
                color=TEXT_MAIN, 
                weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.W_400
            ),
            padding=ft.Padding.only(left=30, top=6, bottom=6),
            bgcolor="#1A1410" if is_active else None, 
        )

    # Sidebar Navigation List
    nav_items = ft.Column(
        controls=[
            sidebar_header("Overview"),
            sidebar_item("Dashboard"),
            
            sidebar_header("Master Records"),
            sidebar_item("User Management", is_active=True),
            sidebar_item("Suppliers"),
            sidebar_item("Ingredients & Supplies"),
            
            sidebar_header("Operations"),
            sidebar_item("Inventory Monitoring"),
            sidebar_item("Low- Stock Alerts"),
            sidebar_item("Purchase Orders"),
            sidebar_item("Movement History"),
            
            sidebar_header("Transactions"),
            sidebar_item("Receiving/ Stock-In"),
            sidebar_item("Stock-Out/ Usage"),
            sidebar_item("Daily Sales"),
            
            sidebar_header("Insights"),
            sidebar_item("Reports"),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO
    )

    # User Profile Bar (Bottom of Sidebar)
    user_profile = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(name="account_circle", color=TEXT_MAIN, size=36),
                        ft.Column(
                            controls=[
                                ft.Text("Juan Dela Cruz", size=13, color=TEXT_MAIN, weight=ft.FontWeight.BOLD),
                                ft.Text("Owner/ Admin", size=11, color=TEXT_MUTED),
                            ],
                            spacing=0
                        )
                    ],
                    spacing=10
                ),
                ft.IconButton(icon=ft.icons.LOGOUT_ROUNDED, icon_color=ACCENT_ORANGE, icon_size=20)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.Padding.all(20),
        border=ft.Border.only(top=ft.BorderSide(1, "#261D17")),
    )

    # Assemble Sidebar Layout
    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                logo_section,
                ft.Container(content=nav_items, expand=True),
                user_profile
            ],
            spacing=0
        ),
        width=240,
        bgcolor=BG_DARK,
        border=ft.Border.only(right=ft.BorderSide(1, "#261D17"))
    )

    # --- MAIN CONTENT COMPONENTS ---
    
    # Top mini breadcrumb header
    top_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon("chrome_reader_mode_outlined", color=TEXT_MUTED, size=18),
                ft.Text("User Management", color=TEXT_MUTED, size=14, weight=ft.FontWeight.W_600)
            ],
            spacing=8
        ),
        padding=ft.Padding.only(left=25, top=15, bottom=15),
        border=ft.Border.only(bottom=ft.BorderSide(1, "#261D17"))
    )

    # Title & Add Button Bar
    title_bar = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text("User Management", size=28, color=TEXT_MAIN, weight=ft.FontWeight.BOLD),
                    ft.Text("Manage staff and admin accounts and their access", size=12, color=TEXT_MUTED)
                ],
                spacing=2
            ),
            ft.ElevatedButton(
                text="Add User",
                bgcolor=ACCENT_ORANGE,
                color=BG_DARK,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=6),
                    text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=13)
                ),
                height=36
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Search Bar (FIXED: ft.Icons -> ft.icons)
    search_input = ft.TextField(
        hint_text="Search",
        hint_style=ft.TextStyle(color="#544B44", size=13),
        prefix_icon=ft.icons.SEARCH,  
        icon_color="#544B44",
        bgcolor="#1C1612",
        border_color="#2A211B",
        border_radius=6,
        height=36,
        width=240,
        content_padding=ft.Padding.only(left=10, right=10),
    )

    # Custom Badge helper
    def create_badge(text: str, bg_color: str, text_color: str):
        return ft.Container(
            content=ft.Text(text, color=text_color, size=11, weight=ft.FontWeight.BOLD),
            bgcolor=bg_color,
            padding=ft.Padding.symmetric(horizontal=12, vertical=4),
            border_radius=12
        )

    # User Table Header Row
    table_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Name", color=TEXT_MAIN, size=15, weight=ft.FontWeight.BOLD, expand=3),
                ft.Text("Email", color=TEXT_MAIN, size=15, weight=ft.FontWeight.BOLD, expand=4),
                ft.Text("Role", color=TEXT_MAIN, size=15, weight=ft.FontWeight.BOLD, expand=2),
                ft.Text("Status", color=TEXT_MAIN, size=15, weight=ft.FontWeight.BOLD, expand=2),
                ft.Container(expand=1) 
            ]
        ),
        padding=ft.Padding.symmetric(horizontal=15, vertical=12),
    )

    # Individual User Row Builder (FIXED: ft.Icons -> ft.icons)
    def create_table_row(name: str, email: str, role_badge: ft.Container, status_badge: ft.Container):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(name, color=TEXT_MAIN, size=15, weight=ft.FontWeight.BOLD, expand=3),
                    ft.Text(email, color=TEXT_MUTED, size=14, expand=4),
                    ft.Row([role_badge], expand=2, alignment=ft.MainAxisAlignment.START),
                    ft.Row([status_badge], expand=2, alignment=ft.MainAxisAlignment.START),
                    ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.icons.EDIT, icon_color=TEXT_MAIN, icon_size=18),
                            ft.IconButton(icon=ft.icons.DELETE, icon_color="#D93838", icon_size=18),
                        ],
                        expand=1,
                        spacing=0,
                        alignment=ft.MainAxisAlignment.END
                    )
                ]
            ),
            padding=ft.Padding.symmetric(horizontal=15, vertical=10),
            border=ft.Border.only(top=ft.BorderSide(1, "#261D17")),
        )

    # Table Grid Data Population
    user_table = ft.Container(
        content=ft.Column(
            controls=[
                table_header,
                create_table_row(
                    "Dana Whitfield", "owner@brewtrack.com", 
                    create_badge("Owner/ Admin", COLOR_OWNER, TEXT_OWNER), 
                    create_badge("Active", COLOR_ACTIVE, TEXT_ACTIVE)
                ),
                create_table_row(
                    "Marco Reyes", "staff@brewtrack.com", 
                    create_badge("Staff", COLOR_STAFF, TEXT_STAFF), 
                    create_badge("Active", COLOR_ACTIVE, TEXT_ACTIVE)
                ),
                create_table_row(
                    "Priya Nair", "priya@brewtrack.com", 
                    create_badge("Staff", COLOR_STAFF, TEXT_STAFF), 
                    create_badge("Active", COLOR_ACTIVE, TEXT_ACTIVE)
                ),
                create_table_row(
                    "Sam Okafor", "sam@brewtrack.com", 
                    create_badge("Staff", COLOR_STAFF, TEXT_STAFF), 
                    create_badge("Active", COLOR_ACTIVE, TEXT_ACTIVE)
                ),
                ft.Container(height=20, border=ft.Border.only(top=ft.BorderSide(1, "#261D17")))
            ],
            spacing=0
        ),
        border=ft.Border.all(1, "#261D17"),
        border_radius=6,
    )

    # Layout Assembly for Main Workspace Panel
    main_workspace = ft.Container(
        content=ft.Column(
            controls=[
                title_bar,
                ft.Container(height=15),
                search_input,
                ft.Container(height=15),
                user_table
            ],
            spacing=0,
            
        ),
        padding=25,
        expand=True
    )

    # Content Column joining layout headers and workspace
    content_area = ft.Column(
        controls=[
            top_header,
            main_workspace
        ],
        spacing=0,
        expand=True
    )

    # Final Layout Wrapper
    layout = ft.Row(
        controls=[
            sidebar,
            ft.Container(content=content_area, bgcolor=BG_CARD, expand=True)
        ],
        spacing=0,
        expand=True
    )

    page.add(layout)

ft.run(main)