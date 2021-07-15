# starting pygame window
import pygame
import vector
import random
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


clock = pygame.time.Clock()


while True:
    delta_time = clock.tick() / 1000
    event = pygame.event.poll()
    keys = pygame.key.get_pressed()

    #day night cycle
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

    if keys[pygame.K_ESCAPE]:
        break
    if event.type == pygame.QUIT:
        break

    print(time)

    win.fill(current_time)

    pygame.display.flip()
pygame.quit()