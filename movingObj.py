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
        self.bar_area = (0,0,130,70)
        self.frame = 0
        self.health = 100
        self.harpoons = 1
        self.harpoon_is_active = False
        self.init_vel = 0
        self.harpy = 0
        self.harpx = 0
        self.orange_fish_caught = 0
        self.red_fish_caught = 0
        self.total_fish_caught = 0
        self.proj_list = []

    def handle_input(self, dt, fish1_list,witnessed, fish4_list):
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
        if mbuttons[2] and self.casting is not True and witnessed is False:
            pygame.draw.line(self.surf, "red", (self.pos.x + self.radius / 2, self.pos.y + 20), (mpos[0], mpos[1]), 2)

        # if clicking, you are casting your line, so create a Bobber
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and self.casting != True and witnessed is False:
            self.casting = True
            init_vel = vector.Vector2(self.pos.x + self.radius / 2, self.pos.y) - vector.Vector2(mpos[0], mpos[1])
            self.B = Bobber(self.pos.x + self.radius / 2, self.pos.y, init_vel.x, init_vel.y, 10)

        # if casting line and there isn't a bobber, create one
        if self.casting and self.B!=None:
            self.B.draw_bobber(self.surf, dt, self.pos, self.radius, event)

        # left and right movement / up and down
        if witnessed:
            self.speed = 350
        if keys[pygame.K_d]:# and self.casting != True:
            self.pos.x += self.speed * dt
            self.frame += 1 * dt

        # you can shoot if endgame is active
        if witnessed is True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mpos_x = mpos[0]
                mpos_y = mpos[1]
                init_vel = vector.Vector2(mpos_x, mpos_y) - vector.Vector2(self.pos.x, self.pos.y)
                self.proj_list.append(PlayerShot(self.surf, self.pos.x, self.pos.y, 15, init_vel[0], init_vel[1]))

            for proj in self.proj_list:
                proj.update(dt, fish4_list)
                proj.draw()
                if proj.pos.x >= self.surf.get_width() + proj.radius:
                    self.proj_list.remove(proj)
                if proj.pos.x <= -proj.radius:
                    self.proj_list.remove(proj)
                if proj.pos.y >= self.surf.get_height() + proj.radius:
                    self.proj_list.remove(proj)
                if proj.pos.y <= -proj.radius:
                    self.proj_list.remove(proj)

        if keys[pygame.K_a]:
            self.pos.x -= self.speed * dt
            self.frame += 1 * dt

        if keys[pygame.K_w] and witnessed == True:
            self.pos.y -= self.speed * dt

        if keys[pygame.K_s] and witnessed == True:
            self.pos.y += self.speed * dt

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
        if self.pos.x > self.surf.get_width() - self.radius * 2 and witnessed is False:
            self.pos.x = self.surf.get_width() - self.radius * 2
        elif self.pos.x > self.surf.get_width() - 350 and witnessed is True:
            self.pos.x = self.surf.get_width() - 350
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > self.surf.get_height() - 260:
            self.pos.y = self.surf.get_height() - 260

    def update(self, flist, money):
        for fish in flist:
            if self.B != None and fish.hitbox == True:
                caught_fish = self.B.hooked(fish.pos.x, fish.pos.y, fish.radius, self.surf, fish.qte_key, fish.pulling)
                if caught_fish:
                    fish.caught = True
                    fish.pulling = True
                if fish.caught:
                    fish.pos.x = self.B.hook_x
                    fish.pos.y = self.B.hook_y
                    if fish.pos.y <= 250 + fish.radius:
                        flist.remove(fish)
                        money += random.randint(20, 27)
                        self.casting = False
                        self.caught_fish = 0
                        self.total_fish_caught += 1
                        if fish.color == "orange":
                            self.orange_fish_caught += 1
                            return money, self.total_fish_caught, self.orange_fish_caught, self.red_fish_caught
                        if fish.color == "red":
                            self.red_fish_caught += 1
                            return money, self.total_fish_caught, self.orange_fish_caught, self.red_fish_caught
        return money, self.total_fish_caught, self.orange_fish_caught, self.red_fish_caught

    def draw_player(self,img,bar_img,revel):
        if self.frame > 0.25:
            self.area = (95,0,87,90)
            self.bar_area = (0,0,130,70)
            if self.frame > 0.5:
                self.area = (0,0,87,90)
                self.frame = 0
                # self.bar_area = (145, -3, 140, 70)

        for hp in range(int(self.health)):
            pygame.draw.rect(self.surf,(100,255,200),(879 + (hp * 0.95),31,1,10))
        if revel is False:
            self.surf.blit(img,self.pos,self.area)
        else:
            self.surf.blit(img,(self.pos.x - 170, self.pos.y - 120))

        self.surf.blit(bar_img,(870,10),self.bar_area)

