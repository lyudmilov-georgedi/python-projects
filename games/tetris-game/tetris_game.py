import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Shapes
SHAPES = [
    [['*', '*', '*', '*']],  # I shape
    [['*', '*', '*'], ['*', ' ', ' ']],  # L shape
    [['*', '*', '*'], [' ', ' ', '*']],  # J shape
    [['*', '*'], ['*', '*']],  # O shape
    [['*', '*', ' '], [' ', '*', '*']],  # S shape
    [[' ', '*', '*'], ['*', '*', ' ']],  # Z shape
    [['*', '*', '*'], [' ', '*', ' ']],  # T shape
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris game by lyudmilov-georgedi")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for displaying score
font = pygame.font.SysFont('Arial', 24)
large_font = pygame.font.SysFont('Arial', 28)

class Tetris:
    def __init__(self):
        self.board = [[0] * (SCREEN_WIDTH // GRID_SIZE) for _ in range(SCREEN_HEIGHT // GRID_SIZE)]
        self.current_shape = self.new_shape()
        self.shape_x = SCREEN_WIDTH // GRID_SIZE // 2 - len(self.current_shape[0]) // 2
        self.shape_y = 0
        self.game_over = False
        self.score = 0
        self.quit_requested = False

    def new_shape(self):
        return random.choice(SHAPES)

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell == '*':
                    pygame.draw.rect(screen, WHITE, pygame.Rect((self.shape_x + x) * GRID_SIZE, (self.shape_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def move_shape(self, dx, dy):
        if not self.collision(dx, dy):
            self.shape_x += dx
            self.shape_y += dy
        elif dy > 0:
            self.lock_shape()
            cleared_lines = self.clear_lines()
            self.score += cleared_lines * 100
            self.current_shape = self.new_shape()
            self.shape_x = SCREEN_WIDTH // GRID_SIZE // 2 - len(self.current_shape[0]) // 2
            self.shape_y = 0
            if self.collision(0, 0):
                self.game_over = True

    def rotate_shape(self):
        rotated_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        if not self.collision(0, 0, rotated_shape):
            self.current_shape = rotated_shape

    def collision(self, dx, dy, shape=None):
        if shape is None:
            shape = self.current_shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '*':
                    new_x = self.shape_x + x + dx
                    new_y = self.shape_y + y + dy
                    if new_x < 0 or new_x >= SCREEN_WIDTH // GRID_SIZE or new_y >= SCREEN_HEIGHT // GRID_SIZE:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
        return False

    def lock_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell == '*':
                    self.board[self.shape_y + y][self.shape_x + x] = 1

    def clear_lines(self):
        new_board = [row for row in self.board if not all(row)]
        cleared_lines = len(self.board) - len(new_board)
        for _ in range(cleared_lines):
            new_board.insert(0, [0] * (SCREEN_WIDTH // GRID_SIZE))
        self.board = new_board
        return cleared_lines

    def draw_board(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, WHITE, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def draw_quit_message(self):
        message1 = "Press R to Restart"
        message2 = "or Q to Quit"
        text_surface1 = large_font.render(message1, True, WHITE)
        text_surface2 = large_font.render(message2, True, WHITE)
        rect1 = text_surface1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        rect2 = text_surface2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(text_surface1, rect1)
        screen.blit(text_surface2, rect2)

    def run(self):
        while not self.quit_requested:
            screen.fill(BLACK)
            if not self.game_over:
                self.draw_board()
                self.draw_shape()
                self.draw_score()
            else:
                self.draw_quit_message()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_requested = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_shape(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_shape(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_shape(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_shape()
                    elif event.key == pygame.K_q:
                        if self.game_over:
                            self.quit_requested = True
                        else:
                            self.game_over = True
                    elif event.key == pygame.K_r and self.game_over:
                        self.__init__()

            if not self.game_over:
                self.move_shape(0, 1)
            clock.tick(4)

# Start the game
game = Tetris()
game.run()

pygame.quit()
