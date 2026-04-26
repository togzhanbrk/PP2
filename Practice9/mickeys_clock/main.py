import pygame
from clock import Clock

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Mickey Clock")

clock = Clock()
timer = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))
    clock.draw(screen)

    pygame.display.flip()
    timer.tick(60)

pygame.quit()