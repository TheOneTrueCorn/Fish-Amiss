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

    def handle_input(self, dt):
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            done = True
            return done
        if event.type == pygame.QUIT:
            done = True
            return done

        # left and right movement
        if keys[pygame.K_d]:
            self.pos.x += self.speed * dt

        if keys[pygame.K_a]:
            self.pos.x -= self.speed * dt

        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     Fish(self.surf, 3, 300, 300)

        # this code doesn't allow you to go off screen
        if self.pos.x > self.surf.get_width() - self.radius:
            self.pos.x = self.surf.get_width() - self.radius

        if self.pos.x < 0:
            self.pos.x = 0

    def draw_player(self):
        pygame.draw.rect(self.surf, "white", (self.pos.x, self.pos.y, self.radius, self.radius))


class Fish(Player):
    def __init__(self, surf, num_fish, radius):
        super().__init__(surf)
        self.radius = radius
        self.fish_list = []
        for i in range(num_fish):
            self.fish_list.append(random.randint(300, surf.get_height() - self.radius))

    # def update(self, dt):
    #     for i in self.fish_list:
    #         self.pos.x += 30 * dt

    # def draw(self, speed):
    #     for fish in self.fish_list:
    #         pygame.draw.circle(self.surf, "green", (0 + speed, fish), self.radius)

class BoringFish(Fish):
    def __init__(self, surf, num_fish, radius):
        super().__init__(surf, num_fish, radius)
        
    def draw(self, speed):
        for fish in self.fish_list:
            pygame.draw.circle(self.surf, "green", (0 + speed, fish), self.radius)