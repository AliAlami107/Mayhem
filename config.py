"""
Authors: Ali Alami, Kasper Hansen
This module contains all constant variables. 
Have tried to separate each object and its properties.
"""
import pygame
vector = pygame.math.Vector2

# define color white
WHITE = (255, 255, 255)


# Player properties
PLAYER_SPEED = 300
PLAYER_ROTATION_SPEED = 250
PLAYER_HEALTH = 100
PLAYER_HITBOX = pygame.Rect(0, 0, 30, 30)
PLAYER_IMAGE = 'player_new.png'
PLAYER_FUEL = 700
PLAYER_SCORE = 0
PLAYER_GRAVITY = 1



# Game properties
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
FONT = pygame.font.match_font('arial')
FPS = 80

BG_IMAGE = 'starBackground.png'
TITLE = 'Mayhem'
METEOR_IMAGE = 'meteorBig.png'


# Laser properties
LASER_SPEED = 500
LASER_IMAGE = 'laserRedShot.png'
LASER_LIFETIME = 1100
LASER_DMG = 1
LASER_OFFSET = vector(60, 5)
LASER_RATE = 700

# Item properties
BARREL_IMAGE = 'barrelRed_side.png'
FUEL_BARREL = 700