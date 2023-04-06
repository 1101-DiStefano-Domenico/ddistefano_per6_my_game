import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
import math


vec = pg.math.Vector2

# player class
class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((50,50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.hp = HEALTH
        self.score = SCORE

    # method that takes user input and applies acceleration to the sprite
    def input(self):
        keystate = pg.key.get_pressed()

        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            # print("im inputing")
        if keystate[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keystate[pg.K_w]:
            self.acc.y = -PLAYER_ACC
        if keystate[pg.K_s]:
            self.acc.y = PLAYER_ACC
        if keystate[pg.K_r]:
            self.pos = vec(WIDTH/2, HEIGHT/2)
            self.hp = 100
        
            

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
    
    # method that detects mob collision and then subtracts from hp pool and slows player when colliding
    def mob_collide(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.vel.x *= 0
            self.vel.y *= 0
            self.hp -= 1       
    
    # method that updates values every 1/60th of a second
    def update(self):
        self.inbounds()
        self.mob_collide()
        self.acc = self.vel * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos

# class for mobs
class Mob(Sprite):
    # parameters for mob class
    def __init__(self, game, player, width, height, color):
        Sprite.__init__(self)
        self.player = player
        self.game = game
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        # randomizes starting position and velocity
        self.rect.center = vec(randint(0, WIDTH), randint(0,HEIGHT))
        self.pos = vec(randint(0,50),randint(0,50))
        self.vel = vec(randint(1,5),randint(1,5))
        self.acc = vec(1,1)
        self.cofric = 0.1
        self.enemyspeed = .2
        
    # keeps mob inbounds adjusting it to its own width that is determined when an instance of the class is created
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

    # method for rudimentary pathing used to track and follow player
    def pathing(self):
        if self.player.pos.x > self.pos.x:
            self.vel.x += self.enemyspeed
        if self.player.pos.x < self.pos.x:
            self.vel.x -= self.enemyspeed
        if self.player.pos.y < self.pos.y:
            self.vel.y -= self.enemyspeed
        if self.player.pos.y > self.pos.y:
            self.vel.y += self.enemyspeed

    # method for determining player collision and then stops the mob from continuing to move
    def player_collide(self):
        hits = pg.sprite.spritecollide(self, self.game.player1, False)
        if hits:
            self.vel.x *= 0
            self.vel.y *= 0
            
    # updates mob class when called
    def update(self):
        self.inbounds()
        self.pathing()
        self.player_collide()
        self.pos += self.vel
        self.rect.center = self.pos

# class for projectiles
class Projectile(Sprite):
    def __init__(self, game, enemies, player):
        # allows me to call methods from the parent class
        super().__init__()

        self.game = game
        self.enemies = enemies
        self.player = player
        self.projectilespeed = 1
        self.pos = vec(50,50)
        self.pos.x = self.player.pos.x
        self.pos.y = self.player.pos.y
        self.vel = vec(randint(1,5),randint(1,5))
        self.acc = vec(1,1)
        self.image = pg.Surface([10, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    # method for rudimentary tracking by changing velocities depending on enemy position
    def tracking(self):
        if self.enemies.pos.x > self.pos.x:
            self.vel.x -= self.projectilespeed
        if self.enemies.pos.x < self.pos.x:
            self.vel.x += self.projectilespeed
        if self.enemies.pos.y < self.pos.y:
            self.vel.y += self.projectilespeed
        if self.enemies.pos.y > self.pos.y:
            self.vel.y -= self.projectilespeed

    # updates sprite when called
    def update(self):
        self.tracking()
        self.pos += self.vel * MOB_FRICTION
        self.rect.center = self.pos