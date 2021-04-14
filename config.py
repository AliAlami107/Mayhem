import pygame as pg
vec = pg.math.Vector2

# define color white
WHITE = (255, 255, 255)


# game settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
FPS = 60
TITLE = 'Mayhem'
FONT = pg.font.match_font('arial')

BG_IMG = 'starBackground.png'
METEOR_IMG = 'meteorBig.png'

# Player properties
PLAYER_HEALTH = 100
PLAYER_SPD = 300
PLAYER_ROT_SPD = 250
PLAYER_IMG = 'player_new.png'
PLAYER_HITBOX = pg.Rect(0, 0, 35, 35)
LASER_OFFSET = vec(60, 5)
PLAYER_FUEL = 500
PLAYER_GRAVITY = 1
PLAYER_SCORE = 0

# Bullet properties
LASER_IMG = 'laserRedShot.png'
LASER_SPD = 500
LASER_LIFETIME = 1100
LASER_RATE = 700
LASER_DMG = 1

# Item properties
FUEL_BARREL = 500
BARREL_IMG = 'barrelRed_side.png'