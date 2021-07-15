# player class
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

        # this code doesn't allow you to go off screen
        if self.pos.x > self.surf.get_width() - self.radius:
            self.pos.x = self.surf.get_width() - self.radius

        if self.pos.x < 0:
            self.pos.x = 0


    def draw_player(self):
        pygame.draw.rect(self.surf, "white", (self.pos.x, self.pos.y, self.radius, self.radius))
