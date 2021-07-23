# player class
import random
import vector
import pygame
import math

class Player:
    def __init__(self, surf):
        self.radius = 43
        self.pos = vector.Vector2(surf.get_width() / 2 - self.radius / 2, 220)
        self.speed = 200
        self.surf = surf
        self.casting = False
        self.B = None
        self.caught_fish = 0
        self.area = (0,0,87,90)
        self.frame = 0
        self.health = 100

    def handle_input(self, dt, fish1_list):
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()
        mpos = pygame.mouse.get_pos()
        mbuttons = pygame.mouse.get_pressed()

        if keys[pygame.K_ESCAPE]:
            done = True
            return done
        if event.type == pygame.QUIT:
            done = True
            return done


        # if clicking, draw a line from boat to mouse pos
        if mbuttons[2]:
            pygame.draw.line(self.surf, "red", (self.pos.x + self.radius / 2, self.pos.y + 20), (mpos[0], mpos[1]), 2)

        # if clicking, you are casting your line, so create a Bobber
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and self.casting != True:
            self.casting = True
            init_vel = vector.Vector2(self.pos.x + self.radius / 2, self.pos.y) - vector.Vector2(mpos[0], mpos[1])
            self.B = Bobber(self.pos.x + self.radius / 2, self.pos.y, init_vel.x, init_vel.y, 10)

        # if casting line and there isn't a bobber, create one
        if self.casting and self.B!=None:
            self.B.draw_bobber(self.surf, dt, self.pos, self.radius, event)

        # left and right movement
        if keys[pygame.K_d] and self.casting != True:
            self.pos.x += self.speed * dt
            self.frame += 1 * dt

        if keys[pygame.K_a] and self.casting != True:
            self.pos.x -= self.speed * dt
            self.frame += 1 * dt

        # you retrieve your bobber when you press spacebar
        # but you can't retrieve it while you're casting
        if keys[pygame.K_SPACE] and self.casting and self.B.position.y >= 250:
            self.casting = False
            self.B.hook_y = 0
            # fish disappears if you press spacebar with a fish
            for fish in fish1_list:
                if fish.caught:
                    fish.hitbox = False
                    fish.fish_speed = 300
                fish.caught = False

        # this code doesn't allow you to go off screen
        if self.pos.x > self.surf.get_width() - self.radius:
            self.pos.x = self.surf.get_width() - self.radius
        if self.pos.x < 0:
            self.pos.x = 0


    def update(self, flist, money):
        for fish in flist:
            if self.B != None and fish.hitbox == True:
                caught_fish = self.B.hooked(fish.pos.x, fish.pos.y, fish.radius, self.surf, fish.qte_key)
                if caught_fish:
                    fish.caught = True
                if fish.caught:
                    fish.pos.x = self.B.hook_x
                    fish.pos.y = self.B.hook_y
                    if fish.pos.y <= 250 + fish.radius:
                        flist.remove(fish)
                        money += random.randint(20, 27)
                        self.casting = False
                        self.caught_fish = 0
                        return money
        return money

    def draw_player(self,img):
        if self.frame > 0.25:
            self.area = (95,0,87,90)
            if self.frame > 0.5:
                self.area = (0,0,87,90)
                self.frame = 0
        self.surf.blit(img,self.pos,self.area)

