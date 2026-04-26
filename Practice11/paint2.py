import pygame
import sys
import math

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Practice 11")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 220)
YELLOW = (255, 220, 0)
GRAY = (180, 180, 180)

font = pygame.font.Font(None, 25)

current_color = BLACK
tool = "brush"
brush_size = 5

screen.fill(WHITE)

# Tool buttons
buttons = {
    "brush": pygame.Rect(10, 10, 75, 35),
    "square": pygame.Rect(95, 10, 80, 35),
    "right tri": pygame.Rect(185, 10, 90, 35),
    "eq tri": pygame.Rect(285, 10, 80, 35),
    "rhombus": pygame.Rect(375, 10, 95, 35),
}

# Color buttons
color_buttons = [
    (BLACK, pygame.Rect(500, 12, 30, 30)),
    (RED, pygame.Rect(540, 12, 30, 30)),
    (GREEN, pygame.Rect(580, 12, 30, 30)),
    (BLUE, pygame.Rect(620, 12, 30, 30)),
    (YELLOW, pygame.Rect(660, 12, 30, 30)),
]

drawing = False
start_pos = None


# Draw toolbar
def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 55))

    for name, rect in buttons.items():
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 9))

    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    text = font.render(f"Tool: {tool}", True, BLACK)
    screen.blit(text, (720, 18))


# Find distance between two points
def distance(pos1, pos2):
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

        # Mouse pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Select tool
            for name, rect in buttons.items():
                if rect.collidepoint(mouse_pos):
                    tool = name

            # Select color
            for color, rect in color_buttons:
                if rect.collidepoint(mouse_pos):
                    current_color = color
                    tool = "brush"

            # Start drawing only below toolbar
            if mouse_pos[1] > 55:
                drawing = True
                start_pos = mouse_pos

        # Mouse moving while pressed
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

            # Brush drawing
            if drawing and tool == "brush" and mouse_pos[1] > 55:
                pygame.draw.circle(screen, current_color, mouse_pos, brush_size)

        # Mouse released
        if event.type == pygame.MOUSEBUTTONUP:
            end_pos = pygame.mouse.get_pos()

            if drawing and start_pos is not None:
                x1, y1 = start_pos
                x2, y2 = end_pos

                # Draw square
                if tool == "square":
                    side = min(abs(x2 - x1), abs(y2 - y1))

                    if x2 < x1:
                        draw_x = x1 - side
                    else:
                        draw_x = x1

                    if y2 < y1:
                        draw_y = y1 - side
                    else:
                        draw_y = y1

                    pygame.draw.rect(
                        screen,
                        current_color,
                        (draw_x, draw_y, side, side),
                        3
                    )

                # Draw right triangle
                elif tool == "right tri":
                    points = [
                        (x1, y1),
                        (x1, y2),
                        (x2, y2)
                    ]

                    pygame.draw.polygon(screen, current_color, points, 3)

                # Draw equilateral triangle
                elif tool == "eq tri":
                    side = distance(start_pos, end_pos)
                    height = int(side * math.sqrt(3) / 2)

                    points = [
                        (x1, y1 - height),
                        (x1 - side // 2, y1),
                        (x1 + side // 2, y1)
                    ]

                    pygame.draw.polygon(screen, current_color, points, 3)

                # Draw rhombus
                elif tool == "rhombus":
                    center_x = x1
                    center_y = y1

                    width = abs(x2 - x1)
                    height = abs(y2 - y1)

                    points = [
                        (center_x, center_y - height),
                        (center_x + width, center_y),
                        (center_x, center_y + height),
                        (center_x - width, center_y)
                    ]

                    pygame.draw.polygon(screen, current_color, points, 3)

            drawing = False
            start_pos = None

    draw_toolbar()
    pygame.display.update()