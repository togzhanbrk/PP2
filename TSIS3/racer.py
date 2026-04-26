import pygame
import random
from persistence import save_score

WIDTH = 800
HEIGHT = 600

ROAD_X = 200
ROAD_WIDTH = 400
LANES = [250, 350, 450, 550]

WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
DARK = (20, 20, 20)
RED = (220, 50, 50)
BLUE = (50, 120, 255)
GREEN = (50, 220, 100)
YELLOW = (255, 220, 50)
PURPLE = (180, 80, 255)
ORANGE = (255, 150, 40)


class RacerGame:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings

        self.player_lane = 1
        self.player = pygame.Rect(LANES[self.player_lane] - 25, 500, 50, 80)

        self.car_color = self.get_car_color()

        self.traffic = []
        self.obstacles = []
        self.powerups = []

        self.coins = 0
        self.distance = 0
        self.finish_distance = 3000
        self.score = 0

        self.speed = self.get_start_speed()
        self.spawn_timer = 0
        self.obstacle_timer = 0
        self.powerup_timer = 0

        self.active_powerup = None
        self.powerup_end_time = 0
        self.shield = False

        self.game_over = False

    def get_car_color(self):
        colors = {
            "blue": BLUE,
            "red": RED,
            "green": GREEN,
            "yellow": YELLOW
        }
        return colors.get(self.settings["car_color"], BLUE)

    def get_start_speed(self):
        difficulty = self.settings["difficulty"]

        if difficulty == "easy":
            return 4
        elif difficulty == "hard":
            return 7
        return 5

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.player_lane > 0:
                self.player_lane -= 1
            elif event.key == pygame.K_RIGHT and self.player_lane < 3:
                self.player_lane += 1

            self.player.x = LANES[self.player_lane] - 25

    def safe_lane(self):
        safe_lanes = [0, 1, 2, 3]
        player_lane = self.player_lane

        if player_lane in safe_lanes:
            safe_lanes.remove(player_lane)

        return random.choice(safe_lanes)

    def spawn_traffic(self):
        lane = self.safe_lane()
        car = pygame.Rect(LANES[lane] - 25, -100, 50, 80)
        self.traffic.append(car)

    def spawn_obstacle(self):
        lane = self.safe_lane()
        obstacle_type = random.choice(["barrier", "oil", "pothole", "boost"])
        rect = pygame.Rect(LANES[lane] - 30, -60, 60, 40)

        self.obstacles.append({
            "rect": rect,
            "type": obstacle_type
        })

    def spawn_powerup(self):
        lane = self.safe_lane()
        p_type = random.choice(["nitro", "shield", "repair"])

        rect = pygame.Rect(LANES[lane] - 20, -50, 40, 40)

        self.powerups.append({
            "rect": rect,
            "type": p_type,
            "time": pygame.time.get_ticks()
        })

    def activate_powerup(self, p_type):
        now = pygame.time.get_ticks()

        if self.active_powerup is not None:
            return

        if p_type == "nitro":
            self.active_powerup = "nitro"
            self.powerup_end_time = now + 4000
            self.speed += 4

        elif p_type == "shield":
            self.active_powerup = "shield"
            self.shield = True

        elif p_type == "repair":
            if len(self.obstacles) > 0:
                self.obstacles.pop(0)
            self.score += 50

    def update_powerup(self):
        now = pygame.time.get_ticks()

        if self.active_powerup == "nitro" and now > self.powerup_end_time:
            self.speed -= 4
            self.active_powerup = None

    def update(self):
        if self.game_over:
            return

        self.update_powerup()

        self.distance += self.speed * 0.1
        self.score = self.coins * 10 + int(self.distance)

        progress = self.distance / 500
        traffic_frequency = max(25, 80 - int(progress * 5))
        obstacle_frequency = max(40, 100 - int(progress * 5))

        self.spawn_timer += 1
        self.obstacle_timer += 1
        self.powerup_timer += 1

        if self.spawn_timer > traffic_frequency:
            self.spawn_traffic()
            self.spawn_timer = 0

        if self.obstacle_timer > obstacle_frequency:
            self.spawn_obstacle()
            self.obstacle_timer = 0

        if self.powerup_timer > 250:
            self.spawn_powerup()
            self.powerup_timer = 0

        for car in self.traffic:
            car.y += self.speed

        for obstacle in self.obstacles:
            obstacle["rect"].y += self.speed

        for powerup in self.powerups:
            powerup["rect"].y += self.speed

        self.traffic = [car for car in self.traffic if car.y < HEIGHT + 100]
        self.obstacles = [o for o in self.obstacles if o["rect"].y < HEIGHT + 100]

        now = pygame.time.get_ticks()
        self.powerups = [
            p for p in self.powerups
            if p["rect"].y < HEIGHT + 100 and now - p["time"] < 6000
        ]

        self.check_collisions()

        if self.distance >= self.finish_distance:
            self.end_game()

    def check_collisions(self):
        for car in self.traffic[:]:
            if self.player.colliderect(car):
                if self.shield:
                    self.shield = False
                    self.active_powerup = None
                    self.traffic.remove(car)
                else:
                    self.end_game()

        for obstacle in self.obstacles[:]:
            rect = obstacle["rect"]
            o_type = obstacle["type"]

            if self.player.colliderect(rect):
                if o_type == "boost":
                    if self.active_powerup is None:
                        self.active_powerup = "nitro"
                        self.powerup_end_time = pygame.time.get_ticks() + 3000
                        self.speed += 3
                    self.obstacles.remove(obstacle)

                elif self.shield:
                    self.shield = False
                    self.active_powerup = None
                    self.obstacles.remove(obstacle)

                elif o_type == "oil":
                    self.speed = max(3, self.speed - 1)
                    self.obstacles.remove(obstacle)

                else:
                    self.end_game()

        for powerup in self.powerups[:]:
            if self.player.colliderect(powerup["rect"]):
                self.activate_powerup(powerup["type"])
                self.powerups.remove(powerup)

    def end_game(self):
        self.game_over = True
        save_score(self.username, self.score, self.distance)

    def draw_road(self, screen):
        screen.fill((30, 130, 50))

        pygame.draw.rect(screen, GRAY, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))

        for lane_x in [300, 400, 500]:
            for y in range(0, HEIGHT, 80):
                pygame.draw.rect(screen, WHITE, (lane_x, y, 5, 40))

    def draw(self, screen):
        self.draw_road(screen)

        pygame.draw.rect(screen, self.car_color, self.player, border_radius=8)

        if self.shield:
            pygame.draw.circle(screen, (100, 200, 255), self.player.center, 45, 3)

        for car in self.traffic:
            pygame.draw.rect(screen, RED, car, border_radius=8)

        for obstacle in self.obstacles:
            rect = obstacle["rect"]
            o_type = obstacle["type"]

            if o_type == "barrier":
                color = ORANGE
            elif o_type == "oil":
                color = DARK
            elif o_type == "pothole":
                color = (90, 50, 20)
            else:
                color = PURPLE

            pygame.draw.rect(screen, color, rect, border_radius=8)

        for powerup in self.powerups:
            rect = powerup["rect"]
            p_type = powerup["type"]

            if p_type == "nitro":
                color = PURPLE
            elif p_type == "shield":
                color = BLUE
            else:
                color = GREEN

            pygame.draw.ellipse(screen, color, rect)

        self.draw_hud(screen)

    def draw_hud(self, screen):
        font = pygame.font.Font(None, 30)

        texts = [
            f"Name: {self.username}",
            f"Score: {self.score}",
            f"Coins: {self.coins}",
            f"Distance: {int(self.distance)} / {self.finish_distance}",
            f"Power-up: {self.active_powerup if self.active_powerup else 'None'}"
        ]

        y = 15
        for text in texts:
            img = font.render(text, True, WHITE)
            screen.blit(img, (15, y))
            y += 30