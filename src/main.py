import flet as ft

def main(page: ft.Page):
    page.title = "Minesweeper UI"
    page.bgcolor = "#C0C0C0"  # Classic gray background
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # Classic Minesweeper colors
    DARK_GRAY = "#808080"
    LIGHT_GRAY = "#C0C0C0"
    RED = "#FF0000"
    BLACK = "#000000"
    DARK_RED = "#800000"

    # Outer border (sunken effect)
    outer_container = ft.Container(
        padding=10,
        bgcolor=LIGHT_GRAY,
        border=ft.border.all(2, DARK_GRAY),
        border_radius=0,
    )

    # Inner border (raised effect)
    inner_container = ft.Container(
        padding=10,
        bgcolor=LIGHT_GRAY,
        border=ft.border.only(
            left=ft.border.BorderSide(2, "#FFFFFF"),
            top=ft.border.BorderSide(2, "#FFFFFF"),
            right=ft.border.BorderSide(2, DARK_GRAY),
            bottom=ft.border.BorderSide(2, DARK_GRAY),
        ),
        border_radius=0,
    )

    # Top panel container (with sunken border)
    top_panel_container = ft.Container(
        width=300,
        height=50,
        bgcolor=LIGHT_GRAY,
        border=ft.border.only(
            left=ft.border.BorderSide(2, DARK_GRAY),
            top=ft.border.BorderSide(2, DARK_GRAY),
            right=ft.border.BorderSide(2, "#FFFFFF"),
            bottom=ft.border.BorderSide(2, "#FFFFFF"),
        ),
        content=ft.Row(
            controls=[],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=ft.padding.only(left=10, right=10),
    )

    # Mine counter (with black background like classic Minesweeper)
    mine_counter_bg = ft.Container(
        width=60,
        height=40,
        bgcolor=BLACK,
        border_radius=0,
        content=ft.Text(
            "010",
            size=28,
            weight="bold",
            color=RED,
            font_family="Courier New",  # Using standard monospace font
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=2,
    )

    # Timer counter (with black background)
    timer_counter_bg = ft.Container(
        width=60,
        height=40,
        bgcolor=BLACK,
        border_radius=0,
        content=ft.Text(
            "000",
            size=28,
            weight="bold",
            color=RED,
            font_family="Courier New",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=2,
    )

    # Smiley button (classic Minesweeper style)
    smiley_button = ft.Container(
        width=40,
        height=40,
        bgcolor=LIGHT_GRAY,
        border=ft.border.only(
            left=ft.border.BorderSide(2, "#FFFFFF"),
            top=ft.border.BorderSide(2, "#FFFFFF"),
            right=ft.border.BorderSide(2, DARK_GRAY),
            bottom=ft.border.BorderSide(2, DARK_GRAY),
        ),
        content=ft.IconButton(
            icon=ft.Icons.SENTIMENT_SATISFIED,
            icon_size=28,
            icon_color=BLACK,
            on_click=lambda e: print("Smiley clicked!"),
            style=ft.ButtonStyle(
                padding=0,
                shape=ft.RoundedRectangleBorder(radius=0),
            )
        ),
        alignment=ft.alignment.center,
    )

    # Populate the top panel container
    top_panel_container.content.controls = [
        mine_counter_bg,
        smiley_button,
        timer_counter_bg
    ]

    # Dropdown for grid size selection (styled to match)
    grid_size_dropdown = ft.Dropdown(
        label="Grid Size",
        label_style=ft.TextStyle(size=12, weight="bold"),
        options=[
            ft.dropdown.Option("8x8"),
            ft.dropdown.Option("16x16"),
            ft.dropdown.Option("24x24"),
            ft.dropdown.Option("30x16 (Expert)"),
        ],
        value="8x8",
        width=120,
        bgcolor="#FFFFFF",
        border_color=DARK_GRAY,
        focused_border_color=DARK_RED,
        text_size=12,
        content_padding=ft.padding.only(left=10),
    )

    # Function to create a single cell (3D button effect)
    def create_cell():
        return ft.Container(
            width=20,
            height=20,
            bgcolor=LIGHT_GRAY,
            border=ft.border.only(
                left=ft.border.BorderSide(2, "#FFFFFF"),
                top=ft.border.BorderSide(2, "#FFFFFF"),
                right=ft.border.BorderSide(2, DARK_GRAY),
                bottom=ft.border.BorderSide(2, DARK_GRAY),
            ),
            alignment=ft.alignment.center,
            on_click=lambda e: print("Cell clicked!"),
        )

    # Function to create the grid
    def create_grid(rows, cols):
        return ft.Container(
            bgcolor=LIGHT_GRAY,
            border=ft.border.only(
                left=ft.border.BorderSide(2, DARK_GRAY),
                top=ft.border.BorderSide(2, DARK_GRAY),
                right=ft.border.BorderSide(2, "#FFFFFF"),
                bottom=ft.border.BorderSide(2, "#FFFFFF"),
            ),
            padding=4,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[create_cell() for _ in range(cols)],
                        spacing=0,
                    ) for _ in range(rows)
                ],
                spacing=0,
            ),
        )

    # Create default grid
    grid_container = ft.Container(
        content=create_grid(8, 8)
    )

    # Dropdown container (centered below smiley)
    dropdown_container = ft.Container(
        content=ft.Row(
            controls=[
                grid_size_dropdown,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(top=10),
    )

    # Main game container - this will be centered
    game_container = ft.Container(
        content=ft.Column(
            controls=[
                top_panel_container,
                dropdown_container,
                ft.Container(height=10),  # Spacing
                grid_container,
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        # This container will center its content
        alignment=ft.alignment.center,
    )

    # Function to handle grid size change
    def on_grid_change(e):
        value = grid_size_dropdown.value
        if value == "8x8":
            rows, cols = 8, 8
        elif value == "16x16":
            rows, cols = 16, 16
        elif value == "24x24":
            rows, cols = 24, 24
        elif value == "30x16 (Expert)":
            rows, cols = 16, 30
        else:
            rows, cols = 8, 8
        
        # Update the grid
        grid_container.content = create_grid(rows, cols)
        page.update()

    grid_size_dropdown.on_change = on_grid_change

    # Put game container in inner container
    inner_container.content = game_container

    # Put inner container in outer container
    outer_container.content = inner_container

    # Create a centered container for the entire game
    centered_game = ft.Container(
        content=outer_container,
        alignment=ft.alignment.center,
        expand=True,  # This makes the container expand to fill available space
    )

    # Add to page
    page.add(centered_game)

if __name__ == "__main__":
    ft.app(target=main)