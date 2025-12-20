import flet as ft
import random


def main(page: ft.Page):
    """
    Main function that sets up the Minesweeper game UI and logic.
    This is the entry point for the Flet application.
    """
    # Set up the page properties
    page.title = "Minesweeper UI"  # Window title
    page.bgcolor = "#C0C0C0"  # Classic gray background (like old Windows Minesweeper)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Center content vertically
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Center content horizontally
    page.theme_mode = ft.ThemeMode.LIGHT  # Use light theme

    # Define color constants for the classic Minesweeper look
    DARK_GRAY = "#808080"  # Dark gray for pressed borders
    LIGHT_GRAY = "#C0C0C0"  # Light gray for background and raised borders
    RED = "#FF0000"  # Red for the counter displays
    BLACK = "#000000"  # Black for text and icons
    DARK_RED = "#800000"  # Dark red (not used but available)

    # Define emoji strings for game elements
    flag_str: str = "🚩"  # Flag emoji for marking suspected mines
    mine_str: str = "💣"  # Mine emoji for revealed mines

    # Game configuration
    rows: int = 8  # Number of rows in the grid
    cols: int = 8  # Number of columns in the grid
    mine_percentage: float = 0.15  # Percentage of cells that will be mines (15% = easy)

    # === UI SETUP SECTION ===
    # Create the outer container with sunken border effect (classic Minesweeper look)
    outer_container = ft.Container(
        padding=10,  # Space around the inner content
        bgcolor=LIGHT_GRAY,  # Background color
        border=ft.border.all(2, DARK_GRAY),  # Dark gray border on all sides for sunken effect
        border_radius=0,  # Sharp corners (classic look)
    )

    # Create the inner container with raised border effect
    inner_container = ft.Container(
        padding=10,  # Space around the game content
        bgcolor=LIGHT_GRAY,  # Background color
        border=ft.border.only(  # Different colors on different sides for 3D effect
            left=ft.border.BorderSide(2, "#FFFFFF"),  # White on left and top (light source)
            top=ft.border.BorderSide(2, "#FFFFFF"),
            right=ft.border.BorderSide(2, DARK_GRAY),  # Dark gray on right and bottom (shadow)
            bottom=ft.border.BorderSide(2, DARK_GRAY),
        ),
        border_radius=0,  # Sharp corners
    )

    # Create the top panel container (holds mine counter, smiley, and timer)
    top_panel_container = ft.Container(
        width=300,  # Fixed width for the panel
        height=50,  # Fixed height for the panel
        bgcolor=LIGHT_GRAY,  # Background color
        border=ft.border.only(  # Sunken border effect for the panel
            left=ft.border.BorderSide(2, DARK_GRAY),
            top=ft.border.BorderSide(2, DARK_GRAY),
            right=ft.border.BorderSide(2, "#FFFFFF"),
            bottom=ft.border.BorderSide(2, "#FFFFFF"),
        ),
        content=ft.Row(  # Layout for the three elements in the panel
            controls=[],  # Will be populated below
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Space elements evenly
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Center vertically
            spacing=20,  # Space between elements
        ),
        padding=ft.padding.only(left=10, right=10),  # Padding inside the panel
    )

    # Create the mine counter display (shows remaining mines)
    mine_counter_bg = ft.Container(
        width=60,  # Fixed width
        height=40,  # Fixed height
        bgcolor=BLACK,  # Black background (classic Minesweeper style)
        border_radius=0,  # Sharp corners
        content=ft.Text(  # The text showing the mine count
            "010",  # Default display value
            size=28,  # Large text
            weight="bold",  # Bold font
            color=RED,  # Red text (classic style)
            font_family="Courier New",  # Monospace font for even spacing
            text_align=ft.TextAlign.CENTER,  # Center the text
        ),
        alignment=ft.alignment.center,  # Center the text in the container
        padding=2,  # Small padding around the text
    )

    # Create the timer counter display (shows elapsed time)
    timer_counter_bg = ft.Container(
        width=60,  # Fixed width
        height=40,  # Fixed height
        bgcolor=BLACK,  # Black background (matches mine counter)
        border_radius=0,  # Sharp corners
        content=ft.Text(  # The text showing the elapsed time
            "000",  # Default display value
            size=28,  # Large text
            weight="bold",  # Bold font
            color=RED,  # Red text (matches mine counter)
            font_family="Courier New",  # Monospace font for even spacing
            text_align=ft.TextAlign.CENTER,  # Center the text
        ),
        alignment=ft.alignment.center,  # Center the text in the container
        padding=2,  # Small padding around the text
    )

    # Create the smiley button (game state indicator and reset button)
    smiley_button = ft.Container(
        width=40,  # Fixed width
        height=40,  # Fixed height
        bgcolor=LIGHT_GRAY,  # Background color
        border=ft.border.only(  # Raised border effect (opposite of sunken)
            left=ft.border.BorderSide(2, "#FFFFFF"),  # White on left and top
            top=ft.border.BorderSide(2, "#FFFFFF"),
            right=ft.border.BorderSide(2, DARK_GRAY),  # Dark gray on right and bottom
            bottom=ft.border.BorderSide(2, DARK_GRAY),
        ),
        content=ft.IconButton(  # The actual clickable button
            icon=ft.Icons.SENTIMENT_SATISFIED,  # Happy face icon
            icon_size=28,  # Icon size
            icon_color=BLACK,  # Icon color
            on_click=lambda e: print("Smiley clicked!"),  # Click handler (placeholder)
            style=ft.ButtonStyle(  # Button styling
                padding=0,  # No extra padding
                shape=ft.RoundedRectangleBorder(radius=0),  # Sharp corners
            ),
        ),
        alignment=ft.alignment.center,  # Center the button in the container
    )

    # Add the three elements to the top panel
    top_panel_container.content.controls = [
        mine_counter_bg,  # Left: Mine counter
        smiley_button,    # Center: Smiley/reset button
        timer_counter_bg, # Right: Timer
    ]

    # Create the menu bar for game options
    menubar = ft.MenuBar(
        expand=False,  # Don't expand to full width
        style=ft.MenuStyle(  # Styling for the menu
            bgcolor=LIGHT_GRAY,  # Background color
            alignment=ft.alignment.top_left,  # Align to top left
        ),
        controls=[  # Menu items
            ft.SubmenuButton(  # Main "Game" menu
                content=ft.Text("Game", size=12, weight="bold"),  # Menu label
                controls=[  # Submenu items
                    ft.MenuItemButton(  # 8x8 grid option
                        content=ft.Text("8x8"),
                        on_click=lambda e: change_grid_size("8x8"),  # Call function when clicked
                    ),
                    ft.MenuItemButton(  # 16x16 grid option
                        content=ft.Text("16x16"),
                        on_click=lambda e: change_grid_size("16x16"),
                    ),
                    ft.MenuItemButton(  # 24x24 grid option
                        content=ft.Text("24x24"),
                        on_click=lambda e: change_grid_size("24x24"),
                    ),
                    ft.MenuItemButton(  # 30x16 expert grid option
                        content=ft.Text("30x16 (Expert)"),
                        on_click=lambda e: change_grid_size("30x16 (Expert)"),
                    ),
                ],
            ),
        ],
    )

    # === GAME LOGIC FUNCTIONS SECTION ===
    # Function to create a single cell (3D button effect)
    def create_cell(row: int = 0, col: int = 0, has_mine: bool = False):
        """
        Creates a single cell for the Minesweeper grid.
        Each cell is a clickable button with 3D border effects.
        """
        # Create the cell container with 3D border effect (raised appearance)
        cell = ft.Container(
            width=20,  # Cell width in pixels
            height=20,  # Cell height in pixels
            # Store cell data: (row, col, has_mine, is_revealed, is_flagged)
            data=(row, col, has_mine, False, False),
            bgcolor=LIGHT_GRAY,  # Background color
            border=ft.border.only(  # 3D border effect
                left=ft.border.BorderSide(2, "#FFFFFF"),  # White on left and top (light)
                top=ft.border.BorderSide(2, "#FFFFFF"),
                right=ft.border.BorderSide(2, DARK_GRAY),  # Dark gray on right and bottom (shadow)
                bottom=ft.border.BorderSide(2, DARK_GRAY),
            ),
            alignment=ft.alignment.center,  # Center content in the cell
        )
        
        # Wrap the cell with GestureDetector to handle both left and right clicks
        gesture_detector = ft.GestureDetector(
            content=cell,  # The cell is the content of the gesture detector
            on_tap=lambda e: on_cell_click(e),  # Left click handler
            on_secondary_tap=lambda e: on_right_click(e),  # Right click handler
        )
        
        return gesture_detector

    # Function to create the entire grid of cells
    def create_grid(rows, cols):
        """
        Creates the complete Minesweeper grid by arranging cells in rows and columns.
        """
        # Create the grid container with sunken border effect
        grid = ft.Container(
            bgcolor=LIGHT_GRAY,  # Background color
            border=ft.border.only(  # Sunken border effect (opposite of cell borders)
                left=ft.border.BorderSide(2, DARK_GRAY),
                top=ft.border.BorderSide(2, DARK_GRAY),
                right=ft.border.BorderSide(2, "#FFFFFF"),
                bottom=ft.border.BorderSide(2, "#FFFFFF"),
            ),
            padding=4,  # Small padding around the cells
            content=ft.Column(  # Vertical arrangement of rows
                controls=[  # Create each row
                    ft.Row(  # Horizontal arrangement of cells in a row
                        controls=[create_cell(row, col, False) for col in range(cols)],  # Create cells for this row
                        spacing=0,  # No space between cells
                    )
                    for row in range(rows)  # Create all rows
                ],
                spacing=0,  # No space between rows
            ),
        )
        # Center the grid horizontally
        return ft.Row([grid], alignment=ft.MainAxisAlignment.CENTER)

    # Create the default grid based on initial rows and cols
    grid_container = ft.Container(content=create_grid(rows, cols))

    # Create container for the menu bar (positioned below the game)
    menubar_container = ft.Container(
        content=ft.Row(
            controls=[
                menubar,  # The menu bar content
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Center the menu bar
        ),
        padding=ft.padding.only(top=10),  # Space above the menu bar
    )

    # Create the main game container that holds everything
    game_container = ft.Container(
        content=ft.Column(  # Vertical layout
            controls=[
                top_panel_container,  # Top panel with counters and smiley
                ft.Container(height=10),  # Small space between panel and grid
                grid_container,  # The actual game grid
            ],
            spacing=0,  # No space between elements
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center everything horizontally
        ),
        # This container will center its content vertically and horizontally
        alignment=ft.alignment.center,
    )

    # === ALL FUNCTIONS GROUPED TOGETHER ===
    
    # Function to set cell border state (up or down)
    def set_cell_border(cell, state):
        """
        Set cell border to create 3D effect.
        state: 'up' for raised effect, 'down' for pressed effect
        """
        if state == 'up':
            # Raised border (normal state)
            cell.border = ft.border.only(
                left=ft.border.BorderSide(2, "#FFFFFF"),
                top=ft.border.BorderSide(2, "#FFFFFF"),
                right=ft.border.BorderSide(2, DARK_GRAY),
                bottom=ft.border.BorderSide(2, DARK_GRAY),
            )
        elif state == 'down':
            # Pressed border (clicked state)
            cell.border = ft.border.only(
                left=ft.border.BorderSide(2, DARK_GRAY),
                top=ft.border.BorderSide(2, DARK_GRAY),
                right=ft.border.BorderSide(2, "#FFFFFF"),
                bottom=ft.border.BorderSide(2, "#FFFFFF"),
            )

    # Function to count adjacent mines for a cell
    def count_adjacent_mines(row, col):
        """Count the number of mines in the 8 neighboring cells without revealing them"""
        count = 0
        # Check all 8 neighboring cells
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:  # Skip the cell itself
                    continue
                nr, nc = row + dr, col + dc
                # Check if neighbor is within bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Get the gesture detector, then access the cell container
                    gesture_detector = grid_container.content.controls[0].content.controls[nr].controls[nc]
                    neighbor_cell = gesture_detector.content
                    if neighbor_cell.data[2]:  # If neighbor has a mine
                        count += 1
                    # IMPORTANT: Do NOT reveal the mine, just count it!
        return count

    # Function to reveal a single cell
    def reveal_cell(cell):
        """Reveal a single cell and set its content"""
        if cell.data[3] or cell.data[4]:  # Already revealed or flagged
            return
        
        # Mark as revealed
        cell.data = (cell.data[0], cell.data[1], cell.data[2], True, cell.data[4])
        
        # Set border to pressed state
        set_cell_border(cell, 'down')
        
        # If it's a mine, DO NOT reveal it during flood fill
        # Mines should only be revealed when clicked directly by player
        if cell.data[2]:
            # Don't show mine during flood fill - keep it hidden
            cell.content = None
        else:
            # Count adjacent mines
            adjacent_mines = count_adjacent_mines(cell.data[0], cell.data[1])
            if adjacent_mines > 0:
                # Show the number
                cell.content = ft.Text(str(adjacent_mines), size=9)
            # If 0 mines, don't show anything (empty cell)

    # Recursive flood fill function for revealing cells
    def flood_fill(row, col):
        """Recursively reveal cells starting from (row, col)"""
        # Check bounds
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return
        
        # Get the gesture detector, then access the cell container
        gesture_detector = grid_container.content.controls[0].content.controls[row].controls[col]
        cell = gesture_detector.content
        
        # Skip if already revealed or flagged
        if cell.data[3] or cell.data[4]:
            return
        
        # Reveal this cell
        reveal_cell(cell)
        
        # Count adjacent mines for this cell
        adjacent_mines = count_adjacent_mines(row, col)
        
        # If this cell has 0 adjacent mines, recursively check neighbors
        if adjacent_mines == 0:
            # Check all 8 neighboring cells
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:  # Skip the cell itself
                        continue
                    nr, nc = row + dr, col + dc
                    flood_fill(nr, nc)  # Recursive call

        
    # Function to show game over popup
    def show_game_over_popup():
        """Show game over dialog when player steps on a mine"""
        def on_reset_click(e):
            page.close(dialog)
            reset_game()
            page.update()
        
        def on_close_click(e):
            page.close(dialog)
            page.update()
        
        # Create the dialog
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("💥 Game Over!", size=20, weight="bold"),
            content=ft.Text("You stepped on a mine! Better luck next time.", size=16),
            actions=[
                ft.TextButton("Try Again", on_click=on_reset_click),
                ft.TextButton("Close", on_click=on_close_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Open the dialog using page.open()
        page.open(dialog)

    # Function to show win popup
    def show_win_popup():
        """Show victory dialog when player wins"""
        def on_reset_click(e):
            page.close(dialog)
            reset_game()
            page.update()
        
        def on_close_click(e):
            page.close(dialog)
            page.update()
        
        # Create the dialog
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("🎉 Congratulations!", size=20, weight="bold"),
            content=ft.Text("You found all the safe cells! You're a Minesweeper master!", size=16),
            actions=[
                ft.TextButton("Play Again", on_click=on_reset_click),
                ft.TextButton("Close", on_click=on_close_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Open the dialog using page.open()
        page.open(dialog)

    # Function to reset the game
    def reset_game():
        """Reset the game to initial state"""
        # Reset smiley button
        smiley_button.content.icon = ft.Icons.SENTIMENT_SATISFIED
        smiley_button.content.icon_color = BLACK
        
        # Recreate the grid
        grid_container.content = create_grid(rows, cols)
        
        # Place new mines
        place_mines(rows, cols)
        
        # Update mine counter (placeholder - would need actual mine count)
        mine_counter_bg.content.value = f"{int(rows * cols * mine_percentage):03d}"
        
        # Reset timer counter (placeholder)
        timer_counter_bg.content.value = "000"
        
        page.update()

    # Function to check if player has won
    def check_win():
        """Check if all non-mine cells are revealed"""
        total_cells = rows * cols
        revealed_count = 0
        
        # Count all revealed cells
        for r in range(rows):
            for c in range(cols):
                gesture_detector = grid_container.content.controls[0].content.controls[r].controls[c]
                cell = gesture_detector.content
                if cell.data[3]:  # is_revealed
                    revealed_count += 1
        
        # Calculate number of non-mine cells
        non_mine_cells = total_cells - sum(1 for r in range(rows) for c in range(cols) 
                                         if grid_container.content.controls[0].content.controls[r].controls[c].content.data[2])
        
        # Player wins if all non-mine cells are revealed
        if revealed_count >= non_mine_cells:
            print("🎉 Player wins!")
            # Change smiley to winning face
            smiley_button.content.icon = ft.Icons.SENTIMENT_VERY_SATISFIED
            smiley_button.content.icon_color = ft.Colors.YELLOW
            show_win_popup()
            return True
        return False

    # Function to handle left mouse click (cell reveal)
    def on_cell_click(e):
        """
        Handle left mouse click on a cell.
        
        This function determines what happens when a player clicks on a cell:
        1. Check if cell is already revealed or flagged (if so, do nothing)
        2. If it's a mine: Game Over! Show mine and display game over popup
        3. If it has adjacent mines: Just reveal that single cell
        4. If it has 0 adjacent mines: Use flood fill to reveal large area
        5. Check if player has won after revealing cells
        """
        # Get the actual cell container from the gesture detector
        cell = e.control.content
        
        # Don't process if already revealed or flagged
        if cell.data[3] or cell.data[4]:  # is_revealed or is_flagged
            return
            
        # Get row and column from cell data
        row, col = cell.data[0], cell.data[1]
        
        # Check if it's a mine - Game Over!
        if cell.data[2]:  # has_mine
            print(f"Cell {cell.data} clicked! Mine exploded!")
            cell.content = ft.Text(mine_str, size=9)  # Show mine emoji
            set_cell_border(cell, 'down')  # Set pressed border
            # Change smiley to dead face to indicate game over
            smiley_button.content.icon = ft.Icons.SENTIMENT_VERY_DISSATISFIED
            smiley_button.content.icon_color = ft.Colors.RED
            show_game_over_popup()  # Show game over dialog
            return  # Exit early - game is over
        
        # Count adjacent mines for the clicked cell
        adjacent_mines = count_adjacent_mines(row, col)
        
        # Decide what to do based on adjacent mine count
        if adjacent_mines == 0:
            # No adjacent mines - use flood fill to reveal large area
            flood_fill(row, col)
        else:
            # Has adjacent mines - just reveal this single cell
            reveal_cell(cell)
        
        # Check if player has won after revealing cells
        check_win()
        
        # Update the page to show changes
        page.update()

    # Function to handle right mouse click (flag placement)
    def on_right_click(e):
        """
        Handle right mouse click on a cell (flag placement/removal).
        
        This function handles the flagging mechanic:
        1. Get the cell from the gesture detector
        2. Only allow flagging if cell is not revealed
        3. If no flag: place a flag
        4. If flag exists: remove the flag
        5. Update the cell data to track flag state
        """
        # Get the actual cell container from the gesture detector
        cell = e.control.content
        
        # Only allow flagging if cell is not revealed
        if not cell.data[3]:  # If not revealed (data[3] = is_revealed)
            # Toggle flag on right click
            if cell.content is None or cell.content.value != flag_str:
                # Place flag
                cell.content = ft.Text(flag_str, size=9)  # Show flag emoji
                # Update data tuple: (row, col, has_mine, is_revealed, is_flagged)
                cell.data = (cell.data[0], cell.data[1], cell.data[2], cell.data[3], True)  # Set is_flagged to True
            else:
                # Remove flag
                cell.content = None  # Clear the flag emoji
                # Update data tuple: (row, col, has_mine, is_revealed, is_flagged)
                cell.data = (cell.data[0], cell.data[1], cell.data[2], cell.data[3], False)  # Set is_flagged to False
        
        # Update the page to show changes
        page.update()

    # Function to handle grid size change from menu
    def change_grid_size(size):
        """
        Change the grid size based on menu selection.
        
        This function updates the game dimensions and recreates the grid.
        It preserves the mine percentage but adjusts the total number of mines.
        """
        # Use nonlocal to modify the outer scope variables
        nonlocal rows, cols
        
        # Set new dimensions based on menu selection
        if size == "8x8":
            rows, cols = 8, 8
        elif size == "16x16":
            rows, cols = 16, 16
        elif size == "24x24":
            rows, cols = 24, 24
        elif size == "30x16 (Expert)":
            rows, cols = 16, 30  # Note: rows=16, cols=30 for expert
        else:
            # Default fallback
            rows, cols = 8, 8
        
        # Update the grid with new dimensions
        grid_container.content = create_grid(rows, cols)
        page.update()
        # Place new mines for the new grid size
        place_mines(rows, cols)

    # Place mines randomly
    def place_mines(rows, cols):
        """
        Place mines randomly in the grid.
        
        This function:
        1. Calculates how many mines to place based on grid size and mine percentage
        2. Randomly selects positions for the mines
        3. Updates the cell data to mark those positions as having mines
        4. Preserves any existing reveal/flag states (for game resets)
        """
        # Calculate number of mines to place
        num_mines = int(rows * cols * mine_percentage)
        # Randomly select mine positions (without replacement)
        mines_position = random.sample(range(rows * cols), num_mines)
        print(f"Placing {num_mines} mines at positions: {mines_position}")
        
        # Place mines at the selected positions
        for pos in mines_position:
            r = pos // cols  # Convert linear position to row
            c = pos % cols   # Convert linear position to column
            print(f"Mine at row {r}, col {c}")
            
            # Get the gesture detector, then access the cell container
            gesture_detector = grid_container.content.controls[0].content.controls[r].controls[c]
            cell = gesture_detector.content
            
            # Update data tuple: (row, col, has_mine, is_revealed, is_flagged)
            # Set has_mine to True, preserve existing reveal and flag states
            cell.data = (r, c, True, cell.data[3], cell.data[4])  # Mark cell as having a mine, preserve reveal/flag states

    # === END OF FUNCTIONS ===

    # === FINAL LAYOUT AND INITIALIZATION SECTION ===
    
    # Create the main layout container that includes the menubar at the top
    main_layout = ft.Column(
        controls=[
            # MenuBar at the top left
            ft.Container(
                content=menubar,
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(bottom=5),  # Space between menu and game
            ),
            # Game area below the menubar
            ft.Container(
                content=outer_container,  # The outer container holds everything
                alignment=ft.alignment.center,  # Center the game area
                expand=True,  # Take up remaining space
            ),
        ],
        spacing=0,  # No space between menu and game area
        expand=True,  # Expand to fill the page
    )

    # Put game container in inner container
    inner_container.content = game_container

    # Put inner container in outer container
    outer_container.content = inner_container

    # Add the main layout to the page
    page.add(main_layout)

    # Initialize mines in the grid
    place_mines(rows, cols)


# === APPLICATION ENTRY POINT ===
if __name__ == "__main__":
    """
    This is the entry point for running the Minesweeper application.
    When this script is run directly (not imported), it will start the Flet app.
    """
    ft.app(target=main)  # Start the Flet application with the main function
