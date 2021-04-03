#!/usr/bin/env python

#Importing the needed modules/libraries
import pygame
#This will import all the variables from config.py, so that we don't need to write config.SCREEN_WIDTH
from config import *

class Game:
    def __init__(self):
        #Initialize game window, etc.
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.running = True


        

    def new_game(self):
        #Start a new game
        #Even though we only have on obstacle, we have to create a sprite group.
        self.obstacle_group = pygame.sprite.Group()
        self.player = Player()
        self.run()
        

    def run(self):
        #Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        

    def update(self):
        #Game loop - update
        self.player_group.update()

    def events(self):
        #Game loop - events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing == False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pygame.K_RIGHT:
                       self.player.move(dx=1)
                if event.key == pygame.K_UP:
                       self.player.move(dy=-1)
                if event.key == pygame.K_DOWN:
                       self.player.move(dy=1)

    def draw(self):
        #Game loop - draw
        self.screen.blit(background, [0,0])
        self.obstacle_group.draw(self.screen)
        pygame.display.update()
    def show_start_screen(self):
        #Game start screen
        pass

    def show_go_screen(self):
        #Game over
        pass

game = Game()

game.show_start_screen()
while game.running:
    game.new_game()
    game.show_go_screen()


pygame.quit()