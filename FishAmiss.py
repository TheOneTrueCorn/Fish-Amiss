# starting pygame window
import pygame
import vector
import random
import movingObj
import solar_object

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


# images
incomprehensible = pygame.image.load("vu'lphsted lunaris.png")
fishies = pygame.image.load("fish.png")
playa = pygame.image.load("boats.png")

time = "day"

P = movingObj.Player(win)
sun = solar_object.backgroundObject(500,350)
moon = solar_object.backgroundObject(500,350)
font_obj = pygame.font.SysFont("Courier New", 25)
font_obj2 = pygame.font.SysFont("Courier New", 20)
font_obj3 = pygame.font.SysFont("Courier New", 15)


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
    sun.get_forward()
    sun.update(delta_time)
    sun.draw(win)
    moon.get_forward()
    moon.alt_update(delta_time)
    moon.alt_draw(win,current_time)
    pygame.draw.rect(win,(current_time[0]/2,current_time[1]/2,current_time[2]),(0,250,1000,750))
# end of function

# starting variables
money = 0
day = 1
basic_fish_timer = 1
fish_count = 1

fish1_list = []
fish2_list = []
fish3_list = []

clock = pygame.time.Clock()
qte_key = 1
side = "left"

done = False
while not done:
    delta_time = clock.tick() / 1000
    basic_fish_timer -= delta_time

    if basic_fish_timer <= 0:
        basic_fish_timer = 1
        side = random.randint(1, 2)
        qte_key += 1
        fish_count += 1
        if qte_key > 6:
            qte_key = 1
        # if side is 1, spawn on left side of screen
        if side == 1:
            if len(fish1_list) < 6:
                fish1_list.append(movingObj.BoringFish(win, -20, random.randint(300, win_height), 20, side, qte_key))

            if fish_count == 10:
                fish2_list.append(
                    movingObj.BiggerFish(win, -40, random.randint(550, win_height), 40, side, qte_key))
                fish_count = 1

        # if side is 2, spawn on right side of screen
        elif side == 2:
            if len(fish1_list) < 6:
                fish1_list.append(movingObj.BoringFish(win, win_width + 20, random.randint(300, win_height - 20), 20, side, qte_key))

            if fish_count == 10:
                fish2_list.append(
                    movingObj.BiggerFish(win, win_width + 40, random.randint(550, win_height - 40), 40, side, qte_key))
                fish_count = 1

    win.fill((0, 0, 0))
    day_night()

    shop(win)
    P.draw_player(playa)

    for fish in fish1_list:
        fish.draw(fishies)
        fish.update(delta_time, fish1_list)

    for fish in fish2_list:
        fish.draw()
        fish.update(delta_time, fish1_list)

    money = P.update(fish1_list, money)
    done = P.handle_input(delta_time)



    pygame.display.flip()
pygame.quit()