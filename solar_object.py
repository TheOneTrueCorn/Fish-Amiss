import pygame
import vector
import math

class backgroundObject:
    def __init__(self,x,y):
        self.start_pos = vector.Vector2(x, y)
        self.angle = -15
        self.rotation_speed = 360

    def get_forward(self):
        radians = math.radians(self.angle)
        d_hat = vector.polar_to_vector2(radians, 1.0)
        return d_hat

    def update(self, dt):
        d_hat = self.get_forward()
        self.rotation_speed = 360
        self.angle -= self.rotation_speed * dt / 60

    def alt_update(self, dt):
        d_hat = self.get_forward()
        self.rotation_speed = 360
        self.angle -= self.rotation_speed * dt / 60

    def draw(self,surf):
        dist = 425
        p0 = (self.start_pos[0], self.start_pos[1])
        forward = self.get_forward()
        end = vector.Vector2(p0[0], p0[1]) + forward * dist
        pygame.draw.circle(surf,(200,50,100),end,100)

    def alt_draw(self,surf,color):
        dist = 425
        p0 = (self.start_pos[0], self.start_pos[1])
        forward = -self.get_forward()
        end = vector.Vector2(p0[0], p0[1]) + forward * dist
        pygame.draw.circle(surf,(200,200,100),end,80)
        pygame.draw.circle(surf, (color), (end[0]-20,end[1]), 61)


