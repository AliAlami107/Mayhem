import pygame 
import sys
import random
from os import path
from config import *
from sprites import *

# Defining method to draw the score, later call it in draw(). 
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT, size)
    txt_surf = font.render(text, True, WHITE)
    txt_rect = txt_surf.get_rect() 
    txt_rect.midtop = (x, y)
    surf.blit(txt_surf, txt_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        pygame.key.set_repeat(500, 100) # To be able to hold down on key to move
        self.running = True
        self.clock = pygame.time.Clock()
        self.load_data()
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.bg_img = pygame.image.load(path.join(img_folder, BG_IMG))
        self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        self.player_img = pygame.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.barrel_img = pygame.image.load(path.join(img_folder, BARREL_IMG)).convert_alpha()
        self.laser_img = pygame.image.load(path.join(img_folder, LASER_IMG)).convert_alpha()
        self.laser_img = pygame.transform.scale(self.laser_img, (30, 30))
        self.meteor_img = pygame.image.load(path.join(img_folder, METEOR_IMG)).convert_alpha()

# This is when the game is over, and we want to start a new game. Here the game is reset. Also the start 
# of game
    def new_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.lasers1 = pygame.sprite.Group()
        self.lasers2 = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.barrels = pygame.sprite.Group()
        self.players1 = pygame.sprite.Group()
        self.players2 = pygame.sprite.Group()
        self.player1 = Player(self, 60, 60, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_SPACE, 
                                self.lasers1, self.lasers2) 
        self.player2 = Player(self, SCREEN_WIDTH - 50, 40, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_g, 
                                self.lasers2, self.lasers1) 
        self.players1.add(self.player1)
        self.players2.add(self.player2)
    

        self.meteor = Meteor(self, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.barrel = Barrel(self, (random.randrange(0, SCREEN_WIDTH - 50), 
                                    random.randrange(0, SCREEN_HEIGHT - 50)))
        self.barrel = Barrel(self, (random.randrange(0, SCREEN_WIDTH - 50), 
                                    random.randrange(0, SCREEN_HEIGHT - 50)))
        self.barrel = Barrel(self, (random.randrange(0, SCREEN_WIDTH - 50), 
                                    random.randrange(0, SCREEN_HEIGHT - 50)))
  
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
        contact = pygame.sprite.spritecollide(self.player1, self.barrels, False)
        for hit in contact:
            if self.player1.fuel < PLAYER_FUEL:
                hit.kill()
                self.player1.add_fuel(FUEL_BARREL) 
        contact = pygame.sprite.spritecollide(self.player2, self.barrels, False)
        for hit in contact:
            if self.player2.fuel < PLAYER_FUEL:
                hit.kill()
                self.player2.add_fuel(FUEL_BARREL) 
     # Checking for collision between players and lasers
        contact = pygame.sprite.spritecollide(self.player2, self.lasers1, False)
        for hit in contact:    
            self.player2.health -= LASER_DMG
            self.player1.score += PLAYER_SCORE

        contact = pygame.sprite.spritecollide(self.player1, self.lasers2, False)
        for hit in contact:
            self.player1.health -= LASER_DMG
            self.player2.score += PLAYER_SCORE
      
        # Checking for collision between players
        contact = pygame.sprite.spritecollide(self.player1, self.players2, False)
        for hit in contact:
            self.player1.score -= PLAYER_SCORE

        contact = pygame.sprite.spritecollide(self.player2, self.players1, False)
        for hit in contact:
            self.player2.score -= PLAYER_SCORE



        

      

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                pass


    def draw(self):
        # This it to see the fps of the game, allows us to find out if game is lagging
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.bg_img, (0, 0))
        self.all_sprites.draw(self.screen)
        self.meteors.draw(self.screen)
        draw_text(self.screen, str(self.player1.score), 18, SCREEN_WIDTH / 10, 10)
        draw_text(self.screen, str(self.player2.score), 18, SCREEN_WIDTH / 1.1, 10)
        pygame.display.update()

# Creating instance of the game 
g = Game()

#Loop that runs the game
while g.running:
    # This is going to start the game. 
    g.new_game()
 

# If the loop ends we quit the game
pygame.quit()
