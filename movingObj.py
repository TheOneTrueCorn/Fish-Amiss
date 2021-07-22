# player class
import random
import vector
import pygame
class Player:
    def __init__(self, surf):
        self.radius = 50
        self.pos = vector.Vector2(surf.get_width() / 2 - self.radius / 2, 200)
        self.speed = 200
        self.surf = surf
        self.casting = False
        self.B = None

    def handle_input(self, dt):
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
            pygame.draw.line(self.surf, "red", (self.pos.x + self.radius / 2, self.pos.y), (mpos[0], mpos[1]), 2)

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

        if keys[pygame.K_a] and self.casting != True:
            self.pos.x -= self.speed * dt

        # you retrieve your bobber when you press spacebar
        # but you can't retrieve it while you're casting
        if keys[pygame.K_SPACE] and self.casting and self.B.position.y >= 250:
            self.casting = False

        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     Fish(self.surf, 3, 300, 300)

        # this code doesn't allow you to go off screen
        if self.pos.x > self.surf.get_width() - self.radius:
            self.pos.x = self.surf.get_width() - self.radius
        if self.pos.x < 0:
            self.pos.x = 0

    def update(self, flist, money):
        for fish in flist:
            if self.B != None:
                caught_fish = self.B.hooked(fish.pos.x, fish.pos.y, fish.radius, self.surf, fish.qte_key)
                if caught_fish:
                    fish.pos.x = self.B.hook_x
                    fish.pos.y = self.B.hook_y
                    if fish.pos.y <= 250 + fish.radius:
                        flist.remove(fish)
                        money += random.randint(20, 27)
                        self.casting = False
                        return money
        return money

    def draw_player(self):
        pygame.draw.rect(self.surf, "white", (self.pos.x, self.pos.y, self.radius, self.radius))

class Bobber:
    def __init__(self, x, y, vel_x, vel_y, radius):
        self.velocity = vector.Vector2(vel_x, vel_y)
        self.color = vector.Vector3(255, 0, 0)
        self.radius = radius
        self.position = vector.Vector2(x, y)
        self.acceleration = vector.Vector2(0, 0)
        self.change_hook = False
        # do same thing with B, change from global to attribute
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

        pygame.draw.line(surf, "white", (player_pos.x + player_rad / 2, player_pos.y), (self.position))
        pygame.draw.circle(surf, self.color, self.position, self.radius)

    # ISN'T CALLED ANYWHERE
    def hooked(self, fish_x, fish_y, fish_rad, surf, qte_key):
        if self.hook_x != None and self.hook_y != None:
            x_diff = fish_x - self.hook_x
            y_diff = fish_y - self.hook_y
            distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
            if distance <= fish_rad + self.radius:
                keys = pygame.key.get_pressed()
                
                if qte_key == 1:
                    qte_key = "R"
                    font = pygame.font.SysFont("Courier New", 20)
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_r]
                if qte_key == 2:
                    qte_key = "T"
                    font = pygame.font.SysFont("Courier New", 20)
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_t]
                if qte_key == 3:
                    qte_key = "F"
                    font = pygame.font.SysFont("Courier New", 20)
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_f]
                if qte_key == 4:
                    qte_key = "G"
                    font = pygame.font.SysFont("Courier New", 20)
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_g]
                if qte_key == 5:
                    qte_key = "C"
                    font = pygame.font.SysFont("Courier New", 20)
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_c]
                if qte_key == 6:
                    qte_key = "V"
                    font = pygame.font.SysFont("Courier New", 20)
                    txt = font.render("press [" + str(qte_key) + "]", False, (255, 255, 255))
                    surf.blit(txt, (self.hook_x - 30, self.hook_y + 10))
                    return keys[pygame.K_v]





                # success = Player.QTE(surf)
                # if success:
                #     print("EDD")
                #     fish_x = self.hook_x
                #     fish_y = self.hook_y
                # else:
                #     pass

class BoringFish(Player):
    def __init__(self, surf, x, y, radius, side, qte_key):
        super().__init__(surf)
        self.side = side
        self.pos = vector.Vector2(x, y)
        self.radius = radius
        self.fish_speed = random.randint(50, 150)
        self.qte_key = qte_key

    def update(self, dt, fish_list):
        # side is 1 (left screen), move right
        if self.side == 1:
            self.pos.x += self.fish_speed * dt
        # side is 2 (right screen), move left
        if self.side == 2:
            self.pos.x += -(self.fish_speed * dt)

        for fish in fish_list:
            if fish.pos.x > self.surf.get_width() + 2 * fish.radius:
                fish_list.remove(fish)
            if fish.pos.x < -(2 * fish.radius):
                fish_list.remove(fish)

    def draw(self):
        pygame.draw.circle(self.surf, "green", (self.pos.x, self.pos.y), self.radius)