import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Initialize Pygame
pygame.init()


# ============================================================
# CUBE
# ============================================================

class Cube:
    def __init__(self, start, dir_x=1, dir_y=0, color=(255, 0, 0)):
        self.pos = start
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.color = color

    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y

        self.pos = (
            self.pos[0] + self.dir_x,
            self.pos[1] + self.dir_y
        )

    def draw(
        self,
        surface,
        cell_size,
        offset_x,
        offset_y,
        eyes=False
    ):
        x, y = self.pos

        pixel_x = offset_x + x * cell_size
        pixel_y = offset_y + y * cell_size

        # Draw the cube
        pygame.draw.rect(
            surface,
            self.color,
            (
                pixel_x + 1,
                pixel_y + 1,
                cell_size - 2,
                cell_size - 2
            )
        )

        # Draw the snake's eyes
        if eyes:
            center_y = pixel_y + cell_size // 2
            radius = max(2, cell_size // 10)

            eye_1 = (
                pixel_x + cell_size // 3,
                center_y - cell_size // 5
            )

            eye_2 = (
                pixel_x + (cell_size * 2) // 3,
                center_y - cell_size // 5
            )

            pygame.draw.circle(
                surface,
                (0, 0, 0),
                eye_1,
                radius
            )

            pygame.draw.circle(
                surface,
                (0, 0, 0),
                eye_2,
                radius
            )


# ============================================================
# SNAKE
# ============================================================

class Snake:

    def __init__(self, color, position):
        self.color = color

        # Snake body and direction changes
        self.body = []
        self.turns = {}

        # Create the snake head
        self.head = Cube(
            position,
            color=color
        )

        self.body.append(self.head)

        # Initial direction
        self.dir_x = 0
        self.dir_y = 1

    def move(self):

        # Handle window and keyboard events
        for event in pygame.event.get():

            # Close the game window
            if event.type == pygame.QUIT:
                return False

            # Handle keyboard input
            if event.type == pygame.KEYDOWN :

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.dir_x = -1
                    self.dir_y = 0

                    self.turns[self.head.pos[:]] = [
                        self.dir_x,
                        self.dir_y
                    ]

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.dir_x = 1
                    self.dir_y = 0

                    self.turns[self.head.pos[:]] = [
                        self.dir_x,
                        self.dir_y
                    ]

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.dir_x = 0
                    self.dir_y = -1

                    self.turns[self.head.pos[:]] = [
                        self.dir_x,
                        self.dir_y
                    ]

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.dir_x = 0
                    self.dir_y = 1

                    self.turns[self.head.pos[:]] = [
                        self.dir_x,
                        self.dir_y
                    ]

        # Move every segment of the snake
        for index, cube in enumerate(self.body):

            position = cube.pos[:]

            # Apply a stored direction change
            if position in self.turns:

                turn = self.turns[position]

                cube.move(
                    turn[0],
                    turn[1]
                )

                # Remove the turn after the tail has passed
                if index == len(self.body) - 1:
                    self.turns.pop(position)

            else:

                # Wrap around the left edge
                if cube.dir_x == -1 and cube.pos[0] <= 0:
                    cube.pos = (
                        GRID_SIZE - 1,
                        cube.pos[1]
                    )

                # Wrap around the right edge
                elif (
                    cube.dir_x == 1
                    and cube.pos[0] >= GRID_SIZE - 1
                ):
                    cube.pos = (
                        0,
                        cube.pos[1]
                    )

                # Wrap around the bottom edge
                elif (
                    cube.dir_y == 1
                    and cube.pos[1] >= GRID_SIZE - 1
                ):
                    cube.pos = (
                        cube.pos[0],
                        0
                    )

                # Wrap around the top edge
                elif cube.dir_y == -1 and cube.pos[1] <= 0:
                    cube.pos = (
                        cube.pos[0],
                        GRID_SIZE - 1
                    )

                # Normal movement
                else:
                    cube.move(
                        cube.dir_x,
                        cube.dir_y
                    )

        return True

    def reset(self, position):

        # Reset the snake body and turns
        self.body = []
        self.turns = {}

        # Create a new head
        self.head = Cube(
            position,
            color=self.color
        )

        self.body.append(self.head)

        # Reset direction
        self.dir_x = 0
        self.dir_y = 1

    def add_cube(self):

        # Get the current tail
        tail = self.body[-1]

        dir_x = tail.dir_x
        dir_y = tail.dir_y

        # Add the new cube behind the tail
        if dir_x == 1 and dir_y == 0:

            self.body.append(
                Cube(
                    (
                        tail.pos[0] - 1,
                        tail.pos[1]
                    ),
                    color=self.color
                )
            )

        elif dir_x == -1 and dir_y == 0:

            self.body.append(
                Cube(
                    (
                        tail.pos[0] + 1,
                        tail.pos[1]
                    ),
                    color=self.color
                )
            )

        elif dir_x == 0 and dir_y == 1:

            self.body.append(
                Cube(
                    (
                        tail.pos[0],
                        tail.pos[1] - 1
                    ),
                    color=self.color
                )
            )

        elif dir_x == 0 and dir_y == -1:

            self.body.append(
                Cube(
                    (
                        tail.pos[0],
                        tail.pos[1] + 1
                    ),
                    color=self.color
                )
            )

        # Set the new segment direction
        self.body[-1].dir_x = dir_x
        self.body[-1].dir_y = dir_y

    def draw(
        self,
        surface,
        cell_size,
        offset_x,
        offset_y
    ):

        # Draw every segment of the snake
        for index, cube in enumerate(self.body):

            cube.draw(
                surface,
                cell_size,
                offset_x,
                offset_y,
                eyes=(index == 0)
            )


# ============================================================
# GRID
# ============================================================

def draw_grid(
    surface,
    grid_size,
    cell_size,
    offset_x,
    offset_y
):
    grid_color = (60, 60, 60)

    # Draw vertical lines
    for index in range(grid_size + 1):

        x = offset_x + index * cell_size

        pygame.draw.line(
            surface,
            grid_color,
            (x, offset_y),
            (
                x,
                offset_y + grid_size * cell_size
            )
        )

    # Draw horizontal lines
    for index in range(grid_size + 1):

        y = offset_y + index * cell_size

        pygame.draw.line(
            surface,
            grid_color,
            (offset_x, y),
            (
                offset_x + grid_size * cell_size,
                y
            )
        )


# ============================================================
# DRAW GAME WINDOW
# ============================================================

def redraw_window(surface):

    # Clear the screen
    surface.fill((0, 0, 0))

    # Get the current window size
    window_width, window_height = surface.get_size()

    # Keep the game board square
    board_size = min(
        window_width,
        window_height
    )

    # Calculate the cell size
    cell_size = board_size // GRID_SIZE

    # Calculate the actual board size
    actual_board_size = cell_size * GRID_SIZE

    # Center the board inside the window
    offset_x = (
        window_width - actual_board_size
    ) // 2

    offset_y = (
        window_height - actual_board_size
    ) // 2

    # Draw the snake
    snake.draw(
        surface,
        cell_size,
        offset_x,
        offset_y
    )

    # Draw the food
    food.draw(
        surface,
        cell_size,
        offset_x,
        offset_y
    )

    # Draw the grid
    draw_grid(
        surface,
        GRID_SIZE,
        cell_size,
        offset_x,
        offset_y
    )

    # Update the display
    pygame.display.flip()


# ============================================================
# FOOD GENERATION
# ============================================================

def generate_food(snake):

    # Keep generating positions until an empty one is found
    while True:

        x = random.randrange(GRID_SIZE)
        y = random.randrange(GRID_SIZE)

        # Check if the position is occupied by the snake
        if any(
            cube.pos == (x, y)
            for cube in snake.body
        ):
            continue

        return (x, y)


# ============================================================
# MESSAGE BOX
# ============================================================

def show_message(title, message):

    # Create a temporary Tkinter window
    root = tk.Tk()

    # Keep the message box on top
    root.attributes(
        "-topmost",
        True
    )

    # Hide the main Tkinter window
    root.withdraw()

    # Display the message
    messagebox.showinfo(
        title,
        message
    )

    # Destroy the temporary window
    root.destroy()


# ============================================================
# MAIN GAME
# ============================================================

def main():

    global snake, food

    # Create a resizable Pygame window
    window = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        pygame.RESIZABLE
    )

    # Set the window title
    pygame.display.set_caption("Snake")

    # Create the snake
    snake = Snake(
        (255, 0, 0),
        (10, 10)
    )

    # Create the first food item
    food = Cube(
        generate_food(snake),
        color=(0, 255, 0)
    )

    # Create the game clock
    clock = pygame.time.Clock()

    running = True

    while running:

        # Handle movement and events
        running = snake.move()

        if not running:
            break

        # Check if the snake ate the food
        if snake.body[0].pos == food.pos:

            snake.add_cube()

            food = Cube(
                generate_food(snake),
                color=(0, 255, 0)
            )

        # Check for collision with the snake's body
        head_position = snake.body[0].pos

        for cube in snake.body[1:]:

            if head_position == cube.pos:

                score = len(snake.body)

                print("Score:", score)

                show_message(
                    "Game Over",
                    f"Score: {score}\n\nPlay again!"
                )

                # Reset the snake
                snake.reset((10, 10))

                break

        # Redraw the game
        redraw_window(window)

        # Limit the game FPS
        clock.tick(FPS)

    # Close Pygame
    pygame.quit()


# ============================================================
# GAME SETTINGS
# ============================================================

GRID_SIZE = 20
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 10


# ============================================================
# START GAME
# ============================================================

if __name__ == "__main__":
    main()