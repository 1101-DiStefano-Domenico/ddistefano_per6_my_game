import pygame as pg

from pygame.sprite import Sprite

from settings import *

vec = pg.math.Vector2

# player class
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
    def input(self):
        keystate = pg.key.get_pressed()

        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keystate[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keystate[pg.K_s]:
            self.acc.y = PLAYER_ACC
        if keystate[pg.K_r]:
            self.pos = vec(WIDTH/2, HEIGHT/2)

        # velocity cap
        # if self.vel.x > 6:
        #     self.vel.x = 6
        # if self.vel.y > 6:
        #     self.vel.y = 6
        # if self.vel.x < -6:
        #     self.vel.x = -6
        # if self.vel.y < -6:
        #     self.vel.y = -6
        
    # this is a method that will keep the sprite on screen
    def inbounds(self):
        width = 50
        height = 50
        if self.rect.x > WIDTH - width:
            self.pos.x = WIDTH - width/2
            self.vel.x = 0
        if self.rect.x < 0:
            self.pos.x = width/2
            self.vel.x = 0
        if self.rect.y > HEIGHT - height:
            self.pos.y = HEIGHT - height/2
            self.vel.y = 0
        if self.rect.y < 0:
            self.pos.y = height/2
            self.vel.y = 0
        
    def update(self):
        self.inbounds()
        self.acc = self.vel * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

# mob class
class Mob(Sprite):
    def __init__(self,width,height):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1

    # this is a method that will keep the sprite on screen
    def inbounds(self):
        if self.rect.x > WIDTH - self.width:
            self.pos.x = WIDTH - self.width/2
            self.vel.x = 0
        if self.rect.x < 0:
            self.pos.x = self.width/2
            self.vel.x = 0
        if self.rect.y > HEIGHT - self.height:
            self.pos.y = HEIGHT - self.height/2
            self.vel.y = 0
        if self.rect.y < 0:
            self.pos.y = self.height/2
            self.vel.y = 0
    def behavior(self):
        # print(self.vel)
        self.acc.x = -PLAYER_ACC
        
    def update(self):
        self.inbounds()
        self.acc = self.vel * MOB_FRICTION
        self.vel += self.acc
        self.behavior()
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
