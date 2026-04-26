import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 400
HEIGHT = 600

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Clock controls FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

# Font for coin score
font = pygame.font.Font(None, 36)

# Player car
player_width = 50
player_height = 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 5

# Enemy car
enemy_width = 50
enemy_height = 80
enemy_x = random.randint(50, WIDTH - 100)
enemy_y = -100
enemy_speed = 5

# Coin
coin_radius = 15
coin_x = random.randint(60, WIDTH - 60)
coin_y = random.randint(-500, -50)
coin_speed = 4

# Collected coins
coins = 0

# Game loop
running = True
while running:

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Move player left
    if keys[pygame.K_LEFT] and player_x > 40:
        player_x -= player_speed

    # Move player right
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width - 40:
        player_x += player_speed

    # Move enemy down
    enemy_y += enemy_speed

    # If enemy goes down, return it to top
    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(50, WIDTH - 100)

    # Move coin down
    coin_y += coin_speed

    # If coin goes down, return it to random top position
    if coin_y > HEIGHT:
        coin_y = random.randint(-500, -50)
        coin_x = random.randint(60, WIDTH - 60)

    # Create rectangles for collision
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    coin_rect = pygame.Rect(coin_x - coin_radius, coin_y - coin_radius,
                            coin_radius * 2, coin_radius * 2)

    # Check collision with enemy
    if player_rect.colliderect(enemy_rect):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Check collision with coin
    if player_rect.colliderect(coin_rect):
        coins += 1
        coin_y = random.randint(-500, -50)
        coin_x = random.randint(60, WIDTH - 60)

    # Draw background
    screen.fill(GREEN)

    # Draw road
    pygame.draw.rect(screen, GRAY, (40, 0, WIDTH - 80, HEIGHT))

    # Draw road middle line
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

    # Draw player
    pygame.draw.rect(screen, RED, player_rect)

    # Draw enemy
    pygame.draw.rect(screen, BLACK, enemy_rect)

    # Draw coin
    pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), coin_radius)

    # Draw coin score in top right corner
    coin_text = font.render(f"Coins: {coins}", True, WHITE)
    screen.blit(coin_text, (WIDTH - 130, 20))

    # Update screen
    pygame.display.update()

    # FPS limit
    clock.tick(FPS)


