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
shops = pygame.image.load("fish shop.png")
title =pygame.image.load("fish amiss title.png")
hook_wurm = pygame.image.load("big bois and harpoon.png")
spews = pygame.image.load("spewer.png")
player_bar = pygame.image.load("healthbar.png")
forbidden_knowledge = pygame.image.load("eldritch foresight.png")

#sound/music
# main_theme = "somber ocean.wav"
pygame.mixer.init()
# pygame.mixer.music.load('somber ocean.wav')
# pygame.mixer.music.play(-1)

time = "day"

P = movingObj.Player(win)
sun = solar_object.BackgroundObject(500,350)
moon = solar_object.BackgroundObject(500,350)
font_obj = pygame.font.SysFont("Courier New", 25)
font_obj2 = pygame.font.SysFont("Courier New", 20)
font_obj3 = pygame.font.SysFont("Courier New", 15)


def shop(win):
    shop_txt = font_obj.render("Shop", False, (255, 255, 255))
    win.blit(shop_txt, (120, 5))



    win.blit(shops,(5,35))
    money_txt = font_obj2.render("Cash:$" + str(int(money)), False, (255, 255, 255))
    win.blit(money_txt, (185, 160))

    money_txt = font_obj2.render("Day:" + str(day), False, (255, 255, 255))
    win.blit(money_txt, (50, 160))
    pygame.draw.line(win, (255, 255, 255), (5, 35), (305, 35), 2)
    pygame.draw.line(win, (255, 255, 255), (5, 150), (305, 150), 3)
    pygame.draw.line(win, (255, 255, 255), (150, 150), (150, 190), 3)
    pygame.draw.rect(win, (255, 255, 255), (5, 5, 300, 185), 3)


def day_night(reality_broken):
    global day
    #day night cycle
    global time
    global day_check1
    global day_check2
    global day_check3
    global night_check1
    global night_check2
    global night_check3
    if reality_broken is False:
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
        sun.draw(win,beyond_revealed,forbidden_knowledge)
        moon.get_forward()
        moon.alt_update(delta_time)
        moon.alt_draw(win,current_time,beyond_revealed,forbidden_knowledge)
        pygame.draw.rect(win,(current_time[0]/2,current_time[1]/2,current_time[2]),(0,250,1000,750))
    else:
        sun.get_forward()
        sun.update(delta_time)
        sun.draw(win,beyond_revealed,forbidden_knowledge)
        moon.get_forward()
        moon.alt_update(delta_time)
        moon.alt_draw(win, current_time,beyond_revealed,forbidden_knowledge)

# end of function

# starting variables
money = 75
day = 1
basic_fish_timer = 1
projectile_timer = 1
projectile2_timer = 1
day_bonus_timer = 60
shop_timer = 3
fish_count = 1
boss_fish = False

fish1_list = []
fish2_list = []
fish3_list = []
fish4_list = []
lunaris_plist = []
MegaBoss_plist = []
cannon_list = []
harpoon_list = []
cash_list = []

shop_active = True
paused = True
title_screen = True
clock = pygame.time.Clock()
qte_key = 1
side = "left"
oranges = 0
cannons = 0
harpoons = 0
done = False
harpoon_active = False
Bosses = 0
MegaBosses = 0
beyond_revealed = False
total_cannon_kills = 0

# quests
completed = True
completed_quests = []
unlocked = True
quest_menu = False
quest1 = False
quest2 = False
quest3 = False
quest4 = False
quest5 = False
quest6 = False
quest7 = False
quest8 = False
quest9 = False
quest10 = False
angler_caught = 0
shark_caught = 0
big_fish_caught = 0
fish_during_boss = 0
check = False
music_timer = 0
cp = 0
quest_marker = False
time_survived = 0
while not done:
    mpos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    if P.health > 0:
        delta_time = clock.tick() / 1000
    if keys[pygame.K_p] and paused == False and quest_menu == False and beyond_revealed is False:
        paused = True
    if keys[pygame.K_q] and paused == False and quest_menu == False:
        quest_menu = True
        quest_marker = False
    if keys[pygame.K_u] and paused == True:
        paused = False
        title_screen = False
    if keys[pygame.K_u] and quest_menu == True:
        quest_menu = False
    if paused:
        delta_time = 0
    if quest_menu:
        delta_time = 0

    music_timer += 1 * delta_time
    time_survived += 1 * delta_time
    if beyond_revealed and music_timer >= 31:
        music_timer = 0
        # pygame.mixer.music.load("amalgamation of waste.wav")
        # pygame.mixer.music.play()