class Bobber:
    def __init__(self, x, y, vel_x, vel_y, radius):
        self.velocity = vector.Vector2(vel_x, vel_y)
        self.color = vector.Vector3(255, 0, 0)
        self.radius = radius
        self.position = vector.Vector2(x, y)
        self.acceleration = vector.Vector2(0, 0)
        self.change_hook = False
        self.caught = False
        self.hook_x = None
        self.hook_y = None

    def draw_bobber(self, surf, dt, player_pos, player_rad, event):
        #global hook_x, hook_y
        self.position += self.velocity * dt

        self.acceleration = vector.Vector2(0, 0)

        if self.position.x > surf.get_width() - self.radius:
            self.position.x = surf.get_width() - self.radius

        if self.position.x < self.radius:
            self.position.x = self.radius
        
        # makes bobber fall
        if self.velocity.magnitude > 0:
            friction = 150 * (dt+0.65)**1/175
            self.velocity.y += friction
            if self.position.y > 250:
                self.velocity = vector.Vector2(0, 0)
                self.change_hook = True
                self.hook_x = self.position.x
                self.hook_y = self.position.y
            else:
                self.change_hook = False

        # if we get here, the bobber hit the water
        if self.change_hook:
            pygame.draw.line(surf, "white", (self.position), (self.hook_x, self.hook_y), 1)
            pygame.draw.circle(surf, "gold", (self.hook_x, self.hook_y), self.radius)

            # scroll to change hook_y
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                self.hook_y += 10
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                self.hook_y -= 10
            if self.hook_y <= 250:
                self.hook_y = 250

        pygame.draw.line(surf, "white", (player_pos.x + player_rad / 2, player_pos.y + 20), (self.position))
        pygame.draw.circle(surf, self.color, self.position, self.radius)

    def hooked(self, fish_x, fish_y, fish_rad, surf, qte_key):
        # checks distance from hook to fish
        if self.hook_x != None and self.hook_y != None:
            x_diff = fish_x - self.hook_x
            y_diff = fish_y - self.hook_y
            distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
            if distance <= fish_rad + self.radius:
                keys = pygame.key.get_pressed()
                font = pygame.font.SysFont("Courier New", 20)

                # if hook is over a fish, show text box with random key, return true if correct key is pressed
                if qte_key == 1:
                    qte_key = "R"
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_r]
                if qte_key == 2:
                    qte_key = "T"
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_t]
                if qte_key == 3:
                    qte_key = "F"
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_f]
                if qte_key == 4:
                    qte_key = "G"
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_g]
                if qte_key == 5:
                    qte_key = "C"
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_c]
                if qte_key == 6:
                    qte_key = "V"
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_v]

class BoringFish(Player):
    def __init__(self, surf, x, y, radius, side, qte_key):
        super().__init__(surf)
        self.side = side
        self.pos = vector.Vector2(x, y)
        self.radius = radius
        self.fish_speed = random.randint(50, 150)
        self.qte_key = qte_key
        self.caught = False
        self.area = (0, 0, 0, 0)
        self.type = random.randint(1, 2)
        self.hitbox = True

    def update(self, dt, fish_list):
        # side is 1 (left screen), move right
        if self.side == 1:
            self.pos.x += self.fish_speed * dt
            if self.type == 1:
                self.area = (0, 0, 78, 75)
            else:
                self.area = (85, 0, 85, 70)
        # side is 2 (right screen), move left
        if self.side == 2:
            self.pos.x += -(self.fish_speed * dt)
            if self.type == 1:
                self.area = (78,70,90,80)
            else:
                self.area = (0, 70, 90, 80)

        # remove fish if they go off screen
        for fish in fish_list:
            if fish.pos.x > self.surf.get_width() + 2 * fish.radius:
                fish_list.remove(fish)
            if fish.pos.x < -(2 * fish.radius):
                fish_list.remove(fish)

    def draw(self,img):
        self.surf.blit(img,(self.pos.x - 40,self.pos.y - 35 ),self.area)