class PlayerShot:
    def __init__(self, surf, x, y, radius, velx, vely):
        self.surf = surf
        self.pos = vector.Vector2(x, y)
        self.radius = radius
        self.velocity = vector.Vector2(velx, vely)

    def update(self, dt, Mplist):
        self.pos += self.velocity * dt
        for proj in Mplist:
            dist = distance(proj.pos.x, self.pos.x, proj.pos.y, self.pos.y)
            if dist <= proj.radius + self.radius:
                Mplist.remove(proj)

    def draw(self):
        pygame.draw.circle(self.surf, "green", (self.pos), self.radius)

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
            friction = 500 * dt#(dt+0.65)**1/175
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

    def hooked(self, fish_x, fish_y, fish_rad, surf, qte_key, fish_pulling):
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
                    qte_key = "S"
                    if fish_pulling is not True:
                        txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                        surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_s]
                if qte_key == 2:
                    qte_key = "W"
                    if fish_pulling is not True:
                        txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                        surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_w]
                if qte_key == 3:
                    qte_key = "E"
                    if fish_pulling is not True:
                        txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                        surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_e]
                if qte_key == 4:
                    qte_key = "R"
                    if fish_pulling is not True:
                        txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                        surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_r]
                if qte_key == 5:
                    qte_key = "T"
                    if fish_pulling is not True:
                        txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                        surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_t]
                if qte_key == 6:
                    qte_key = "F"
                    if fish_pulling is not True:
                        txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                        surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_f]

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
        self.color = None
        self.pulling = False

    def update(self, dt, fish_list):
        # side is 1 (left screen), move right
        if self.side == 1:
            self.pos.x += self.fish_speed * dt
            if self.type == 1:
                self.area = (0, 0, 78, 75)
                self.color = "orange"
            else:
                self.area = (85, 0, 85, 70)
                self.color = "red"
        # side is 2 (right screen), move left
        if self.side == 2:
            self.pos.x += -(self.fish_speed * dt)
            if self.type == 1:
                self.area = (78,70,90,80)
                self.color = "orange"
            else:
                self.area = (0, 70, 90, 80)
                self.color = "red"

        # remove fish if they go off screen
        for fish in fish_list:
            if fish.pos.x > self.surf.get_width() + 2 * fish.radius:
                fish_list.remove(fish)
            if fish.pos.x < -(2 * fish.radius):
                fish_list.remove(fish)

        return self.color

    def draw(self,img):
        self.surf.blit(img,(self.pos.x - 40,self.pos.y - 35 ),self.area)

