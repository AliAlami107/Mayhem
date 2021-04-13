import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
FPS = 60
TITLE = 'Mayhem'

BG_IMG = 'starBackground.png'
METEOR_IMG = 'meteorBig.png'

# Player properties
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'player_new.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(20, 10)
PLAYER_FUEL = 500
PLAYER_GRAVITY = 0.5


# Bullet properties
LASER_IMG = 'laserRedShot.png'
LASER_SPEED = 500
LASER_LIFETIME = 1000
LASER_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5
LASER_DMG = 10

# Item properties
FUEL_BARREL = 500
BARREL_IMG = 'barrelRed_side.png'