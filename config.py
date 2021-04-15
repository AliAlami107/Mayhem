"""
Authors: Ali Alami, Kasper Hansen
This module contains all constant variables. 
Have tried to separate each object and its properties.
"""
import pygame
vec = pygame.math.Vector2

# define color white
WHITE = (255, 255, 255)


# game settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
FPS = 60
TITLE = 'Mayhem'
FONT = pygame.font.match_font('arial')

BG_IMG = 'starBackground.png'
METEOR_IMG = 'meteorBig.png'

# Player properties
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROTATION_SPEED = 250
PLAYER_IMG = 'player_new.png'
PLAYER_HITBOX = pygame.Rect(0, 0, 30, 30)
LASER_OFFSET = vec(60, 5)
PLAYER_FUEL = 700
PLAYER_GRAVITY = 1
PLAYER_SCORE = 0

# Laser properties
LASER_IMG = 'laserRedShot.png'
LASER_SPEED = 500
LASER_LIFETIME = 1100
LASER_RATE = 700
LASER_DMG = 1

# Item properties
FUEL_BARREL = 700
BARREL_IMG = 'barrelRed_side.png'