class BiggerFish(Player):
    def __init__(self, surf, x, y, radius, side, qte_key):
        super().__init__(surf)
        self.side = side
        self.pos = vector.Vector2(x, y)
        self.radius = radius
        self.fish_speed = 300
        self.qte_key = qte_key
        self.area = (0,0,0,0)
        self.type = random.randint(1,2)
        self.caught = False
        self.total_big_fish_caught = 0
        self.is_angler = None
        self.is_shark = None
        self.angler_caught = 0
        self.shark_caught = 0

    def update(self, dt, bor_fish_list, big_fish_list):
        # side is 1 (left screen), move right
        if self.side == 1:
            self.pos.x += self.fish_speed * dt
            if self.type == 1:
                self.is_angler = True
                self.area = (200,0,125,90)
            else:
                self.is_shark = True
                self.area = (0, 150, 150, 100)
                self.radius = 60
        # side is 2 (right screen), move left
        if self.side == 2:
            self.pos.x += -(self.fish_speed * dt)
            if self.type == 1:
                self.is_angler = True
                self.area = (330,0,125,90)
            else:
                self.is_shark = True
                self.area = (150, 150, 160, 100)
                self.radius = 60

        # remove fish if they go off screen
        #for big_fish in big_fish_list:
        for big_fish in big_fish_list:
            if big_fish.pos.x > self.surf.get_width() + 2 * big_fish.radius:
                big_fish_list.remove(big_fish)
            if big_fish.pos.x < -(2 * big_fish.radius):
                big_fish_list.remove(big_fish)

        # if a big fish hits a small fish, remove it
        if self.caught != True:
            for lit_fish in bor_fish_list:
                x_diff = self.pos.x - lit_fish.pos.x
                y_diff = self.pos.y - lit_fish.pos.y
                distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
                if distance <= self.radius + lit_fish.radius:
                    bor_fish_list.remove(lit_fish)



    def draw(self, img):
        self.surf.blit(img, (self.pos.x - 65, self.pos.y - 60), self.area)


class BossFish(Player):
    def __init__(self, surf, x, y, radius, side):
        super().__init__(surf)
        self.side = side
        self.pos = vector.Vector2(x, y)
        self.radius = radius
        self.fish_speed = 60
        self.moving = True
        self.proj_list = []
        self.health = 1
        self.defeated = False

    def update(self, dt, fish_list):
        # side is 1 (left screen), move right
        if self.moving == True:
            self.pos.y -= self.fish_speed * dt
            # self.pos.x += random.randint(1, 2)
            # self.pos.x -= random.randint(1, 2)
        if self.pos.y <= self.surf.get_height() - 200:
            self.pos.y = self.surf.get_height() - 200
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
       self.surf.blit(img,(self.pos.x - 170,self.pos.y - 100),(0,60,400,600))

class MegaBossFish:
    def __init__(self, surf, x, y, radius, side):
        self.side = side
        self.surf = surf
        self.pos = vector.Vector2(x, y)
        self.radius = radius
        self.fish_speed = 200
        self.moving = True
        self.proj_list = []
        self.health = 1
        self.defeated = False
        self.in_bounds = False
        if self.side == 1:
            self.flipped = False
        else:
            self.flipped = True

    def update(self, dt, fish_list, Px, Py, Pradius, Phealth):
        if self.side == 1:
            if self.pos.x > self.radius - 1:
                self.in_bounds = True
            if self.flipped is False:
                self.pos.x += self.fish_speed * dt
            if self.flipped is True:
                self.pos.x -= self.fish_speed * dt

            if self.pos.x >= self.surf.get_width() - self.radius + 1:
                self.flipped = not self.flipped

            if self.pos.x < self.radius - 1 and self.in_bounds is True:
                self.flipped = not self.flipped

        if self.side == 2:
            if self.pos.x < self.surf.get_width() - self.radius + 1:
                self.in_bounds = True
            if self.flipped is False:
                self.pos.x += self.fish_speed * dt
            if self.flipped is True:
                self.pos.x -= self.fish_speed * dt

            if self.pos.x >= self.surf.get_width() - self.radius + 1 and self.in_bounds is True:
                self.flipped = not self.flipped

            if self.pos.x < self.radius - 1:
                self.flipped = not self.flipped

        for fish in fish_list:
            dist = distance(fish.pos.x, Px, fish.pos.y, Py)
            if dist <= fish.radius + Pradius:
                Phealth -= 10 * dt
        return Phealth


    def draw(self):
        pygame.draw.circle(self.surf, "white", (self.pos), self.radius)

