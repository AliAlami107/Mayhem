"""
Authors: Ali Alami, Kasper Hansen
This module contains the game loop, events, etc.
This works as a manager for the other modules.   
"""
import pygame 
import random
from os import path
from config import *
from sprites import *

"""
With draw_text() method we can draw the score on screen, and choose its position, size, and font.
"""
# Defining method to draw the score, later call it in draw(). 
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT, size)
    txt_surf = font.render(text, True, WHITE)
    txt_rect = txt_surf.get_rect() 
    txt_rect.midtop = (x, y)
    surf.blit(txt_surf, txt_rect)

"""
Game:

The class Game contains everything needed to start the game up. It contains different methods
that does its own part to create the program. 
- load_data() to load images.
- new_game() creates the sprite groups and instances.
- run(), the game loop.
- update(), updates the sprites.
- events(), if we want to quit.
- draw(), draws everything on the screen and updates it. 
- And a while loop that ends if we quit the game.
"""
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        pygame.key.set_repeat(500, 100) # To be able to hold down on key to move
        self.running = True
        self.clock = pygame.time.Clock()
        self.load_data()

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
        self.barrel = Barrel(self, (random.randrange(0, SCREEN_WIDTH - 50), # random locations for barrels
                                    random.randrange(0, SCREEN_HEIGHT - 50)))
        self.barrel = Barrel(self, (random.randrange(0, SCREEN_WIDTH - 50), 
                                    random.randrange(0, SCREEN_HEIGHT - 50)))
        self.barrel = Barrel(self, (random.randrange(0, SCREEN_WIDTH - 50), 
                                    random.randrange(0, SCREEN_HEIGHT - 50)))
    
  
        self.run()
# Here we load all the images for the sprites
    def load_data(self):
        mayhem_folder = path.dirname(__file__)
        image_folder = path.join(mayhem_folder, 'image')
        self.bg_image = pygame.image.load(path.join(image_folder, BG_IMAGE))
        self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        self.player_image = pygame.image.load(path.join(image_folder, PLAYER_IMAGE)).convert_alpha()
        self.barrel_image = pygame.image.load(path.join(image_folder, BARREL_IMAGE)).convert_alpha()
        self.laser_image = pygame.image.load(path.join(image_folder, LASER_IMAGE)).convert_alpha()
        self.laser_image = pygame.transform.scale(self.laser_image, (30, 30))
        self.meteor_image = pygame.image.load(path.join(image_folder, METEOR_IMAGE)).convert_alpha()


# This is the game loop update
    def update(self):
        # Updates all sprites in this group.
        self.all_sprites.update()   

     # Checking for collision between players and lasers. Deals dmg to players and adds score.
        contact = pygame.sprite.spritecollide(self.player2, self.lasers1, False)
        for contacts in contact:    
            self.player2.health -= LASER_DMG
            self.player1.score += 1

        contact = pygame.sprite.spritecollide(self.player1, self.lasers2, False)
        for contacts in contact:
            self.player1.health -= LASER_DMG
            self.player2.score += 1
      
        # Checking for collision between players
        contact = pygame.sprite.spritecollide(self.player1, self.players2, False)
        for contacts in contact:
            self.player1.score -= 1

        contact = pygame.sprite.spritecollide(self.player2, self.players1, False)
        for contacts in contact:
            self.player2.score -= 1

        # Here score is subtracted if colliding with meteors.
        contact = pygame.sprite.spritecollide(self.player2, self.meteors, False)
        for contacts in contact:
            self.player2.score -= 1

        contact = pygame.sprite.spritecollide(self.player1, self.meteors, False)
        for contacts in contact:
            self.player1.score -= 1

         # When player and barrel has contact, add fuel to player and delete barrel.
        contact = pygame.sprite.spritecollide(self.player1, self.barrels, False)
        for contacts in contact:
            if self.player1.fuel < PLAYER_FUEL:
                contacts.kill()
                self.player1.add_fuel(FUEL_BARREL) 
        contact = pygame.sprite.spritecollide(self.player2, self.barrels, False)
        for contacts in contact:
            if self.player2.fuel < PLAYER_FUEL:
                contacts.kill()
                self.player2.add_fuel(FUEL_BARREL) 

# This will contain the game loop
    def run(self):
        # Want a variable that does everything while the game is playing
        self.play = True
        while self.play:
            # this is to combat lag and fps drop. i.e player speed is the same regardless of fps
            self.dt = self.clock.tick(FPS) / 1000 
            self.events()
            self.draw()
            self.update()

    def draw(self):
        # Sets the background image on the screen
        self.screen.blit(self.bg_image, (0, 0))
        self.all_sprites.draw(self.screen)
        self.meteors.draw(self.screen)
        # Calls the draw_text method to show scores of each player.
        draw_text(self.screen, str(self.player1.score), 18, SCREEN_WIDTH / 10, 10)
        draw_text(self.screen, str(self.player2.score), 18, SCREEN_WIDTH / 1.1, 10)
        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.play:
                    self.play = False
                self.running = False

# Creating instance of the game 
mayhem = Game()
#Loop that runs the game
while mayhem.running:
    # This is going to start the game. 
    mayhem.new_game()
 

# If the loop ends we quit the game
pygame.quit()
