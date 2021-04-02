#!/usr/bin/env python

#Importing the needed modules/libraries
import pygame

#initizling pygame
pygame.init()
Clock = pygame.time.Clock()
#Defining window size and etc.
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Mayhem')

#Window logo
icon = pygame.image.load('Mayhem\images\Logo.png')
pygame.display.set_icon(icon)

#Colors
BLUE = (50,50,255)

class Spaceship(pygame.sprite.Sprite):
  def __init__(self, pos_x, pos_y, speed):
    super().__init__()
    self.image = pygame.Surface((500,500))
    self.image.fill((23,53,25))
    self.rect = self.image.get_rect()


space = Spaceship(50,50,1)
Group = pygame.spirte.Group()
Group.add(space) 

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
    screen.fill(BLUE)
  pygame.display.update()
  Group.draw(screen)
  Clock.tick(60)
pygame.quit()