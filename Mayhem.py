#!/usr/bin/env python

#Importing the needed modules/libraries
import pygame
#This will import all the variables from config.py, so that we don't need to write config.SCREEN_WIDTH
from config import *
#Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

#Images
background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
obstacle_image = pygame.image.load("Asteroid2.png")
player_image = pygame.image.load("spaceShip.png")
#Colors
BLUE = (50,50,255)

"""
We don't need to create a parent class with 'class parent(Sprite)'. Instead, 
all of our objects will directly inherit from pygame.sprite.Sprite.
So player(pygame.sprite.Sprite)
"""
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):  
        super().__init__()
        self.image = obstacle_image #Getting the image we assigned above
        #The image needs a rectangle that surrounds it and so we can manipulate it.
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
    
    #Method to move the player
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

#Even though we only have on obstacle, we have to create a sprite group.
obstacle_group = pygame.sprite.Group()
obstacle = Obstacle()
obstacle_group.add(obstacle)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.move(dx=-1)
            if event.key == pygame.K_RIGHT:
                   self.player.move(dx=1)
            if event.key == pygame.K_UP:
                   self.player.move(dy=-1)
            if event.key == pygame.K_DOWN:
                   self.player.move(dy=1)
    

    screen.blit(background, [0,0])
    obstacle_group.draw(screen)
    pygame.display.update()
    Clock.tick(60)
