import pygame as pg 
from config import *
vec = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_obstacles(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y



class Player(pg.sprite.Sprite):
    # The game parameter will give the player a reference to the game
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center 
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
       # self.health = PLAYER_HEALTH
        self.fuel = PLAYER_FUEL
     
 
    def thrust(self):
        if self.fuel <= 0:
            self.vel = vec(0, 0)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed() # This is going to show us what keys are being pressed
        if keys[pg.K_LEFT]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            self.fuel -= 1
   #     if keys[pg.K_DOWN]:
    #        self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > LASER_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Laser(self.game, pos, dir)
                self.vel = vec(-KICKBACK, 0).rotate(-self.rot)
        
    def update(self):
        self.get_keys()
        self.thrust()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        # We use self.x not rect.x because of integer values in a rectangle, and we will then lose some values.
        self.hit_rect.centerx = self.pos.x
        collide_with_obstacles(self, self.game.meteors, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_obstacles(self, self.game.meteors, 'y')
        self.rect.center = self.hit_rect.center
        # Checking collision with screen borders
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_WIDTH:
            self.rect.bottom = SCREEN_WIDTH
    
    def add_fuel(self, amount):
        self.fuel += amount
        if self.fuel > PLAYER_FUEL:
            self.fuel = PLAYER_FUEL

class Meteor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.meteors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.meteor_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y

class Laser(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.lasers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.laser_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos) # This copies the pos vector, otherwise both laser and player use same pos
        # Result is when fire laser button is pressed, both bullet and player moves.
        self.rect.center = pos
        self.vel = dir * LASER_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > LASER_LIFETIME:
            self.kill()

class Barrel(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.barrels
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.barrel_img
        self.rect = self.image.get_rect()
        self.rect.center = pos
