import pygame
import random
import sys
import time

pygame.init()

WIDTH = 600
HEIGHT = 600
BLOCK = 20
WALL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)

# Snake body
snake = [(300, 300), (280, 300), (260, 300)]

# Snake direction
dx = BLOCK
dy = 0

score = 0
speed = 7

# Food disappears after this many seconds
FOOD_TIME = 5


# Generate food that is not on wall and not on snake
def generate_food():
    while True:
        x = random.randrange(WALL, WIDTH - WALL, BLOCK)
        y = random.randrange(WALL, HEIGHT - WALL, BLOCK)

        if (x, y) not in snake:
            weight = random.choice([1, 2, 3])
            created_time = time.time()
            return x, y, weight, created_time


food_x, food_y, food_weight, food_created = generate_food()

running = True
while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx != BLOCK:
                dx = -BLOCK
                dy = 0

            elif event.key == pygame.K_RIGHT and dx != -BLOCK:
                dx = BLOCK
                dy = 0

            elif event.key == pygame.K_UP and dy != BLOCK:
                dx = 0
                dy = -BLOCK

            elif event.key == pygame.K_DOWN and dy != -BLOCK:
                dx = 0
                dy = BLOCK

    # If food lives too long, it disappears and new food appears
    if time.time() - food_created > FOOD_TIME:
        food_x, food_y, food_weight, food_created = generate_food()

    # New snake head
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Wall collision
    if (
        new_head[0] < WALL
        or new_head[0] >= WIDTH - WALL
        or new_head[1] < WALL
        or new_head[1] >= HEIGHT - WALL
    ):
        print("Game Over! Wall collision.")
        pygame.quit()
        sys.exit()

    # Self collision
    if new_head in snake:
        print("Game Over! Snake hit itself.")
        pygame.quit()
        sys.exit()

    # Add new head
    snake.insert(0, new_head)

    # If snake eats food
    if new_head == (food_x, food_y):
        score += food_weight

        # Speed can increase slowly with score
        if score % 5 == 0:
            speed += 1

        food_x, food_y, food_weight, food_created = generate_food()

    else:
        # Remove tail if food is not eaten
        snake.pop()

    # Draw background
    screen.fill(BLACK)

    # Draw walls
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, WALL))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - WALL, WIDTH, WALL))
    pygame.draw.rect(screen, GRAY, (0, 0, WALL, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - WALL, 0, WALL, HEIGHT))

    # Draw snake
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], BLOCK, BLOCK))

    # Food color depends on weight
    if food_weight == 1:
        food_color = RED
    elif food_weight == 2:
        food_color = YELLOW
    else:
        food_color = WHITE

    # Draw food
    pygame.draw.rect(screen, food_color, (food_x, food_y, BLOCK, BLOCK))

    # Draw food weight
    weight_text = font.render(str(food_weight), True, BLACK)
    screen.blit(weight_text, (food_x + 4, food_y))

    # Draw score
    time_left = int(FOOD_TIME - (time.time() - food_created))
    text = font.render(f"Score: {score}  Speed: {speed}  Food time: {time_left}", True, WHITE)
    screen.blit(text, (30, 30))

    pygame.display.update()