class FishProjectile(Player):
    def __init__(self, surf, x, y, radius, side, proj_speed):
        super().__init__(surf)
        self.pos = vector.Vector2(x, y)
        self.proj_speed = proj_speed
        self.radius = radius
        self.side = side
        self.velocity = vector.Vector2(random.randint(-60, 60), 0)

    def draw(self):
        pygame.draw.circle(self.surf, "white", (self.pos.x, self.pos.y), self.radius)

    def update(self, dt, plist, player_x, player_y, player_rad, player_health, wait):
        # if boss fish is done moving
        if wait != True:
            for proj in plist:
                proj.proj_path(dt)

                if proj.pos.y <= -player_rad:
                    plist.remove(proj)
                if proj.pos.x <= -player_rad:
                    plist.remove(proj)
                if proj.pos.x >= self.surf.get_width() + player_rad:
                    plist.remove(proj)

                # check distance from projectile to player
                x_diff = proj.pos.x - player_x - player_rad
                y_diff = proj.pos.y - player_y - 10
                distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
                if distance <= proj.radius + player_rad:
                    plist.remove(proj)
                    # player loses some health
                    player_health -= 10
                    return player_health
        return player_health

    def proj_path(self, dt):
        self.pos.y -= self.proj_speed * dt
        self.pos.x += self.velocity.x * dt

class Harpoon:
    def __init__(self, surf, hx, hy, velx, vely):
        self.surf = surf
        self.orientation = 0
        self.velocity = vector.Vector2(velx, vely)
        self.pos = vector.Vector2(hx, hy)
        self.direction = "Down"
        self.radius = 20
        self.fish_num = 0
        self.big_fish_value = 0
        self.harpoon_active = False
        self.fish_on_a_stick = 0

    def update(self, dt, Pposx, Pposy, harp_list, fish1_list, fish2_list, money):
        self.harpoon_active = True
        if self.direction == "Down":
            self.pos += self.velocity * dt
            self.velocity.y += 250 * dt
            if self.velocity.y == 0:
                self.velocity.y = 0
            if self.pos.y >= self.surf.get_height() - self.radius:
                self.direction = "Up"

            elif self.pos.x >= self.surf.get_width() - self.radius:
                self.direction = "Up"

            elif self.pos.x <= self.radius:
                self.direction = "Up"

        if self.direction == "Up":
            returning_vel = vector.Vector2(Pposx, Pposy) - vector.Vector2(self.pos.x, self.pos.y)
            self.pos += returning_vel * dt

        for fish in fish1_list:
            dist = distance(fish.pos.x, self.pos.x, fish.pos.y, self.pos.y)
            if dist <= fish.radius + self.radius and fish.caught is not True:
                fish.pos = self.pos
                if self.direction == "Up":
                    if fish.pos.y <= 275:
                        self.fish_num += 1
                        self.fish_on_a_stick += 1
                        fish1_list.remove(fish)

        for fish in fish2_list:
            dist = distance(fish.pos.x, self.pos.x, fish.pos.y, self.pos.y)
            if dist <= fish.radius + self.radius:
                fish.pos = self.pos
                fish.caught = True
                if self.direction == "Up":
                    if fish.pos.y <= 275:
                        self.big_fish_value = 220
                        if fish.is_angler:
                            fish.angler_caught += 1
                        if fish.is_shark:
                            fish.shark_caught += 1
                        self.fish_on_a_stick += 1
                        fish2_list.remove(fish)
                        return money, self.harpoon_active, fish.angler_caught, fish.shark_caught, self.fish_on_a_stick


        for harp in harp_list:
            if self.direction == "Up":
                if harp.pos.y <= 270:
                    harp_list.remove(harp)
                    money += (random.randint(21, 27) * self.fish_num) + self.big_fish_value
                    self.harpoon_active = False
                    #return money, self.harpoon_active, None, None, None
                
        return money, self.harpoon_active, None, None, self.fish_on_a_stick

    def draw(self, Pposx, Pposy):
        pygame.draw.line(self.surf, (107, 72, 12), (Pposx + 45, Pposy + 30), (self.pos), 5)
        #pygame.draw.circle(self.surf, "black", (self.pos), self.radius)
        A = self.pos.x + 15, self.pos.y
        B = self.pos.x, self.pos.y + 30
        C = self.pos.x - 15, self.pos.y
        pygame.draw.polygon(self.surf, "light grey", (A, B, C))

