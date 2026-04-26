import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 600
HEIGHT = 600

# Block size for snake and food
BLOCK = 20

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock controls speed
clock = pygame.time.Clock()

# Font for score and level
font = pygame.font.Font(None, 36)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)

# Snake starting position
snake = [(300, 300), (280, 300), (260, 300)]

# Snake movement
dx = BLOCK
dy = 0

# Score and level
score = 0
level = 1
speed = 7

# Wall border size
WALL = 20


# Function to generate food safely
def generate_food():
    while True:
        # Food must appear inside the walls
        x = random.randrange(WALL, WIDTH - WALL, BLOCK)
        y = random.randrange(WALL, HEIGHT - WALL, BLOCK)

        # Food must not appear on snake
        if (x, y) not in snake:
            return (x, y)


# First food
food = generate_food()

# Game loop
running = True
while running:

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard control
        if event.type == pygame.KEYDOWN:

            # Move left, but not if snake is moving right
            if event.key == pygame.K_LEFT and dx != BLOCK:
                dx = -BLOCK
                dy = 0

            # Move right, but not if snake is moving left
            elif event.key == pygame.K_RIGHT and dx != -BLOCK:
                dx = BLOCK
                dy = 0

            # Move up, but not if snake is moving down
            elif event.key == pygame.K_UP and dy != BLOCK:
                dx = 0
                dy = -BLOCK

            # Move down, but not if snake is moving up
            elif event.key == pygame.K_DOWN and dy != -BLOCK:
                dx = 0
                dy = BLOCK

    # Get current snake head
    head_x, head_y = snake[0]

    # Create new head position
    new_head = (head_x + dx, head_y + dy)

    # Check wall collision
    if (
        new_head[0] < WALL
        or new_head[0] >= WIDTH - WALL
        or new_head[1] < WALL
        or new_head[1] >= HEIGHT - WALL
    ):
        print("Game Over! Snake hit the wall.")
        pygame.quit()
        sys.exit()

    # Check snake collision with itself
    if new_head in snake:
        print("Game Over! Snake hit itself.")
        pygame.quit()
        sys.exit()

    # Add new head to snake
    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += 1

        # Every 3 foods, level increases
        if score % 3 == 0:
            level += 1
            speed += 2

        # Generate new safe food
        food = generate_food()

    else:
        # Remove tail if food is not eaten
        snake.pop()

    # Draw background
    screen.fill(BLACK)

    # Draw wall border
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, WALL))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - WALL, WIDTH, WALL))
    pygame.draw.rect(screen, GRAY, (0, 0, WALL, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - WALL, 0, WALL, HEIGHT))

    # Draw snake
    for part in snake:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], BLOCK, BLOCK))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK, BLOCK))

    # Draw score and level
    text = font.render(f"Score: {score}   Level: {level}", True, WHITE)
    screen.blit(text, (30, 30))

    # Update screen
    pygame.display.update()

    # Control game speed
    clock.tick(speed)