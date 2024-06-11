import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 540, 600
CELL_SIZE = WIDTH // 9

# Font settings
FONT_SIZE = 40
font = pygame.font.SysFont(None, FONT_SIZE)
# Function to draw the Sudoku grid
def draw_grid(screen, grid):
    screen.fill(WHITE)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                text_surface = font.render(str(grid[i][j]), True, BLACK)
                text_rect = text_surface.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text_surface, text_rect)
# Function to generate a Sudoku puzzle
def generate_sudoku():
    # Start with an empty grid
    grid = [[0] * 9 for _ in range(9)]

    # Solve the Sudoku puzzle
    solve_sudoku(grid)

    # Remove some numbers to create a puzzle
    empty_cells = random.randint(40, 50)
    for _ in range(empty_cells):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0

    return grid

# Function to solve Sudoku recursively using backtracking
def solve_sudoku(grid):
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0

    return False

# Function to find an empty cell in the grid
def find_empty_cell(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)
    return None

# Function to check if a move is valid
def is_valid_move(grid, row, col, num):
    # Check row
    if num in grid[row]:
        return False

    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False

    # Check 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False

    return True

# Function to draw the Sudoku grid
def draw_grid(screen, grid):
    screen.fill(WHITE)
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 4)
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT - CELL_SIZE), 4)
        else:
            pygame.draw.line(screen, GRAY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
            pygame.draw.line(screen, GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT - CELL_SIZE), 2)

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                text_surface = font.render(str(grid[i][j]), True, BLACK)
                text_rect = text_surface.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text_surface, text_rect)

# Function to check if the player's solution is correct
def check_solution(grid, solved_grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != solved_grid[i][j]:
                return False
    return True

# Main function
def main():
    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")

    # Generate Sudoku puzzle
    solved_grid = generate_sudoku()
    grid = [[solved_grid[i][j] for j in range(9)] for i in range(9)]

    # Main loop
    running = True
    selected_cell = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE
                if grid[row][col] == 0:
                    selected_cell = (row, col)

            if event.type == pygame.KEYDOWN:
                if selected_cell:
                    if event.unicode.isdigit() and solved_grid[selected_cell[0]][selected_cell[1]] == 0:
                        grid[selected_cell[0]][selected_cell[1]] = int(event.unicode)
                    elif event.key == pygame.K_BACKSPACE:
                        grid[selected_cell[0]][selected_cell[1]] = 0

        # Draw grid
        draw_grid(screen, grid)

        # Highlight selected cell
        if selected_cell:
            pygame.draw.rect(screen, RED, (selected_cell[1] * CELL_SIZE, selected_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

        # Check solution
        if check_solution(grid, solved_grid):
            text_surface = font.render("Congratulations! You solved the Sudoku!", True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - CELL_SIZE // 2))
            screen.blit(text_surface, text_rect)

        # Update display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