########################################################        MUSIC
    basic_fish_timer -= delta_time
    day_bonus_timer -= delta_time

    if day_bonus_timer <= 0 and not beyond_revealed:
        money += 40
        P.health += 10
        day_bonus_timer = 60

    if beyond_revealed is False:
        # spawn feeesh  if endgame is not unlocked
        if basic_fish_timer <= 0:
            basic_fish_timer = 1
            side = random.randint(1, 2)
            qte_key += 1
            fish_count += 1
            if qte_key > 6:
                qte_key = 1
            # if side is 1, spawn on left side of screen
            if side == 1:
                if len(fish1_list) < 10:
                    fish1_list.append(movingObj.BoringFish(win, -20, random.randint(300, win_height), 20, side, qte_key))

                if fish_count == 10:
                    fish2_list.append(
                        movingObj.BiggerFish(win, -40, random.randint(550, win_height), 40, side, qte_key))
                    fish_count = 1

            # if side is 2, spawn on right side of screen
            elif side == 2:
                if len(fish1_list) < 10:
                    fish1_list.append(movingObj.BoringFish(win, win_width + 20, random.randint(300, win_height - 20), 20, side, qte_key))

                if fish_count == 10:
                    fish2_list.append(
                        movingObj.BiggerFish(win, win_width + 40, random.randint(550, win_height - 40), 40, side, qte_key))
                    fish_count = 1

            # boss fish spawn
            if day % 2 == 0 and len(fish3_list) < day / 2 and Bosses < day:
                for i in range(int(day / 2)):
                    Bosses += 2
                    fish3_list.append(B := movingObj.BossFish(win, random.randint(200, win_width - 200), win_height + 80, 80, side))
                    boss_fish = True
            if day % 2 != 0:
                Bosses = 0


    win.fill((random.randint(0,20),random.randint(0,20),random.randint(0,20)))
    day_night(beyond_revealed)

    if beyond_revealed is False:
        shop(win)
        P.draw_player(playa,player_bar,beyond_revealed)
    else:
        P.draw_player(incomprehensible,player_bar,beyond_revealed)
        P.health += 3 * delta_time

    # as long as endgame is false, update and draw all the fishes
    if beyond_revealed is False:
        for fish in fish1_list:
            fish.draw(fishies)
            color = fish.update(delta_time, fish1_list)

        for fish in fish2_list:
            fish.draw(fishies)
            fish.update(delta_time, fish1_list, fish2_list)

        for fish in fish3_list:
            fish.draw(hook_wurm)
            fish.update(delta_time, fish1_list)

    for cannon in cannon_list:
        cannon.draw()
        boss_kills, cannon_kills = cannon.update(delta_time, fish1_list, fish2_list, fish3_list, cannon_list)

        if quest9 is not completed:
            if cannon_kills >= 3:
                quest9 = completed
                completed_quests.append(1)
                quest_marker = True
                money += 150

        if quest4 is not completed:
            if boss_kills >= 1:
                quest4 = completed
                completed_quests.append(1)
                quest_marker = True
                money += 150

    for harp in harpoon_list:
        harp.draw(P.pos.x, P.pos.y)
        money, harpoon_active, angler_caught, shark_caught, total_fish_caught = harp.update(delta_time, P.pos.x, P.pos.y, harpoon_list, fish1_list, fish2_list, money)

        if angler_caught is not None:
            if quest5 is not completed:
                if angler_caught > 0:
                    quest5 = completed
                    cp += 1
                    completed_quests.append(cp)
                    quest_marker = True
                    money += 150

        if shark_caught is not None:
            if quest6 is not completed:
                if shark_caught > 0:
                    quest6 = completed
                    cp += 1
                    completed_quests.append(cp)
                    quest_marker = True
                    money += 150

        if quest7 is not completed:
            if total_fish_caught > 2:
                quest7 = completed
                cp += 1
                completed_quests.append(cp)
                quest_marker = True
                money += 75

    #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
    if boss_fish == True:
        projectile_timer -= delta_time

        if projectile_timer <= 0 and B.moving is False and len(fish3_list) > 0:
            for B in fish3_list:
                lunaris_plist.append(movingObj.FishProjectile(win, B.pos.x, B.pos.y, 10, 0, 10))
                lunaris_plist.append(movingObj.FishProjectile(win, B.pos.x, B.pos.y, 10, 0, 10))
                lunaris_plist.append(movingObj.FishProjectile(win, B.pos.x, B.pos.y, 10, 0, 10))
            projectile_timer = 0.5

        for proj in lunaris_plist:
            proj.draw()
            if len(fish3_list) > 0:
                P.health = proj.update(delta_time, lunaris_plist, P.pos.x, P.pos.y, P.radius, P.health, fish3_list[0].moving)
            else:
                proj.pos.y += 50 * delta_time
                if proj.pos.y >= win_height + proj.radius:
                    lunaris_plist.remove(proj)
    #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

    money, total_fish_caught, orange_fish_caught, red_fish_caught = P.update(fish1_list, money)
    done = P.handle_input(delta_time, fish1_list,beyond_revealed, fish4_list,sun,moon)

    if P.health > 100:
        P.health = 100

    # shop is not available
    if beyond_revealed is False:
        if shop_active == False:
            shop_timer -= delta_time
            if shop_timer <= 0:
                shop_timer = 3
                shop_active = True
            pygame.draw.rect(win, "white", (5, 80, 300, 30))
            txt = font_obj3.render("Stock available in: " + str(int(shop_timer + 1)), False, (0, 0, 0))
            win.blit(txt, (60, 85))

        # shop is available
        else:
            if keys[pygame.K_1]:
                if money >= 150:
                    shop_active = False
                    # player bought an orange
                    money -= 150
                    oranges += 1
                    P.health += 30
            elif keys[pygame.K_2]:
                if money >= 70:
                    shop_active = False
                    # player bought a cannon
                    money -= 70
                    cannons += 1
                    cannon_list.append(movingObj.Cannon(win, P.pos.x, P.pos.y))
            elif keys[pygame.K_3] and harpoon_active == False:
                if money >= 250:
                    shop_active = False
                    # player bought a harpoon
                    money -= 250
                    harpoons += 1
                    mpos_x = mpos[0]
                    mpos_y = mpos[1]
                    init_vel = vector.Vector2(mpos_x, mpos_y) - vector.Vector2(P.pos.x, P.pos.y)
                    harpoon_list.append(movingObj.Harpoon(win, P.pos.x, P.pos.y, init_vel[0], init_vel[1]))
                    harpoon_list.append(movingObj.Harpoon(win, P.pos.x, P.pos.y, 200, 0))
                    harpoon_list.append(movingObj.Harpoon(win, P.pos.x, P.pos.y, -200, 0))

    # options menu
    if paused:
        menu = pygame.Surface((700, 500))
        menu.fill((0, 0, 0))
        win.blit(menu, (win_width / 2 - 350, win_height / 2 - 250))
        txt = font_obj2.render("Information", False, (255, 255, 255))
        win.blit(txt, (450, 105))
        txt = font_obj2.render("Return to Game: [U]", False, (255, 255, 255))
        win.blit(txt, (400, 145))
        txt = font_obj2.render("Fishing Rod: Right Click to Charge, Release to Throw", False, (255, 255, 255))
        win.blit(txt, (170, 220))
        txt = font_obj2.render("Lower/Raise Fish Hook: Scroll Button", False, (255, 255, 255))
        win.blit(txt, (170, 260))
        txt = font_obj2.render("Catch Fish: Press Cooresponding Fish Key that Appears", False, (255, 255, 255))
        win.blit(txt, (170, 300))
        txt = font_obj2.render("Possible Fish Keys: [W], [E], [R], [T], [F], [S]", False, (255, 255, 255))
        win.blit(txt, (170, 340))
        txt = font_obj2.render("Move Left/Right: [A] (left), [D] (right)", False, (255, 255, 255))
        win.blit(txt, (170, 380))
        txt = font_obj2.render("Purchase Item: Press Cooresponding Key in Shop Window", False, (255, 255, 255))
        win.blit(txt, (170, 420))
        txt = font_obj2.render("Retract Bobber: [Spacebar]", False, (255, 255, 255))
        win.blit(txt, (170, 460))
        txt = font_obj2.render("Your Goal: Survive", False, (255, 255, 255))
        win.blit(txt, (170, 500))

    if quest1 is not completed:
        if total_fish_caught >= 3:
            quest1 = completed
            cp += 1
            completed_quests.append(cp)
            quest_marker = True
            money += 30

    if quest2 is not completed:
        if orange_fish_caught >= 5:
            quest2 = completed
            cp += 1
            completed_quests.append(cp)
            quest_marker = True
            money += 60

    if quest3 is not completed:
        if red_fish_caught >= 5:
            quest3 = completed
            cp += 1
            completed_quests.append(cp)
            quest_marker = True
            money += 60

    if quest8 is not completed:
        if oranges >= 4:
            quest8 = completed
            cp += 1
            completed_quests.append(cp)
            quest_marker = True
            money += 60

    if quest10 is not unlocked:
        if len(completed_quests) == 9:
            quest10 = unlocked

