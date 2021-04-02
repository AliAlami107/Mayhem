#!/usr/bin/env python

#Importing the needed modules/libraries
import pygame

#initizling pygame
pygame.init()
Clock = pygame.time.Clock()
#Defining window size and etc.
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Mayhem')
background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
#Colors
BLUE = (50,50,255)

class object(pygame.sprite.Sprite):
    """This class will represent every object. It derives from
    'sprite' class in pygame.
    """
    def init(self):
        super().init()
        self.pos_x = 0
        self.pos_y = 0
        self.image = 0
        self.width = 0
        self.height = 0





running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, [0,0])

    pygame.display.update()
    Clock.tick(60)