class Cannon:
    def __init__(self, surf, x, y):
        self.surf = surf
        self.radius = 20
        self.pos = vector.Vector2(x + 40, y + 20)
        self.velocity = vector.Vector2(0, 300)
        self.hitbox = True
        self.boss_kills = 0
        self.kills = 0

    def update(self, dt, f1_list, f2_list, f3_list, cannon_list):
        self.pos.y += self.velocity.y * dt
        for cannon in cannon_list:
            if cannon.pos.y >= self.surf.get_height() + cannon.radius:
                cannon_list.remove(cannon)

        for lit_fish in f1_list:
            dist = distance(lit_fish.pos.x, self.pos.x, lit_fish.pos.y, self.pos.y)
            if dist <= lit_fish.radius + self.radius:
                self.kills += 1
                f1_list.remove(lit_fish)

        for big_fish in f2_list:
            dist = distance(big_fish.pos.x, self.pos.x, big_fish.pos.y, self.pos.y)
            if dist <= big_fish.radius + self.radius:
                self.kills += 1
                f2_list.remove(big_fish)

        for boss_fish in f3_list:
            dist = distance(boss_fish.pos.x, self.pos.x, boss_fish.pos.y, self.pos.y)
            if dist <= boss_fish.radius + self.radius and self.hitbox:
                boss_fish.health -= 1
                self.hitbox = False
                if boss_fish.health <= 0:
                    f3_list.remove(boss_fish)
                    self.boss_kills += 1

        return self.boss_kills, self.kills

    def draw(self):
        pygame.draw.circle(self.surf, (60, 60, 60), (self.pos), self.radius)


class MegaFishProjectile(Player):
    def __init__(self, surf, x, y, radius, proj_speed):
        super().__init__(surf)
        self.pos = vector.Vector2(x, y)
        self.proj_speed = proj_speed
        self.radius = radius
        self.velocity = vector.Vector2(random.randint(-60, 60), random.randint(-60, 60))

    def draw(self):
        pygame.draw.circle(self.surf, "white", (self.pos.x, self.pos.y), self.radius)

    def update(self, dt, plist, player_x, player_y, player_rad, player_health, wait):
        # if boss fish is done moving
        for proj in plist:
            proj.proj_path(dt)

            if proj.pos.y <= -player_rad:
                plist.remove(proj)
            if proj.pos.y >= self.surf.get_height() + player_rad:
                plist.remove(proj)
            if proj.pos.x <= -player_rad:
                plist.remove(proj)
            if proj.pos.x >= self.surf.get_width() + player_rad:
                plist.remove(proj)

            # check distance from projectile to player
            x_diff = proj.pos.x - player_x - player_rad
            y_diff = proj.pos.y - player_y - 10
            distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
            if distance <= proj.radius + player_rad:
                plist.remove(proj)
                # player loses some health
                player_health -= 10
                return player_health
        return player_health

    def proj_path(self, dt):
            self.pos += self.velocity * dt

def distance(x1, x2, y1, y2):
    x_diff = x1 - x2
    y_diff = y1 - y2
    return (x_diff ** 2 + y_diff ** 2) ** 0.5