import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (255, 220, 0)
GRAY = (180, 180, 180)

# Drawing settings
current_color = BLACK
tool = "brush"
brush_size = 6
eraser_size = 25

# Canvas background
screen.fill(WHITE)

# Toolbar buttons
buttons = {
    "brush": pygame.Rect(10, 10, 80, 35),
    "rect": pygame.Rect(100, 10, 80, 35),
    "circle": pygame.Rect(190, 10, 80, 35),
    "eraser": pygame.Rect(280, 10, 90, 35),
}

# Color buttons
color_buttons = [
    (BLACK, pygame.Rect(400, 10, 30, 30)),
    (RED, pygame.Rect(440, 10, 30, 30)),
    (GREEN, pygame.Rect(480, 10, 30, 30)),
    (BLUE, pygame.Rect(520, 10, 30, 30)),
    (YELLOW, pygame.Rect(560, 10, 30, 30)),
]

font = pygame.font.Font(None, 28)

drawing = False
start_pos = None


def draw_toolbar():
    # Draw toolbar background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 55))

    # Draw tool buttons
    for name, rect in buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x + 8, rect.y + 8))

    # Draw color buttons
    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Show selected tool
    selected_text = font.render(f"Tool: {tool}", True, BLACK)
    screen.blit(selected_text, (620, 15))


def distance(pos1, pos2):
    # Find distance between two points
    x1, y1 = pos1
    x2, y2 = pos2
    return int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check tool buttons
            for name, rect in buttons.items():
                if rect.collidepoint(mouse_pos):
                    tool = name

            # Check color buttons
            for color, rect in color_buttons:
                if rect.collidepoint(mouse_pos):
                    current_color = color
                    tool = "brush"

            # Start drawing only below toolbar
            if mouse_pos[1] > 55:
                drawing = True
                start_pos = mouse_pos

        # Mouse button released
        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = pygame.mouse.get_pos()

            if drawing and start_pos is not None:

                # Draw rectangle
                if tool == "rect":
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    rect_x = min(x1, x2)
                    rect_y = min(y1, y2)
                    rect_w = abs(x2 - x1)
                    rect_h = abs(y2 - y1)

                    pygame.draw.rect(
                        screen,
                        current_color,
                        (rect_x, rect_y, rect_w, rect_h),
                        3
                    )

                # Draw circle
                elif tool == "circle":
                    radius = distance(start_pos, end_pos)
                    pygame.draw.circle(
                        screen,
                        current_color,
                        start_pos,
                        radius,
                        3
                    )

            drawing = False
            start_pos = None

        # Mouse moving while pressed
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

            if drawing and mouse_pos[1] > 55:

                # Free brush drawing
                if tool == "brush":
                    pygame.draw.circle(
                        screen,
                        current_color,
                        mouse_pos,
                        brush_size
                    )

                # Eraser draws white circles
                elif tool == "eraser":
                    pygame.draw.circle(
                        screen,
                        WHITE,
                        mouse_pos,
                        eraser_size
                    )

    # Toolbar must be redrawn every frame
    draw_toolbar()

    pygame.display.update()