class BiggerFish(Player):
    def __init__(self, surf, x, y, radius, side, qte_key):
        super().__init__(surf)
        self.side = side
        self.pos = vector.Vector2(x, y)
        self.radius = radius
        self.fish_speed = 150
        self.qte_key = qte_key
        self.area = (0,0,0,0)
        self.type = random.randint(1,2)

    def update(self, dt, bor_fish_list, big_fish_list):
        # side is 1 (left screen), move right
        if self.side == 1:
            self.pos.x += self.fish_speed * dt
            if self.type == 1:
                self.area = (200,0,125,90)
            else:
                self.area = (0, 150, 150, 100)
                self.radius = 60
        # side is 2 (right screen), move left
        if self.side == 2:
            self.pos.x += -(self.fish_speed * dt)
            if self.type == 1:
                self.area = (330,0,125,90)
            else:
                self.area = (150, 150, 160, 100)
                self.radius = 60

        # remove fish if they go off screen
        for big_fish in big_fish_list:
            if big_fish.pos.x > self.surf.get_width() + 2 * big_fish.radius:
                big_fish_list.remove(big_fish)
            if big_fish.pos.x < -(2 * big_fish.radius):
                big_fish_list.remove(big_fish)

            # if a big fish hits a small fish, remove it
            for lit_fish in bor_fish_list:
                x_diff = big_fish.pos.x - lit_fish.pos.x
                y_diff = big_fish.pos.y - lit_fish.pos.y
                distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
                if distance <= big_fish.radius + lit_fish.radius:
                    big_fish_list.remove(big_fish)

    def draw(self, img):
        self.surf.blit(img, (self.pos.x - 65, self.pos.y - 60), self.area)


class BossFish(Player):
    def __init__(self, surf, x, y, radius, side):
        super().__init__(surf)
        self.side = side
        self.pos = vector.Vector2(x, y)
        self.radius = radius
        self.fish_speed = 100
        self.moving = True
        self.proj_list = []

    def update(self, dt, fish_list):
        # side is 1 (left screen), move right
        if self.moving == True:
            self.pos.y -= self.fish_speed * dt
            # self.pos.x += random.randint(1, 2)
            # self.pos.x -= random.randint(1, 2)
        if self.pos.y <= self.surf.get_height() - self.radius:
            self.pos.y = self.surf.get_height() - self.radius
            self.moving = False
        # if self.side == 1:
        #     self.pos.x += self.fish_speed * dt
            # if self.type == 1:
            #     self.area = (0,0,78,75)
            # else:
            #     self.area = (85, 0, 85, 75)
        # side is 2 (right screen), move left
        # if self.side == 2:
        #     self.pos.x += -(self.fish_speed * dt)
            # if self.type == 1:
            #     self.area = (78,70,90,80)
            # else:
            #     self.area = (0, 70, 90, 80)

        # for fish in fish_list:
        #     if fish.pos.x > self.surf.get_width() + 2 * fish.radius:
        #         fish_list.remove(fish)
        #     if fish.pos.x < -(2 * fish.radius):
        #         fish_list.remove(fish)

    def draw(self,img):
       # pygame.draw.circle(self.surf, "white", (self.pos.x, self.pos.y), self.radius)
       self.surf.blit(img,(self.pos.x - 170,self.pos.y - 260),(0,60,400,600))

class FishProjectile(Player):
    def __init__(self, surf, x, y, radius, side, proj_speed):
        super().__init__(surf)
        self.pos = vector.Vector2(x, y)
        self.proj_speed = proj_speed
        self.radius = radius
        self.side = side

    def draw(self):
        pygame.draw.circle(self.surf, "white", (self.pos.x, self.pos.y), self.radius)

    def update(self, dt, plist, player_x, player_y, player_rad, player_health, wait):
        # if boss fish is done moving
        if wait != True:
            for proj in plist:
                proj.proj_path(dt)
                #proj.pos.y -= self.proj_speed * dt
                # if len(plist) % 2 == 0:
                #     # make x right
                #     proj.pos.x += 50 * dt
                # if len(plist) % 2 > 0:
                #     # make x left
                #     proj.pos.x -= 50 * dt
                if proj.pos.y <= -player_rad:
                    plist.remove(proj)

                # check distance from projectile to player
                x_diff = proj.pos.x - player_x - player_rad
                y_diff = proj.pos.y - player_y - 10
                distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
                if distance <= proj.radius + player_rad:
                    plist.remove(proj)
                    # player loses some health

    def proj_path(self, dt):
        self.pos.y -= self.proj_speed * dt