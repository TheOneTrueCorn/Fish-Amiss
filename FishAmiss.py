# starting pygame window
import pygame
pygame.init()

win_width = 1000
win_height = 700
win = pygame.display.set_mode((win_width, win_height))

clock = pygame.time.Clock()

while True:
    delta_time = clock.tick() / 1000
    event = pygame.event.poll()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        break
    if event.type == pygame.QUIT:
        break

    win.fill((0, 0, 0))

    pygame.display.flip()
pygame.quit()