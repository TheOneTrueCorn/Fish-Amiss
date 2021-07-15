# starting pygame window
import pygame
import player

pygame.init()

win_width = 1000
win_height = 700
win = pygame.display.set_mode((win_width, win_height))

clock = pygame.time.Clock()
P = player.Player(win)
font_obj = pygame.font.SysFont("Courier New", 25)
font_obj2 = pygame.font.SysFont("Courier New", 20)
font_obj3 = pygame.font.SysFont("Courier New", 15)

# starting variables
money = 0
day = 1

def shop(win):
    shop_txt = font_obj.render("Shop", False, (255, 255, 255))
    win.blit(shop_txt, (120, 5))

    money_txt = font_obj2.render("Cash:" + str(int(money)) + "$", False, (255, 255, 255))
    win.blit(money_txt, (185, 125))

    money_txt = font_obj2.render("Day:" + str(day), False, (255, 255, 255))
    win.blit(money_txt, (50, 125))

    pygame.draw.line(win, (255, 255, 255), (5, 35), (305, 35), 2)
    pygame.draw.line(win, (255, 255, 255), (5, 120), (305, 120), 3)
    pygame.draw.line(win, (255, 255, 255), (150, 120), (150, 155), 3)
    pygame.draw.rect(win, (255, 255, 255), (5, 5, 300, 150), 3)

done = False
while not done:
    delta_time = clock.tick() / 1000
    money += 1 * delta_time
    done = P.handle_input(delta_time)

    win.fill((0, 0, 0))
    shop(win)
    P.draw_player()

    pygame.display.flip()
pygame.quit()