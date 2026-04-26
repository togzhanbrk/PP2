import pygame
import os
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

clock = pygame.time.Clock()

music_folder = os.path.join(os.path.dirname(__file__), "music")
player = MusicPlayer(music_folder)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.previous_track()

            elif event.key == pygame.K_q:
                running = False

        screen.fill((245, 245, 255))

    # title
    title = font.render("🎵 Music Player", True, (45, 45, 90))
    screen.blit(title, (280, 50))

    # card background
    pygame.draw.rect(screen, (220, 230, 255), (60, 120, 680, 280), border_radius=25)

    # track text
    track_text = small_font.render(
        "Current track: " + player.get_current_track(),
        True,
        (30, 30, 60)
)
    screen.blit(track_text, (100, 160))

    # status
    if player.is_playing:
        status = "Status: Playing"
    else:
        status = "Status: Stopped"

    status_text = small_font.render(status, True, (80, 80, 120))
    screen.blit(status_text, (100, 205))

    # buttons
    buttons = [
        ("P", "Play", 100),
        ("S", "Stop", 230),
        ("N", "Next", 360),
        ("B", "Back", 490),
        ("Q", "Quit", 620)
    ]

    for key, name, x in buttons:
        pygame.draw.rect(screen, (120, 150, 255), (x, 300, 90, 55), border_radius=15)

        key_text = small_font.render(key, True, (255, 255, 255))
        screen.blit(key_text, (x + 35, 310))

        name_text = small_font.render(name, True, (40, 40, 80))
        screen.blit(name_text, (x + 15, 365))

 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()