import pygame
import sys
import time
import random

pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 400

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
light_green = (144, 238, 144)

# Grid and Snake block size
grid_size = 20
block_size = grid_size  # Ensure snake block size matches grid square size

# Font and clock
font_style = pygame.font.Font(None, 40)
score_font = pygame.font.Font(None, 25)
clock = pygame.time.Clock()

# Display
display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game by lyudmilov-georgedi')

# Load background image
background = pygame.Surface(display.get_size())
background.fill(light_green)

def draw_grid(surface):
    for y in range(0, screen_height, grid_size):
        for x in range(0, screen_width, grid_size):
            rect = pygame.Rect(x, y, grid_size, grid_size)
            pygame.draw.rect(surface, white, rect, 1)

def message(msg, color, y_displacement=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(screen_width / 2, screen_height / 2 + y_displacement))
    display.blit(mesg, text_rect)

def generate_food_position():
    # Generate random positions aligned with the grid size
    foodx = round(random.randrange(0, screen_width - block_size, grid_size))
    foody = round(random.randrange(0, screen_height - block_size, grid_size))
    return foodx, foody

def gameLoop():
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = grid_size  # Start with movement to the right
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx, foody = generate_food_position()

    while not game_over:

        while game_close == True:
            display.blit(background, (0, 0))
            message("Game Over! Press Q-Quit or C-Play Again", white, y_displacement=-50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:  # Ensure not moving horizontally
                    x1_change = -grid_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = grid_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:  # Ensure not moving vertically
                    y1_change = -grid_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = grid_size
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        display.blit(background, (0, 0))
        draw_grid(display)
        pygame.draw.rect(display, red, [foodx, foody, block_size, block_size])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for segment in snake_List:
            pygame.draw.rect(display, green, [segment[0], segment[1], block_size, block_size])

        # Display score
        score_text = score_font.render("Score: " + str(Length_of_snake - 1), True, black)
        display.blit(score_text, [10, 10])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food_position()
            Length_of_snake += 1

        clock.tick(10)

    pygame.quit()
    quit()

gameLoop()
