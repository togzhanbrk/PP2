import pygame
import sys
import math
from datetime import datetime
from tools import distance, flood_fill

pygame.init()

# Window settings
WIDTH = 1000
HEIGHT = 700
TOOLBAR_HEIGHT = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
RED = (220, 0, 0, 255)
GREEN = (0, 180, 0, 255)
BLUE = (0, 0, 220, 255)
YELLOW = (255, 220, 0, 255)
PURPLE = (150, 0, 200, 255)
GRAY = (180, 180, 180, 255)
DARK_GRAY = (90, 90, 90, 255)

font = pygame.font.Font(None, 24)
text_font = pygame.font.SysFont("Arial", 32)

# Main canvas surface
canvas = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
canvas.fill(WHITE)

# Canvas drawing area
canvas_rect = pygame.Rect(0, TOOLBAR_HEIGHT, WIDTH, HEIGHT - TOOLBAR_HEIGHT)

# Current settings
current_color = BLACK
tool = "pencil"
brush_size = 5

# Drawing states
drawing = False
start_pos = None
last_pos = None

# Text tool states
typing = False
text_position = None
typed_text = ""

# Tool buttons
buttons = {
    "pencil": pygame.Rect(10, 10, 75, 28),
    "line": pygame.Rect(90, 10, 65, 28),
    "rect": pygame.Rect(160, 10, 65, 28),
    "circle": pygame.Rect(230, 10, 75, 28),
    "square": pygame.Rect(310, 10, 80, 28),
    "right tri": pygame.Rect(395, 10, 95, 28),
    "eq tri": pygame.Rect(495, 10, 80, 28),
    "rhombus": pygame.Rect(580, 10, 95, 28),
    "eraser": pygame.Rect(680, 10, 75, 28),
    "fill": pygame.Rect(760, 10, 60, 28),
    "text": pygame.Rect(825, 10, 60, 28),
}

# Brush size buttons
size_buttons = {
    2: pygame.Rect(10, 45, 70, 25),
    5: pygame.Rect(85, 45, 85, 25),
    10: pygame.Rect(175, 45, 75, 25),
}

# Color buttons
color_buttons = [
    (BLACK, pygame.Rect(280, 45, 25, 25)),
    (RED, pygame.Rect(315, 45, 25, 25)),
    (GREEN, pygame.Rect(350, 45, 25, 25)),
    (BLUE, pygame.Rect(385, 45, 25, 25)),
    (YELLOW, pygame.Rect(420, 45, 25, 25)),
    (PURPLE, pygame.Rect(455, 45, 25, 25)),
]


def draw_toolbar():
    # Toolbar background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Draw tool buttons
    for name, rect in buttons.items():
        button_color = WHITE if tool != name else YELLOW
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        text = font.render(name, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 6))

    # Draw brush size buttons
    for size, rect in size_buttons.items():
        button_color = WHITE if brush_size != size else YELLOW
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        label = "small" if size == 2 else "medium" if size == 5 else "large"
        text = font.render(label, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 5))

    # Draw color buttons
    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Information text
    info = font.render(
        f"Tool: {tool} | Size: {brush_size} | Ctrl+S = Save | 1/2/3 = Size",
        True,
        BLACK
    )
    screen.blit(info, (500, 48))


