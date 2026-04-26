import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Practice 11")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)

font = pygame.font.Font(None, 32)

# Player car
player = pygame.Rect(175, 500, 50, 80)
player_speed = 5

# Enemy car
enemy = pygame.Rect(random.randint(60, 290), -100, 50, 80)
enemy_speed = 5

# Score
coins = 0
level = 1

# After every N coins, enemy speed increases
N = 5

# Coin data
coin_radius = 15
coin_x = random.randint(70, 330)
coin_y = random.randint(-500, -50)

# Coin can have different weights
coin_weight = random.choice([1, 2, 3])


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > 40:
        player.x -= player_speed

    if keys[pygame.K_RIGHT] and player.right < WIDTH - 40:
        player.x += player_speed

    # Move enemy down
    enemy.y += enemy_speed

    # If enemy goes outside screen, create new enemy position
    if enemy.y > HEIGHT:
        enemy.y = -100
        enemy.x = random.randint(60, 290)

    # Move coin down
    coin_y += 4

    # If coin goes outside screen, create new coin with new weight
    if coin_y > HEIGHT:
        coin_y = random.randint(-500, -50)
        coin_x = random.randint(70, 330)
        coin_weight = random.choice([1, 2, 3])

    # Coin rectangle for collision
    coin_rect = pygame.Rect(
        coin_x - coin_radius,
        coin_y - coin_radius,
        coin_radius * 2,
        coin_radius * 2
    )

    # Check collision with enemy
    if player.colliderect(enemy):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Check collision with coin
    if player.colliderect(coin_rect):
        coins += coin_weight

        # Increase enemy speed when player earns N coins
        if coins // N + 1 > level:
            level += 1
            enemy_speed += 1

        # Generate new coin
        coin_y = random.randint(-500, -50)
        coin_x = random.randint(70, 330)
        coin_weight = random.choice([1, 2, 3])

    # Draw background
    screen.fill(GREEN)

    # Draw road
    pygame.draw.rect(screen, GRAY, (40, 0, WIDTH - 80, HEIGHT))

    # Draw middle road line
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

    # Draw player and enemy
    pygame.draw.rect(screen, RED, player)
    pygame.draw.rect(screen, BLACK, enemy)

    # Draw coin
    if coin_weight == 1:
        coin_color = YELLOW
    elif coin_weight == 2:
        coin_color = ORANGE
    else:
        coin_color = WHITE

    pygame.draw.circle(screen, coin_color, (coin_x, coin_y), coin_radius)

    # Draw coin weight number
    weight_text = font.render(str(coin_weight), True, BLACK)
    screen.blit(weight_text, (coin_x - 7, coin_y - 10))

    # Draw score
    text = font.render(f"Coins: {coins}  Level: {level}", True, WHITE)
    screen.blit(text, (170, 20))

    pygame.display.update()