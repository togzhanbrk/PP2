import pygame
from racer import RacerGame, WIDTH, HEIGHT
from ui import Button, draw_text
from persistence import load_settings, save_settings, load_leaderboard

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")
clock = pygame.time.Clock()

settings = load_settings()

state = "name"
username = ""
game = None

play_button = Button(300, 180, 200, 50, "Play")
leaderboard_button = Button(300, 250, 200, 50, "Leaderboard")
settings_button = Button(300, 320, 200, 50, "Settings")
quit_button = Button(300, 390, 200, 50, "Quit")

retry_button = Button(300, 300, 200, 50, "Retry")
menu_button = Button(300, 370, 200, 50, "Main Menu")
back_button = Button(300, 520, 200, 50, "Back")

sound_button = Button(280, 180, 240, 50, "Toggle Sound")
color_button = Button(280, 250, 240, 50, "Change Car Color")
difficulty_button = Button(280, 320, 240, 50, "Change Difficulty")


def start_game():
    global game, state
    game = RacerGame(username, settings)
    state = "game"


def draw_name_screen():
    screen.fill((20, 20, 20))
    draw_text(screen, "Enter your name:", 230, 180, big=True)
    draw_text(screen, username + "|", 330, 280)
    draw_text(screen, "Press ENTER to continue", 250, 360)


def draw_menu():
    screen.fill((20, 20, 20))
    draw_text(screen, "RACER GAME", 250, 80, big=True)

    play_button.draw(screen)
    leaderboard_button.draw(screen)
    settings_button.draw(screen)
    quit_button.draw(screen)


def draw_settings():
    screen.fill((20, 20, 20))
    draw_text(screen, "SETTINGS", 280, 80, big=True)

    draw_text(screen, f"Sound: {settings['sound']}", 280, 140)
    draw_text(screen, f"Car Color: {settings['car_color']}", 280, 390)
    draw_text(screen, f"Difficulty: {settings['difficulty']}", 280, 430)

    sound_button.draw(screen)
    color_button.draw(screen)
    difficulty_button.draw(screen)
    back_button.draw(screen)


def draw_leaderboard():
    screen.fill((20, 20, 20))
    draw_text(screen, "TOP 10 SCORES", 230, 50, big=True)

    leaderboard = load_leaderboard()

    y = 130
    if len(leaderboard) == 0:
        draw_text(screen, "No scores yet", 310, y)
    else:
        for i, entry in enumerate(leaderboard):
            text = f"{i + 1}. {entry['name']} | Score: {entry['score']} | Distance: {entry['distance']}"
            draw_text(screen, text, 150, y)
            y += 35

    back_button.draw(screen)


def draw_game_over():
    screen.fill((20, 20, 20))
    draw_text(screen, "GAME OVER", 250, 100, big=True)

    draw_text(screen, f"Score: {game.score}", 300, 180)
    draw_text(screen, f"Distance: {int(game.distance)}", 300, 220)
    draw_text(screen, f"Coins: {game.coins}", 300, 260)

    retry_button.draw(screen)
    menu_button.draw(screen)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "name":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip() != "":
                    state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 12:
                        username += event.unicode

        elif state == "menu":
            if play_button.clicked(event):
                start_game()
            elif leaderboard_button.clicked(event):
                state = "leaderboard"
            elif settings_button.clicked(event):
                state = "settings"
            elif quit_button.clicked(event):
                running = False

        elif state == "settings":
            if sound_button.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            elif color_button.clicked(event):
                colors = ["blue", "red", "green", "yellow"]
                current = colors.index(settings["car_color"])
                settings["car_color"] = colors[(current + 1) % len(colors)]
                save_settings(settings)

            elif difficulty_button.clicked(event):
                levels = ["easy", "normal", "hard"]
                current = levels.index(settings["difficulty"])
                settings["difficulty"] = levels[(current + 1) % len(levels)]
                save_settings(settings)

            elif back_button.clicked(event):
                state = "menu"

        elif state == "leaderboard":
            if back_button.clicked(event):
                state = "menu"

        elif state == "game":
            game.handle_event(event)

        elif state == "game_over":
            if retry_button.clicked(event):
                start_game()
            elif menu_button.clicked(event):
                state = "menu"

    if state == "name":
        draw_name_screen()

    elif state == "menu":
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
    clock.tick(60)

pygame.quit()