def draw_preview(mouse_pos):
    # Live preview for shape tools
    if not drawing or start_pos is None:
        return

    x1, y1 = start_pos
    x2, y2 = mouse_pos

    color = WHITE if tool == "eraser" else current_color

    if tool == "line":
        pygame.draw.line(screen, color, start_pos, mouse_pos, brush_size)

    elif tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, color, rect, brush_size)

    elif tool == "circle":
        radius = distance(start_pos, mouse_pos)
        pygame.draw.circle(screen, color, start_pos, radius, brush_size)

    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        draw_x = x1 - side if x2 < x1 else x1
        draw_y = y1 - side if y2 < y1 else y1
        pygame.draw.rect(screen, color, (draw_x, draw_y, side, side), brush_size)

    elif tool == "right tri":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(screen, color, points, brush_size)

    elif tool == "eq tri":
        side = distance(start_pos, mouse_pos)
        height = int(side * math.sqrt(3) / 2)
        points = [(x1, y1 - height), (x1 - side // 2, y1), (x1 + side // 2, y1)]
        pygame.draw.polygon(screen, color, points, brush_size)

    elif tool == "rhombus":
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        points = [(x1, y1 - height), (x1 + width, y1), (x1, y1 + height), (x1 - width, y1)]
        pygame.draw.polygon(screen, color, points, brush_size)


def draw_final_shape(end_pos):
    # Draw final shape permanently on canvas
    x1, y1 = start_pos
    x2, y2 = end_pos

    color = WHITE if tool == "eraser" else current_color

    if tool == "line":
        pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

    elif tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(canvas, color, rect, brush_size)

    elif tool == "circle":
        radius = distance(start_pos, end_pos)
        pygame.draw.circle(canvas, color, start_pos, radius, brush_size)

    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        draw_x = x1 - side if x2 < x1 else x1
        draw_y = y1 - side if y2 < y1 else y1
        pygame.draw.rect(canvas, color, (draw_x, draw_y, side, side), brush_size)

    elif tool == "right tri":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(canvas, color, points, brush_size)

    elif tool == "eq tri":
        side = distance(start_pos, end_pos)
        height = int(side * math.sqrt(3) / 2)
        points = [(x1, y1 - height), (x1 - side // 2, y1), (x1 + side // 2, y1)]
        pygame.draw.polygon(canvas, color, points, brush_size)

    elif tool == "rhombus":
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        points = [(x1, y1 - height), (x1 + width, y1), (x1, y1 + height), (x1 - width, y1)]
        pygame.draw.polygon(canvas, color, points, brush_size)


def save_canvas():
    # Save canvas with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"paint_{timestamp}.png"

    # Save only canvas area without toolbar
    saved_area = canvas.subsurface(canvas_rect)
    pygame.image.save(saved_area, filename)

    print(f"Saved as {filename}")


running = True

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard events
        if event.type == pygame.KEYDOWN:

            # Ctrl + S saves canvas
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

            # Brush size shortcuts
            elif event.key == pygame.K_1:
                brush_size = 2

            elif event.key == pygame.K_2:
                brush_size = 5

            elif event.key == pygame.K_3:
                brush_size = 10

            # Text typing
            elif typing:
                if event.key == pygame.K_RETURN:
                    rendered = text_font.render(typed_text, True, current_color)
                    canvas.blit(rendered, text_position)
                    typing = False
                    typed_text = ""

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    typed_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

        # Mouse pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Tool button selection
            for name, rect in buttons.items():
                if rect.collidepoint(pos):
                    tool = name
                    typing = False

            # Brush size button selection
            for size, rect in size_buttons.items():
                if rect.collidepoint(pos):
                    brush_size = size

            # Color selection
            for color, rect in color_buttons:
                if rect.collidepoint(pos):
                    current_color = color

            # Canvas actions
            if canvas_rect.collidepoint(pos):

                if tool == "fill":
                    flood_fill(canvas, pos, current_color, canvas_rect)

                elif tool == "text":
                    typing = True
                    text_position = pos
                    typed_text = ""

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        # Mouse moving
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()

            if drawing and canvas_rect.collidepoint(pos):

                # Pencil draws line between old and new mouse position
                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                # Eraser draws white line
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size)
                    last_pos = pos

        # Mouse released
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if drawing and start_pos is not None:
                if tool not in ["pencil", "eraser"]:
                    draw_final_shape(pos)

            drawing = False
            start_pos = None
            last_pos = None

    # Draw everything
    screen.blit(canvas, (0, 0))

    # Draw live preview
    draw_preview(mouse_pos)

    # Draw temporary typing text
    if typing and text_position is not None:
        preview_text = text_font.render(typed_text + "|", True, current_color)
        screen.blit(preview_text, text_position)

    draw_toolbar()

    pygame.display.update()
    clock.tick(60)