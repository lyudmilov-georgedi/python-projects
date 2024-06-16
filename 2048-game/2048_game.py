import pygame
import sys
import random

pygame.init()

SIZE = WIDTH, HEIGHT = 400, 400
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
FONT_SIZE = 40
FONT = pygame.font.Font(None, FONT_SIZE)
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("2048 Game by lyudmilov-georgedi")

def init_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

def add_new_tile(grid):
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if not empty_tiles:
        return
    r, c = random.choice(empty_tiles)
    grid[r][c] = 2 if random.random() < 0.9 else 4

def draw_grid(grid):
    screen.fill(BACKGROUND_COLOR)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            tile = grid[r][c]
            color = TILE_COLORS[tile]
            pygame.draw.rect(screen, color, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile != 0:
                text = FONT.render(str(tile), True, BLACK if tile < 8 else WHITE)
                text_rect = text.get_rect(center=(c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)
    pygame.display.flip()

def compress(grid):
    new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        pos = 0
        for c in range(GRID_SIZE):
            if grid[r][c] != 0:
                new_grid[r][pos] = grid[r][c]
                pos += 1
    return new_grid

def merge(grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r][c + 1] and grid[r][c] != 0:
                grid[r][c] *= 2
                grid[r][c + 1] = 0
    return grid

def reverse(grid):
    new_grid = []
    for r in grid:
        new_grid.append(r[::-1])
    return new_grid

def transpose(grid):
    new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            new_grid[r][c] = grid[c][r]
    return new_grid

def move_left(grid):
    new_grid = compress(grid)
    new_grid = merge(new_grid)
    new_grid = compress(new_grid)
    return new_grid

def move_right(grid):
    new_grid = reverse(grid)
    new_grid = move_left(new_grid)
    new_grid = reverse(new_grid)
    return new_grid

def move_up(grid):
    new_grid = transpose(grid)
    new_grid = move_left(new_grid)
    new_grid = transpose(new_grid)
    return new_grid

def move_down(grid):
    new_grid = transpose(grid)
    new_grid = move_right(new_grid)
    new_grid = transpose(new_grid)
    return new_grid

def is_game_over(grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                return False
            if r < GRID_SIZE - 1 and grid[r][c] == grid[r + 1][c]:
                return False
            if c < GRID_SIZE - 1 and grid[r][c] == grid[r][c + 1]:
                return False
    return True

def main():
    grid = init_grid()
    draw_grid(grid)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    grid = move_left(grid)
                elif event.key == pygame.K_RIGHT:
                    grid = move_right(grid)
                elif event.key == pygame.K_UP:
                    grid = move_up(grid)
                elif event.key == pygame.K_DOWN:
                    grid = move_down(grid)
                else:
                    continue
                
                add_new_tile(grid)
                draw_grid(grid)
                
                if is_game_over(grid):
                    print("Game Over!")
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
