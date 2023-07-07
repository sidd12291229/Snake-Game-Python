import sys
import random
import pygame

# Disable Constant/Variable detection
# pylint: disable=C0103

pygame.init()
clock = pygame.time.Clock()

# Setup screen
SQUARE_SIZE = 18

SCREEN_CELLS_WIDTH = 40
SCREEN_CELLS_HEIGHT = 40
screen = pygame.display.set_mode((SCREEN_CELLS_WIDTH*SQUARE_SIZE, SCREEN_CELLS_HEIGHT*SQUARE_SIZE))

pause_font = pygame.font.SysFont('Helvetica', 100)
#pause_font = pygame.font.Font(None, 100)

# Misc static
FOOD_COLOR = (0, 200, 100)
snake = [(1, 1), (2, 1)]

obstacle = []
OBSTACLE_COLOR = (255, 255, 255)
new_obstacle = True

colors = [(255, 0, 0),
          (0, 255, 0),
          (0, 0, 255),
          (255, 128, 0),
          (128, 255, 0),
          (0, 128, 255)]
snake_color = colors[0]

PAUSE_BOX_WIDTH = 430
PAUSE_BOX_HEIGHT = 120
PAUSE_BOX_X = (SCREEN_CELLS_WIDTH*SQUARE_SIZE - PAUSE_BOX_WIDTH)/2
PAUSE_BOX_Y = (SCREEN_CELLS_HEIGHT*SQUARE_SIZE - PAUSE_BOX_HEIGHT)/2

# Position variables
snake_x = 0
snake_x_direction = 1
snake_y = 0
snake_y_direction = 0

food_x = random.randint(0, SCREEN_CELLS_WIDTH-1)
food_y = random.randint(0, SCREEN_CELLS_HEIGHT-1)

def end_game():
    print("Score:", len(snake))
    sys.exit(0)

def pause_game():
    pygame.draw.rect(screen, (0,0,0), (PAUSE_BOX_X, PAUSE_BOX_Y, PAUSE_BOX_WIDTH, PAUSE_BOX_HEIGHT))
    pygame.draw.rect(screen, (255,255,255),
                     (PAUSE_BOX_X, PAUSE_BOX_Y, PAUSE_BOX_WIDTH, PAUSE_BOX_HEIGHT), width=2)

    pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
    screen.blit(pause_text, (PAUSE_BOX_X+10, PAUSE_BOX_Y+20))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                end_game()
            elif e.type == pygame.KEYDOWN:
                # Quit
                if e.key in (pygame.K_q, pygame.K_ESCAPE):
                    end_game()
                else:
                    return

        clock.tick(10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()

            # change dir (WASD or arrow keys)
            if event.key in (pygame.K_a, pygame.K_LEFT) and snake_x_direction != 1:
                snake_x_direction = -1
                snake_y_direction = 0
            elif event.key in (pygame.K_d, pygame.K_RIGHT) and snake_x_direction != -1:
                snake_x_direction = 1
                snake_y_direction = 0
            elif event.key in (pygame.K_w, pygame.K_UP) and snake_y_direction != 1:
                snake_x_direction = 0
                snake_y_direction = -1
            elif event.key in (pygame.K_s, pygame.K_DOWN) and snake_y_direction != -1:
                snake_x_direction = 0
                snake_y_direction = 1

            # Pause
            if event.key in (pygame.K_p, pygame.K_SPACE):
                pause_game()

            # Quit
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                end_game()

    # Move the snake
    snake_x += snake_x_direction
    snake_y += snake_y_direction

    # detect collision
    if snake_x >= SCREEN_CELLS_WIDTH:
        end_game()
    elif snake_x < 0:
        end_game()
    elif snake_y >= SCREEN_CELLS_HEIGHT:
        end_game()
    elif snake_y < 0:
        end_game()
    elif (snake_x, snake_y) in snake:
        end_game()
    elif (snake_x, snake_y) in obstacle:
        end_game()

    # Move snake by adding new location to the end
    snake.append((snake_x, snake_y))

    # Did we eat food this time?
    if food_x == snake_x and food_y == snake_y:

        # find a place for the food that's not in the snake
        while True:
            food_x = random.randint(0, SCREEN_CELLS_WIDTH-1)
            food_y = random.randint(0, SCREEN_CELLS_HEIGHT-1)

            if (food_x, food_y) not in snake:
                break

        if len(snake) % 10 == 0:
            new_obstacle = True

    else:
        snake.pop(0) # Don't extend, if didn't eat anything

    # draw snake
    screen.fill((0, 0, 0)) # black background
    for s in snake:
        pygame.draw.rect(screen, snake_color,
                         pygame.Rect(s[0]*SQUARE_SIZE, s[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # draw obstacle
    if new_obstacle:
        obstacle = []
        for x in range(0, 10):
            obstacle_x = random.randint(0, SCREEN_CELLS_WIDTH-1)
            obstacle_y = random.randint(0, SCREEN_CELLS_HEIGHT-1)
            if (obstacle_x, obstacle_y) in snake:
                pass # obstacle was in snake
            elif (obstacle_x, obstacle_y) is (food_x, food_y):
                pass # obstacle was in food
            else:
                obstacle.append((obstacle_x, obstacle_y))

        new_obstacle = False

    for s in obstacle:
        pygame.draw.rect(screen, OBSTACLE_COLOR,
                         pygame.Rect(s[0]*SQUARE_SIZE, s[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # draw food
    pygame.draw.rect(screen, FOOD_COLOR,
                     pygame.Rect(food_x*SQUARE_SIZE, food_y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Update display
    pygame.display.flip()

    level = int(len(snake) / 10)
    snake_color = colors[level % len(colors)] # change snake color with level
    fps = 6 + (2*level) # get faster in later levels
    clock.tick(fps)
