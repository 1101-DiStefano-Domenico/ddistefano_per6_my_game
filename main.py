# File created by: Domenico DiStefano
'''
Game Structure:
Goals, Rules, Feedback, Freedom

My goal is:
create projectiles sprite

Reach Goal:

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

    # method that adds sprites  
    def new(self):
        # starting a new game
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player1 = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.player1.add(self.player)
        
        self.bullet_list = pg.sprite.Group()

        # self.projectile = Projectile(self)
        # self.all_sprites.add(self.projectile)
        
        for i in range(0,5):
            self.mob1 = Mob(self, self.player, 20, 20,(0,255,0))
            self.all_sprites.add(self.mob1)
            self.enemies.add(self.mob1)
            
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bullet = Projectile(self, self.enemies)
                    bullet.rect.x = self.player.pos.x 
                    bullet.rect.y = self.player.pos.y -50
                    self.all_sprites.add(bullet)
                    self.bullet_list.add(bullet)
                    print("click")
    
    def update(self):
        self.all_sprites.update()
        
    def draw(self):
        if self.player.hp >= 0:
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            self.draw_text("HP: " + str(self.player.hp), 30,WHITE, 720, HEIGHT/32)
        else:
            self.screen.fill(BLACK)
            self.draw_text("YOU LOSE", 80, WHITE, WIDTH/2, 250)
            self.draw_text("PLAY AGAIN? (R)", 30, WHITE, WIDTH/2, 350)
        pg.display.flip()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)
    

# instantiate the game class...
g = Game()
# kick off the game loop
while g.running:
    g.new()
pg.quit()