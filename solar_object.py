import random

import pygame
import vector
import math
import random

class BackgroundObject:
    def __init__(self,x,y):
        self.start_pos = vector.Vector2(x, y)
        self.angle = -15
        self.rotation_speed = 360
        self.sun_color = (random.randint(175,230),random.randint(25,100),random.randint(60,100))
        self.moon_color = (random.randint(175, 230), random.randint(175, 230), random.randint(60, 100))
        self.end = vector.Vector2(0,0)

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

    def draw(self,surf,ascended,img):
        dist = 425
        p0 = (self.start_pos[0], self.start_pos[1])
        forward = self.get_forward()
        self.end = vector.Vector2(p0[0], p0[1]) + forward * dist
        if not ascended:
            pygame.draw.circle(surf,(self.sun_color),self.end,100)
        else:
            surf.blit(img,self.end)


    def alt_draw(self,surf,color,ascended,img):
        dist = 425
        p0 = (self.start_pos[0], self.start_pos[1])
        forward = -self.get_forward()
        self.end = vector.Vector2(p0[0], p0[1]) + forward * dist
        if not ascended:
            pygame.draw.circle(surf,(self.moon_color),self.end,80)
            pygame.draw.circle(surf, (color), (self.end[0]-20, self.end[1]), 61)
        else:
            surf.blit(img,self.end)




