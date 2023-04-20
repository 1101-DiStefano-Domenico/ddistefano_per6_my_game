# File created by: Domenico DiStefano
'''
Game Structure:
Goals, Rules, Feedback, Freedom

My goal is:
create projectiles sprite
'''
# import libs
import pygame as pg
import os
# import settings 
from settings import *
from sprites import *
# from pg.sprite import Sprite

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# create game class in order to pass properties to the sprites file
class Game:
    def __init__(self):
        # init game window etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game (●'◡'●)")
        self.clock = pg.time.Clock()
        self.running = True
        self.startgame = False

    # method that adds sprites  
    def new(self):
        # starting a new game and adding sprites to groups
        self.bullet_list = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player1 = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.player1.add(self.player)
        
        # makes range of mobs and adds them to all sprites group
        for i in range(0,10):
            self.mob1 = Mob(self, self.player, 20, 20,GREEN)
            self.all_sprites.add(self.mob1)
            self.enemies.add(self.mob1)
        
        
            
        self.run()

    # method for running the game
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # method for detecting events in game
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                # creates projectile on player location and adds it to all sprites and bullet list
                if event.key == pg.K_SPACE:
                    bullet = Projectile(self, self.mob1, self.player)
                    bullet.rect.x = self.player.pos.x 
                    bullet.rect.y = self.player.pos.y -50
                    self.all_sprites.add(bullet)
                    self.bullet_list.add(bullet)
                if event.key == pg.K_r:
                    self.playing = False
                if event.key == pg.K_p:
                    self.startgame = True
                    self.playing = False
    
    # method that updates the game at 1/60th of a second
    def update(self):
        self.all_sprites.update()
        for bullet in self.bullet_list:
        # See if it hit a block
            self.enemy_hit_list = pg.sprite.spritecollide(bullet, self.enemies, True)
        # For each enemy hit, remove the bullet and add to the score
        # also has parameters for removing bullet if its position exceeds the width or height of the screen
            for block in self.enemy_hit_list:
                self.bullet_list.remove(bullet)
                self.all_sprites.remove(bullet)
                self.player.score += 1
                
                # adds a new enemy after one dies
                self.mob1 = Mob(self, self.player, 20, 20,(0,255,0))
                self.all_sprites.add(self.mob1)
                self.enemies.add(self.mob1)
                self.mob1.enemyspeed += 0.01 
                self.player.hp += 5
            if bullet.pos.y > HEIGHT:
                self.bullet_list.remove(bullet)
                self.all_sprites.remove(bullet)
            if bullet.pos.y < 0:
                self.bullet_list.remove(bullet)
                self.all_sprites.remove(bullet)
            if bullet.pos.x > WIDTH:
                self.bullet_list.remove(bullet)
                self.all_sprites.remove(bullet)
            if bullet.pos.x < 0:
                self.bullet_list.remove(bullet)
                self.all_sprites.remove(bullet)

 
    # method for displaying the game and displaying end screen when player hp = 0
    def draw(self):
        if not self.startgame:
            self.screen.fill(BLACK)
            self.draw_text("ALIEN SWARM", 100, GREEN, WIDTH/2, 250)
            self.draw_text("PRESS P TO PLAY", 40, WHITE, WIDTH/2, 330)
            self.draw_text("WASD to move", 30, WHITE, WIDTH/2, 420)
            self.draw_text("SPACE to shoot", 30, WHITE, WIDTH/2, 450)
            self.draw_text("KILL THE ALIENS TO REGAIN HP", 25, WHITE, WIDTH/2, 480)
        else:
            if self.player.hp > 0:
                self.screen.fill(BLACK)
                self.all_sprites.draw(self.screen)
                self.draw_text("HP: " + str(self.player.hp), 30,WHITE, 1100, HEIGHT/32)
                self.draw_text("ELIMINATIONS: " + str(self.player.score), 30,WHITE, 120, HEIGHT/32)
            else:
                self.screen.fill(BLACK)
                self.draw_text("YOU DIED", 100, RED, WIDTH/2, 250)
                self.draw_text("PLAY AGAIN? (P)", 30, WHITE, WIDTH/2, 400)
                self.draw_text("ELIMINATIONS: " + str(self.player.score), 30, WHITE, WIDTH/2, 350)
                # removes all sprites to stop any updates while not visible
                self.all_sprites.empty()
        
        pg.display.flip()
    
    # method for drawing text
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('Monaco')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    

# instantiate the game class
g = Game()
# starts the game loop
while g.running:
    g.new()
pg.quit()