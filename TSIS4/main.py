import pygame
import json
import sys

from config import *
from game import SnakeGame
from db import get_top_10


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 34)
big_font = pygame.font.Font(None, 64)


def load_settings():
    try:
        with open("settings.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "snake_color": "Green",
            "grid": True,
            "sound": True
        }


def save_settings(settings):
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)

        img = font.render(self.text, True, WHITE)
        img_rect = img.get_rect(center=self.rect.center)
        screen.blit(img, img_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def draw_text(text, x, y, color=WHITE, big=False):
    f = big_font if big else font
    img = f.render(text, True, color)
    screen.blit(img, (x, y))


settings = load_settings()

state = "menu"
username = ""
game = None

play_btn = Button(300, 180, 200, 50, "Play")
leader_btn = Button(300, 250, 200, 50, "Leaderboard")
settings_btn = Button(300, 320, 200, 50, "Settings")
quit_btn = Button(300, 390, 200, 50, "Quit")

retry_btn = Button(300, 300, 200, 50, "Retry")
menu_btn = Button(300, 370, 200, 50, "Main Menu")
back_btn = Button(300, 520, 200, 50, "Back")

grid_btn = Button(280, 180, 240, 50, "Toggle Grid")
sound_btn = Button(280, 250, 240, 50, "Toggle Sound")
color_btn = Button(280, 320, 240, 50, "Change Color")
save_back_btn = Button(280, 460, 240, 50, "Save & Back")


def start_game():
    global game, state

    if username.strip() == "":
        return

    game = SnakeGame(username, settings)
    state = "game"


def draw_menu():
    screen.fill(BLACK)

    draw_text("SNAKE GAME", 250, 70, big=True)
    draw_text("Username:", 250, 135)
    draw_text(username + "|", 390, 135, YELLOW)

    play_btn.draw(screen)
    leader_btn.draw(screen)
    settings_btn.draw(screen)
    quit_btn.draw(screen)


def draw_settings():
    screen.fill(BLACK)

    draw_text("SETTINGS", 280, 70, big=True)

    draw_text(f"Grid: {settings['grid']}", 300, 135)
    draw_text(f"Sound: {settings['sound']}", 300, 390)
    draw_text(f"Snake color: {settings['snake_color']}", 260, 425)

    color_rgb = COLOR_OPTIONS[settings["snake_color"]]
    pygame.draw.rect(screen, color_rgb, (550, 420, 40, 30))
    pygame.draw.rect(screen, WHITE, (550, 420, 40, 30), 2)

    grid_btn.draw(screen)
    sound_btn.draw(screen)
    color_btn.draw(screen)
    save_back_btn.draw(screen)


def draw_leaderboard():
    screen.fill(BLACK)

    draw_text("TOP 10 LEADERBOARD", 180, 50, big=True)

    try:
        rows = get_top_10()
    except Exception as e:
        draw_text("Database error!", 300, 150, RED)
        draw_text(str(e)[:50], 120, 200, RED)
        back_btn.draw(screen)
        return

    y = 130
    draw_text("Rank  Name        Score  Level  Date", 120, 95, YELLOW)

    if len(rows) == 0:
        draw_text("No scores yet", 310, y)
    else:
        for i, row in enumerate(rows):
            name, score, level, date = row
            date_text = str(date).split(".")[0]
            text = f"{i + 1}.    {name:<10}  {score:<5}  {level:<5}  {date_text}"
            draw_text(text, 90, y)
            y += 35

    back_btn.draw(screen)


def draw_game_over():
    screen.fill(BLACK)

    draw_text("GAME OVER", 250, 80, big=True)

    draw_text(f"Player: {username}", 300, 160)
    draw_text(f"Score: {game.score}", 300, 200)
    draw_text(f"Level reached: {game.level}", 300, 240)
    draw_text(f"Personal best: {max(game.personal_best, game.score)}", 300, 280)

    retry_btn.draw(screen)
    menu_btn.draw(screen)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    start_game()
                else:
                    if len(username) < 12 and event.unicode.isprintable():
                        username += event.unicode

            if play_btn.clicked(event):
                start_game()

            elif leader_btn.clicked(event):
                state = "leaderboard"

            elif settings_btn.clicked(event):
                state = "settings"

            elif quit_btn.clicked(event):
                running = False

        elif state == "settings":
            if grid_btn.clicked(event):
                settings["grid"] = not settings["grid"]

            elif sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]

            elif color_btn.clicked(event):
                color_names = list(COLOR_OPTIONS.keys())
                current = color_names.index(settings["snake_color"])
                settings["snake_color"] = color_names[(current + 1) % len(color_names)]

            elif save_back_btn.clicked(event):
                save_settings(settings)
                state = "menu"

        elif state == "leaderboard":
            if back_btn.clicked(event):
                state = "menu"

        elif state == "game":
            game.handle_event(event)

        elif state == "game_over":
            if retry_btn.clicked(event):
                start_game()

            elif menu_btn.clicked(event):
                state = "menu"

    if state == "menu":
        draw_menu()

    elif state == "settings":
        draw_settings()

    elif state == "leaderboard":
        draw_leaderboard()

    elif state == "game":
        game.update()
        game.draw(screen)

        if game.game_over:
            state = "game_over"

    elif state == "game_over":
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()