# <<<<<<<  completed_quests = 9

    # for i in range(9):
    #     completed_quests.append(1)

    # Creates a yellow icon next to quests if you complete one
    if quest_menu is not True:
        for i in completed_quests:
            if i > 0 and keys[pygame.K_q]:
                quest_marker = False

        if quest_marker is True:
            pygame.draw.rect(win, "yellow", (595, 15, 3, 8))
            pygame.draw.rect(win, "yellow", (595, 27, 3, 3))

    # quest menu
    if quest_menu:
        menu = pygame.Surface((700, 500))
        menu.fill((0, 0, 0))
        win.blit(menu, (win_width / 2 - 350, win_height / 2 - 250))
        txt = font_obj2.render("Quests", False, (255, 255, 255))
        win.blit(txt, (450, 105))
        txt = font_obj2.render("Return to Game: [U]", False, (255, 255, 255))
        win.blit(txt, (370, 140))

        if quest1 is completed:
            quest1_txt = font_obj2.render("Catch 3 Fish: $30", False, (0, 255, 0))
        else:
            quest1_txt = font_obj2.render("Catch 3 Fish: $30", False, (255, 255, 255))
        win.blit(quest1_txt, (170, 180))

        if quest2 is completed:
            quest2_txt = font_obj2.render("Catch 5 Orange Fish: $60", False, (0, 255, 0))
        else:
            quest2_txt = font_obj2.render("Catch 5 Orange Fish: $60 --- " + str(int(orange_fish_caught)) + " Caught so Far", False, (255, 255, 255))
        win.blit(quest2_txt, (170, 220))

        if quest3 is completed:
            quest3_txt = font_obj2.render("Catch 5 Red Fish: $60", False, (0, 255, 0))
        else:
            quest3_txt = font_obj2.render("Catch 5 Red Fish: $60 --- " + str(int(red_fish_caught)) + " Caught so Far", False, (255, 255, 255))
        win.blit(quest3_txt, (170, 260))

        if quest4 is completed:
            quest4_txt = font_obj2.render("Defeat a Boss Fish: $100", False, (0, 255, 0))
        else:
            quest4_txt = font_obj2.render("Defeat a Boss Fish: $100", False, (255, 255, 255))
        win.blit(quest4_txt, (170, 300))

        if quest5 is completed:
            quest5_txt = font_obj2.render("Harpoon an Angler Fish: $75", False, (0, 255, 0))
        else:
            quest5_txt = font_obj2.render("Harpoon an Angler Fish: $75", False, (255, 255, 255))
        win.blit(quest5_txt, (170, 340))

        if quest6 is completed:
            quest6_txt = font_obj2.render("Harpoon a Shark: $75", False, (0, 255, 0))
        else:
            quest6_txt = font_obj2.render("Harpoon a Shark: $75", False, (255, 255, 255))
        win.blit(quest6_txt, (170, 380))

        if quest7 is completed:
            quest7_txt = font_obj2.render("Capture at Least 3 Fish with ONE Harpoon: $75", False, (0, 255, 0))
        else:
            quest7_txt = font_obj2.render("Capture at Least 3 Fish with ONE Harpoon: $75", False, (255, 255, 255))
        win.blit(quest7_txt, (170, 420))

        if quest8 is completed:
            quest8_txt = font_obj2.render("Purchase 4 Oranges: $100", False, (0, 255, 0))
        else:
            quest8_txt = font_obj2.render("Purchase 4 Oranges: $100 --- " + str(oranges) + " Purchased so Far", False, (255, 255, 255))
        win.blit(quest8_txt, (170, 460))

        if quest9 is completed:
            quest9_txt = font_obj2.render("Kill at Least 3 Fish of Any Type with a Single Cannon", False, (0, 255, 0))
        else:
            quest9_txt = font_obj2.render("Kill at Least 3 Fish of Any Type with a Single Cannon", False, (255, 255, 255))
        win.blit(quest9_txt, (170, 500))

        if quest10 is unlocked:
            win.fill((0, 0, 0))
            quest10_txt = font_obj2.render("DEFEND YOUR THRONE", False, (255, 0, 0))
            txtx = font_obj3.render("Return to Game: [U]", False, (255, 255, 255))
            win.blit(txtx, (400, 600))
            txtxt = font_obj3.render("(up/down movement enabled by w and s. left click to fire)",False,(255,255,255))
            win.blit((txtxt),(220,650))
            music_timer = 30.75
            beyond_revealed = True
            win.blit(quest10_txt, (380, 340))

        else:
            quest10_txt = font_obj2.render("COMPLETE ALL PREVIOUS QUESTS TO ASCEND", False, (255, 0, 0))
            win.blit(quest10_txt, (170, 540))

    if beyond_revealed is False:
        txt = font_obj2.render("[P] for info", False, (255, 255, 255))
        win.blit(txt, (400, 10))
        txt = font_obj2.render("[Q] for quests", False, (255, 255, 255))
        win.blit(txt, (600, 10))

    # lost screen
    if P.health <= 0:
        delta_time = 0
        if beyond_revealed is True:
            for i in fish4_list:
                fish4_list.remove(i)
            for i in MegaBoss_plist:
                MegaBoss_plist.remove(i)
        lose_screen = pygame.Surface((win_width, win_height))
        lose_screen.fill((200, 0, 0))
        win.blit(lose_screen, (0, 0))
        txt = font_obj.render("You Were Destroyed", False, (0, 0, 0))
        win.blit(txt, (320, 100))
        txt = font_obj.render("Days Survived: " + str(day), False, (0, 0, 0))
        win.blit(txt, (320, 150))
        txt = font_obj.render("Fish Caught: " + str(total_fish_caught), False, (0, 0, 0))
        win.blit(txt, (320, 200))
        txt = font_obj.render("Oranges Purchased: " + str(oranges), False, (0, 0, 0))
        win.blit(txt, (320, 250))
        txt = font_obj.render("Cannons Purchased: " + str(cannons), False, (0, 0, 0))
        win.blit(txt, (320, 300))
        txt = font_obj.render("Harpoons Purchased: " + str(harpoons), False, (0, 0, 0))
        win.blit(txt, (320, 350))
        txt = font_obj.render("Total Cash Earned: " + str(money + (oranges * 150) + (cannons * 70) + (harpoons * 250)), False, (0, 0, 0))
        win.blit(txt, (320, 400))
        txt = font_obj.render("Time Alive: " + str(round(time_survived, 1)) + " Seconds",
                              False, (0, 0, 0))
        win.blit(txt, (320, 450))
        if beyond_revealed is True:
            txt = font_obj.render("You Have Seen the Great Beyond...", False, (0, 0, 0))
            win.blit(txt, (270, 500))
            txt = font_obj.render("Thanks for Playing! :D", False, (0,0,0))
            win.blit(txt, (320, 550))
            txt = font_obj3.render("Developed by Trey Davidson and Zach Whitten. All sprites and music developed by Trey Davidson.",False,(0,0,0))
            win.blit(txt,(80,680))
        else:
            txt = font_obj.render("Your Quest for the Truth Sank with Your Boat...", False, (0, 0, 0))
            win.blit(txt, (160, 500))
            txt = font_obj3.render(
                "Developed by Trey Davidson and Zach Whitten. All sprites and music developed by Trey Davidson.", False,(0,0,0))
            win.blit(txt, (80, 680))
        delta_time = 0

    if beyond_revealed is True:
        projectile2_timer -= (delta_time + 0.05)
        if basic_fish_timer <= 0:
            basic_fish_timer = 5
            side = random.randint(1, 2)
            if side == 1:
                fish4_list.append(movingObj.MegaBossFish(win, -30, random.randint(30, win_height - 30), 100, side))
            if side == 2:
                fish4_list.append(movingObj.MegaBossFish(win, win_width + 30, random.randint(30, win_height - 30), 100, side))

        if projectile2_timer <= 0 and len(fish4_list) > 0:
            for M in fish4_list:
                MegaBoss_plist.append(movingObj.MegaFishProjectile(win, M.pos.x, M.pos.y, 10, 10))
                MegaBoss_plist.append(movingObj.MegaFishProjectile(win, M.pos.x, M.pos.y, 10, 10))
            projectile2_timer = 2

        for proj in MegaBoss_plist:
            proj.draw()
            if len(fish4_list) > 0:
                P.health = proj.update(delta_time, MegaBoss_plist, P.pos.x, P.pos.y, P.radius, P.health,
                                       fish4_list[0].moving)
            else:
                proj.pos.y += 50 * delta_time
                if proj.pos.y >= win_height + proj.radius:
                    MegaBoss_plist.remove(proj)


        for fish in fish4_list:
            P.health = fish.update(delta_time, fish4_list, P.pos.x, P.pos.y, P.radius, P.health)
            if fish.pos.y < P.pos.y:
                fish.alt_draw(spews)
            else:
                fish.draw(spews)

    if title_screen:
        win.blit(title,(0,0))
        pygame.draw.rect(win, (0, 0, 0), (380, 537, 250, 50))
        txt = font_obj2.render("Press [U] to Start", False, (200, 0, 0))
        win.blit(txt, (400, 550))

    pygame.display.flip()
pygame.quit()