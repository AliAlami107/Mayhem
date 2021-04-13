import pygame as pg 
import sys
from os import path
from config import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        pg.key.set_repeat(500, 100) # To be able to hold down on key to move
        self.running = True
        self.clock = pg.time.Clock()
        self.load_data()
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
       # self.bg = Map(path.join(game_folder, 'starBackground.png'))
        self.bg_img = pg.image.load(path.join(img_folder, BG_IMG))
        self.bg_img = pg.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.barrel_img = pg.image.load(path.join(img_folder, BARREL_IMG)).convert_alpha()
        self.laser_img = pg.image.load(path.join(img_folder, LASER_IMG)).convert_alpha()
        self.laser_img = pg.transform.scale(self.laser_img, (30, 30))
        self.meteor_img = pg.image.load(path.join(img_folder, METEOR_IMG)).convert_alpha()

# This is when the game is over, and we want to start a new game. Here the game is reset. Also the start 
# of game
    def new_game(self):
        self.all_sprites = pg.sprite.Group()
        self.lasers = pg.sprite.Group()
        self.meteors = pg.sprite.Group()
        self.barrels = pg.sprite.Group()
        self.player = Player(self, 40, 40)    
        self.meteor = Meteor(self, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.barrel = Barrel(self, (SCREEN_WIDTH / 2 + 50, 160 ))
        # self.meteors.add(self.meteor)    
        self.run()

# This will contain the game loop
    def run(self):
        # Want a variable that does everything while the game is playing
        self.playing = True
        while self.playing:
            # this is to combat lag and fps drop. i.e player speed is the same regardless of fps
            self.dt = self.clock.tick(FPS) / 1000 
            self.events()
            self.update()
            self.draw()

# This is the game loop update
    def update(self):
        self.all_sprites.update()   
        hits = pg.sprite.spritecollide(self.player, self.barrels, False)
        for hit in hits:
            if self.player.fuel < PLAYER_FUEL:
                hit.kill()
                self.player.add_fuel(FUEL_BARREL) 

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                pass

    def draw(self):
        # This it to see the fps of the game, allows us to find out if game is lagging
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.bg_img, (0, 0))
        self.all_sprites.draw(self.screen)
        self.meteors.draw(self.screen)
        pg.display.update()

# Creating instance of the game
g = Game()

#Loop that runs the game
while g.running:
    # This is going to start the game. 
    g.new_game()
 

# If the loop ends we quit the game
pg.quit()
