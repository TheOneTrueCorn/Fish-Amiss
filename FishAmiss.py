# starting pygame window
import pygame

import vector
import random

import player


pygame.init()

win_width = 1000
win_height = 700
win = pygame.display.set_mode((win_width, win_height))

background_color_day = vector.Vector3(random.randint(150,250),random.randint(150,250),random.randint(150,250))
background_color_night = vector.Vector3(random.randint(10,50),random.randint(10,50),random.randint(10,50))
day_night_cycle = vector.Vector3(background_color_day[0] - background_color_night[0],background_color_day[1] - background_color_night[1],background_color_day[2] - background_color_night[2])
current_time = vector.Vector3(background_color_night[0],background_color_night[1],background_color_night[2])
day_check1 = 0
day_check2 = 0
day_check3 = 0
night_check1 = 0
night_check2 = 0
night_check3 = 0




time = "day"

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

clock = pygame.time.Clock()

def day_night():
    global day
    #day night cycle
    global time
    global day_check1
    global day_check2
    global day_check3
    global night_check1
    global night_check2
    global night_check3
    if time == "day":
        current_time[0] += day_night_cycle[0] * delta_time / 30
        current_time[1] += day_night_cycle[1] * delta_time / 30
        current_time[2] += day_night_cycle[2] * delta_time / 30
        if current_time[0] >= background_color_day[0]:
            current_time[0] = background_color_day[0]
            day_check1 = 1
        if current_time[1] >= background_color_day[1]:
            current_time[1] = background_color_day[1]
            day_check2 = 1
        if current_time[2] >= background_color_day[2]:
            current_time[2] = background_color_day[2]
            day_check3 = 1
        if day_check1 + day_check2 + day_check3 == 3:
            time = "night"
            day_check1 = 0
            day_check2 = 0
            day_check3 = 0
    elif time == "night":
        current_time[0] -= day_night_cycle[0] * delta_time / 30
        current_time[1] -= day_night_cycle[1] * delta_time / 30
        current_time[2] -= day_night_cycle[2] * delta_time / 30
        if current_time[0] <= background_color_night[0]:
            current_time[0] = background_color_night[0]
            night_check1 = 1
        if current_time[1] <= background_color_night[1]:
            current_time[1] = background_color_night[1]
            night_check2 = 1
        if current_time[2] <= background_color_night[2]:
            current_time[2] = background_color_night[2]
            night_check3 = 1
        if night_check1 + night_check2 + night_check3 == 3:
            time = "day"
            night_check1 = 0
            night_check2 = 0
            night_check3 = 0
            day += 1

    win.fill(current_time)


done = False
while not done:
    delta_time = clock.tick() / 1000
    money += 1 * delta_time
    done = P.handle_input(delta_time)


    win.fill((0, 0, 0))
    day_night()
    shop(win)

    P.draw_player()


    pygame.display.flip()
pygame.quit()