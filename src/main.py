import flet as ft
import random


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

    flag_str: str = "🚩"
    mine_str: str = "💣"

    rows: int = 8
    cols: int = 8
    mine_percentage: float = 0.15  # Adjust based on difficulty

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
            ),
        ),
        alignment=ft.alignment.center,
    )

    # Populate the top panel container
    top_panel_container.content.controls = [
        mine_counter_bg,
        smiley_button,
        timer_counter_bg,
    ]

    # MenuBar for game options (styled to match)
    menubar = ft.MenuBar(
        expand=False,
        style=ft.MenuStyle(
            bgcolor=LIGHT_GRAY,
            alignment=ft.alignment.top_left,
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Game", size=12, weight="bold"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("8x8"),
                        on_click=lambda e: change_grid_size("8x8"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("16x16"),
                        on_click=lambda e: change_grid_size("16x16"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("24x24"),
                        on_click=lambda e: change_grid_size("24x24"),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("30x16 (Expert)"),
                        on_click=lambda e: change_grid_size("30x16 (Expert)"),
                    ),
                ],
            ),
        ],
    )

    # Function to create a single cell (3D button effect)
    def create_cell(row: int = 0, col: int = 0, has_mine: bool = False):
        cell = ft.Container(
            width=20,
            height=20,
            data=(row, col, has_mine),
            bgcolor=LIGHT_GRAY,
            border=ft.border.only(
                left=ft.border.BorderSide(2, "#FFFFFF"),
                top=ft.border.BorderSide(2, "#FFFFFF"),
                right=ft.border.BorderSide(2, DARK_GRAY),
                bottom=ft.border.BorderSide(2, DARK_GRAY),
            ),
            alignment=ft.alignment.center,
            on_click=lambda e: on_cell_click(e),
        )
        return cell

    # Function to create the grid
    def create_grid(rows, cols):
        grid = ft.Container(
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
                        controls=[create_cell(row, col, False) for col in range(cols)],
                        spacing=0,
                    )
                    for row in range(rows)
                ],
                spacing=0,
            ),
        )
        return ft.Row([grid], alignment=ft.MainAxisAlignment.CENTER)

    # Create default grid
    grid_container = ft.Container(content=create_grid(rows, cols))

    # MenuBar container (centered below smiley)
    menubar_container = ft.Container(
        content=ft.Row(
            controls=[
                menubar,
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
                ft.Container(height=10),  # Spacing
                grid_container,
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        # This container will center its content
        alignment=ft.alignment.center,
    )

    # Function to handle cell click
    def on_cell_click(e):
        # Toggle border to create "pressed" effect
        current_left_color = e.control.border.left.color
        current_top_color = e.control.border.top.color

        # If currently in normal state (white on top/left), switch to pressed state
        if current_left_color == "#FFFFFF" and current_top_color == "#FFFFFF":
            # Change border to create "pressed" effect - swap white and dark borders
            e.control.border = ft.border.only(
                left=ft.border.BorderSide(2, DARK_GRAY),
                top=ft.border.BorderSide(2, DARK_GRAY),
                right=ft.border.BorderSide(2, "#FFFFFF"),
                bottom=ft.border.BorderSide(2, "#FFFFFF"),
            )
        else:
            # Restore original border
            e.control.border = ft.border.only(
                left=ft.border.BorderSide(2, "#FFFFFF"),
                top=ft.border.BorderSide(2, "#FFFFFF"),
                right=ft.border.BorderSide(2, DARK_GRAY),
                bottom=ft.border.BorderSide(2, DARK_GRAY),
            )

        if e.control.data[2]:  # If the cell has a mine
            print(f"Cell {e.control.data} clicked!")
            e.control.content = ft.Text(mine_str, size=9)
        # Add your cell reveal logic here
        page.update()

    # Function to handle grid size change
    def change_grid_size(size):
        nonlocal rows, cols
        if size == "8x8":
            rows, cols = 8, 8
        elif size == "16x16":
            rows, cols = 16, 16
        elif size == "24x24":
            rows, cols = 24, 24
        elif size == "30x16 (Expert)":
            rows, cols = 16, 30
        else:
            rows, cols = 8, 8
        
        # Update the grid
        grid_container.content = create_grid(rows, cols)
        page.update()
        place_mines(rows, cols)

    # Create a main layout container that includes the menubar at the top
    main_layout = ft.Column(
        controls=[
            # MenuBar at the top left
            ft.Container(
                content=menubar,
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(bottom=5),
            ),
            # Game area below the menubar
            ft.Container(
                content=outer_container,
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )

    # Put game container in inner container
    inner_container.content = game_container

    # Put inner container in outer container
    outer_container.content = inner_container

    # Add to page
    page.add(main_layout)

    # Place mines randomly
    def place_mines(rows, cols):
        num_mines = int(rows * cols * mine_percentage)
        mines_position = random.sample(range(rows * cols), num_mines)
        # print(mines_position)
        for pos in mines_position:
            r = pos // cols
            c = pos % cols
            # print(r, c)
            cell = grid_container.content.controls[0].content.controls[r].controls[c]
            cell.data = (r, c, True)  # Mark cell as having a mine

    place_mines(rows, cols)


if __name__ == "__main__":
    ft.app(target=main)
