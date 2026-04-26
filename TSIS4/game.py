import pygame
import random
from config import *
from db import save_game, get_personal_best


class SnakeGame:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings

        # FIXED: convert color name like "Green" to RGB
        self.snake_color = tuple(COLOR_OPTIONS[settings["snake_color"]])

        self.snake = [(200, 200), (180, 200), (160, 200)]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = self.direction

        self.score = 0
        self.level = 1
        self.food_eaten = 0

        self.speed = 8
        self.normal_speed = 8

        self.personal_best = get_personal_best(username)

        self.obstacles = []

        self.food = self.random_empty_cell()
        self.food_weight = random.choice([1, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()
        self.food_lifetime = 7000

        self.poison = self.random_empty_cell()

        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0

        self.powerup_active = None
        self.powerup_end_time = 0
        self.shield = False

        self.move_timer = 0
        self.game_over = False
        self.saved = False

    def random_empty_cell(self):
        while True:
            x = random.randrange(40, WIDTH - 40, CELL_SIZE)
            y = random.randrange(80, HEIGHT - 40, CELL_SIZE)
            pos = (x, y)

            if (
                pos not in self.snake
                and pos not in self.obstacles
                and pos != getattr(self, "food", None)
                and pos != getattr(self, "poison", None)
                and pos != getattr(self, "powerup", None)
            ):
                return pos

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, CELL_SIZE):
                self.next_direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and self.direction != (0, -CELL_SIZE):
                self.next_direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and self.direction != (CELL_SIZE, 0):
                self.next_direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-CELL_SIZE, 0):
                self.next_direction = (CELL_SIZE, 0)

    def update(self):
        if self.game_over:
            return

        now = pygame.time.get_ticks()
        self.update_powerups(now)

        self.move_timer += 1

        if self.move_timer < max(3, 18 - self.speed):
            return

        self.move_timer = 0
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if self.check_collision(new_head):
            if self.shield:
                self.shield = False
                self.powerup_active = None
                return
            else:
                self.end_game()
                return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.eat_food()

        elif new_head == self.poison:
            self.eat_poison()

        elif self.powerup and new_head == self.powerup:
            self.collect_powerup()
            self.snake.pop()

        else:
            self.snake.pop()

        if now - self.food_spawn_time > self.food_lifetime:
            self.spawn_food()

        if self.powerup is None and random.randint(1, 250) == 1:
            self.spawn_powerup()

        if self.powerup is not None:
            if now - self.powerup_spawn_time > 8000:
                self.powerup = None
                self.powerup_type = None

    def check_collision(self, pos):
        x, y = pos

        if x < 40 or x >= WIDTH - 40 or y < 80 or y >= HEIGHT - 40:
            return True

        if pos in self.snake:
            return True

        if pos in self.obstacles:
            return True

        return False

    def eat_food(self):
        self.score += self.food_weight
        self.food_eaten += 1

        if self.food_eaten % 5 == 0:
            self.level += 1
            self.normal_speed += 1
            self.speed = self.normal_speed

            if self.level >= 3:
                self.generate_obstacles()

        self.spawn_food()

    def eat_poison(self):
        for _ in range(2):
            if len(self.snake) > 1:
                self.snake.pop()

        if len(self.snake) <= 1:
            self.end_game()
            return

        self.poison = self.random_empty_cell()

    def spawn_food(self):
        self.food = self.random_empty_cell()
        self.food_weight = random.choice([1, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_powerup(self):
        self.powerup = self.random_empty_cell()
        self.powerup_type = random.choice(["speed", "slow", "shield"])
        self.powerup_spawn_time = pygame.time.get_ticks()

    def collect_powerup(self):
        now = pygame.time.get_ticks()

        if self.powerup_type == "speed":
            self.powerup_active = "Speed Boost"
            self.speed = self.normal_speed + 4
            self.powerup_end_time = now + 5000

        elif self.powerup_type == "slow":
            self.powerup_active = "Slow Motion"
            self.speed = max(4, self.normal_speed - 4)
            self.powerup_end_time = now + 5000

        elif self.powerup_type == "shield":
            self.powerup_active = "Shield"
            self.shield = True

        self.powerup = None
        self.powerup_type = None

    def update_powerups(self, now):
        if self.powerup_active in ["Speed Boost", "Slow Motion"]:
            if now > self.powerup_end_time:
                self.speed = self.normal_speed
                self.powerup_active = None

    def generate_obstacles(self):
        self.obstacles = []

        count = self.level + 2
        head = self.snake[0]

        safe_positions = [
            head,
            (head[0] + CELL_SIZE, head[1]),
            (head[0] - CELL_SIZE, head[1]),
            (head[0], head[1] + CELL_SIZE),
            (head[0], head[1] - CELL_SIZE),
        ]

        while len(self.obstacles) < count:
            pos = self.random_empty_cell()

            if pos not in safe_positions:
                self.obstacles.append(pos)

    def end_game(self):
        self.game_over = True

        if not self.saved:
            save_game(self.username, self.score, self.level)
            self.saved = True

    def draw_grid(self, screen):
        if not self.settings["grid"]:
            return

        for x in range(40, WIDTH - 40, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 80), (x, HEIGHT - 40))

        for y in range(80, HEIGHT - 40, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (40, y), (WIDTH - 40, y))

    def draw(self, screen):
        screen.fill(BLACK)

        pygame.draw.rect(screen, DARK_GRAY, (40, 80, WIDTH - 80, HEIGHT - 120))
        self.draw_grid(screen)

        for block in self.obstacles:
            pygame.draw.rect(
                screen,
                GRAY,
                (block[0], block[1], CELL_SIZE, CELL_SIZE)
            )

        for segment in self.snake:
            pygame.draw.rect(
                screen,
                self.snake_color,
                (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            )

        self.draw_food(screen)
        self.draw_poison(screen)
        self.draw_powerup(screen)
        self.draw_hud(screen)

    def draw_food(self, screen):
        if self.food_weight == 1:
            color = YELLOW
        elif self.food_weight == 2:
            color = ORANGE
        else:
            color = WHITE

        pygame.draw.rect(
            screen,
            color,
            (self.food[0], self.food[1], CELL_SIZE, CELL_SIZE)
        )

        font = pygame.font.Font(None, 24)
        text = font.render(str(self.food_weight), True, BLACK)
        screen.blit(text, (self.food[0] + 6, self.food[1] + 2))

    def draw_poison(self, screen):
        pygame.draw.rect(
            screen,
            DARK_RED,
            (self.poison[0], self.poison[1], CELL_SIZE, CELL_SIZE)
        )

    def draw_powerup(self, screen):
        if self.powerup is None:
            return

        if self.powerup_type == "speed":
            color = PURPLE
        elif self.powerup_type == "slow":
            color = CYAN
        else:
            color = BLUE

        pygame.draw.circle(
            screen,
            color,
            (self.powerup[0] + CELL_SIZE // 2, self.powerup[1] + CELL_SIZE // 2),
            CELL_SIZE // 2
        )

    def draw_hud(self, screen):
        font = pygame.font.Font(None, 26)

        texts = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best: {self.personal_best}",
            f"Power-up: {self.powerup_active if self.powerup_active else 'None'}"
        ]

        x = 20
        for text in texts:
            img = font.render(text, True, WHITE)
            screen.blit(img, (x, 20))
            x += 145