import pygame
import sys

# Initialize Pygame
pygame.init()

# Set constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Initialize the board
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Draw the grid
def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

# Draw X or O on the board
def draw_symbol(row, col, symbol):
    font = pygame.font.Font(None, 120)
    text_surface = font.render(symbol, True, RED if symbol == 'X' else BLUE)
    text_rect = text_surface.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
    screen.blit(text_surface, text_rect)

# Check for a win
def check_win(symbol):
    # Check rows and columns
    for i in range(GRID_SIZE):
        if all(board[i][j] == symbol for j in range(GRID_SIZE)) or all(board[j][i] == symbol for j in range(GRID_SIZE)):
            return True
    # Check diagonals
    if all(board[i][i] == symbol for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - i - 1] == symbol for i in range(GRID_SIZE)):
        return True
    return False

# Check for a tie
def check_tie():
    return all(board[i][j] != '' for i in range(GRID_SIZE) for j in range(GRID_SIZE))
# Draw the grid
def draw_grid():
    # Draw horizontal and vertical lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
    
    # Draw box lines
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.rect(screen, (0, 255, 0), (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)


# Main game loop
def main():
    current_player = 'X'
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE

                if board[row][col] == '':
                    board[row][col] = current_player
                    draw_symbol(row, col, current_player)

                    if check_win(current_player):
                        print(f"Player {current_player} wins!")
                        game_over = True
                    elif check_tie():
                        print("It's a tie!")
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

        draw_grid()
        pygame.display.update()

if __name__ == "__main__":
    main()
