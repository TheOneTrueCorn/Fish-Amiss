# starting pygame window
import pygame
import player

pygame.init()

win_width = 1000
win_height = 700
win = pygame.display.set_mode((win_width, win_height))

clock = pygame.time.Clock()
P = player.Player(win)

done = False
while not done:
    delta_time = clock.tick() / 1000
    done = P.handle_input(delta_time)

    win.fill((0, 0, 0))
    P.draw_player()

    pygame.display.flip()
pygame.quit()