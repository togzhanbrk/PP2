import pygame
from collections import deque


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)


def flood_fill(surface, start_pos, fill_color, canvas_rect):
    start_x, start_y = start_pos

    if not canvas_rect.collidepoint(start_pos):
        return

    target_color = surface.get_at(start_pos)

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((start_x, start_y))

    while queue:
        x, y = queue.popleft()

        if not canvas_rect.collidepoint((x, y)):
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))