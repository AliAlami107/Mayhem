import pygame as pg 
from config import *
vec = pg.math.Vector2

def collide_hitbox(one, two):
    return one.hitbox.colliderect(two.rect)

def collide_with_obstacles(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hitbox)
        if hits:
            if hits[0].rect.centerx > sprite.hitbox.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hitbox.width / 2
            if hits[0].rect.centerx < sprite.hitbox.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hitbox.width / 2
            sprite.vel.x = 0
            sprite.hitbox.centerx = sprite.pos.x
            sprite.score -= PLAYER_SCORE
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hitbox)
        if hits:
            if hits[0].rect.centery > sprite.hitbox.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hitbox.height / 2
            if hits[0].rect.centery < sprite.hitbox.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hitbox.height / 2
            sprite.vel.y = 0
            sprite.hitbox.centery = sprite.pos.y
            sprite.score -= PLAYER_SCORE


class Player(pg.sprite.Sprite):
    # The game parameter will give the player a reference to the game
    def __init__(self, game, x, y, left, right, up, fire, lasers, enemy_lasers):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hitbox = PLAYER_HITBOX
        self.hitbox.center = self.rect.center 
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.key_left = left 
        self.key_right = right 
        self.key_up = up 
        self.key_fire = fire 
        self.rot = 0
        self.prev_shot = 0
        self.health = PLAYER_HEALTH
        self.fuel = PLAYER_FUEL
        self.score = PLAYER_SCORE
 
    def thrust(self):
        if self.fuel <= 0:
            self.vel = vec(0, 0)

    def get_keys(self):
        self.rot_spd = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed() # This is going to show us what keys are being pressed
        if keys[self.key_left]:
            self.rot_spd = PLAYER_ROT_SPD
        if keys[self.key_right]:
            self.rot_spd = -PLAYER_ROT_SPD
        if keys[self.key_up]:
            self.vel = vec(PLAYER_SPD, 0).rotate(-self.rot)
            self.fuel -= 1 # When pressing key_up, the spacship will use fuel 
# Here we will decide the rate of fire and fire key.
        if keys[self.key_fire]:
            current_shot = pg.time.get_ticks()
            if current_shot - self.prev_shot > LASER_RATE:
                self.prev_shot = current_shot
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + LASER_OFFSET.rotate(-self.rot)
                Laser(self.game, pos, dir)

        
    def update(self):
        self.get_keys()
        self.thrust()
        self.rot = (self.rot + self.rot_spd * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt 
        self.pos.y += PLAYER_GRAVITY
        # We use self.x not rect.x because of integer values in a rectangle, and we will then lose some values.
        self.hitbox.centerx = self.pos.x
        collide_with_obstacles(self, self.game.meteors, 'x')
        self.hitbox.centery = self.pos.y
        collide_with_obstacles(self, self.game.meteors, 'y')
        self.rect.center = self.hitbox.center
        self.hitbox.centerx = self.pos.x
    
        # Checking collision with screen borders
        if self.pos.x >= SCREEN_WIDTH - 35:
            self.pos.x = SCREEN_WIDTH - 35
            self.score -= PLAYER_SCORE
        if self.pos.x <= 0 + 35:
            self.pos.x = 0 + 35
            self.score -= PLAYER_SCORE 
        if self.pos.y<= 0 + 35:
            self.pos.y = 0 + 35
            self.score -= PLAYER_SCORE 
        if self.pos.y >= SCREEN_HEIGHT - 35:
            self.pos.y = SCREEN_HEIGHT - 35 
            self.score -= PLAYER_SCORE 
        if self.health <= 0:
            self.kill()

        
    
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
        self.groups = game.all_sprites, game.lasers1, game.lasers2
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.laser_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos) # This copies the pos vector, otherwise both laser and player use same pos
        # Result is when fire laser button is pressed, both bullet and player moves.
        self.rect.center = pos
        self.vel = dir * LASER_SPD
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
