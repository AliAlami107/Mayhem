import pygame
from config import *
vec = pygame.math.Vector2

def collision_hitbox(this, other):
    return this.hitbox.colliderect(other.rect)

def collision_obstacles(sprite, group, direction):
    if direction == 'y':
        contact = pygame.sprite.spritecollide(sprite, group, False, collision_hitbox)
        if contact:
            if contact[0].rect.centery < sprite.hitbox.centery:
                sprite.pos.y = contact[0].rect.bottom + sprite.hitbox.height / 2
            if contact[0].rect.centery > sprite.hitbox.centery:
                sprite.pos.y = contact[0].rect.top - sprite.hitbox.height / 2
            sprite.score -= PLAYER_SCORE
            sprite.hitbox.centery = sprite.pos.y
            sprite.vel.y = 0

    if direction == 'x':
        contact = pygame.sprite.spritecollide(sprite, group, False, collision_hitbox)
        if contact:
            if contact[0].rect.centerx < sprite.hitbox.centerx:
                sprite.pos.x = contact[0].rect.right + sprite.hitbox.width / 2
            if contact[0].rect.centerx > sprite.hitbox.centerx:
                sprite.pos.x = contact[0].rect.left - sprite.hitbox.width / 2
            sprite.score -= PLAYER_SCORE
            sprite.hitbox.centerx = sprite.pos.x
            sprite.vel.x = 0

class Player(pygame.sprite.Sprite):
    # The game parameter will give the player a reference to the game
    def __init__(self, game, x, y, left, right, up, fire, lasers, enemy_lasers):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
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
        self.game = game
        self.score = PLAYER_SCORE
        self.health = PLAYER_HEALTH
        self.fuel = PLAYER_FUEL
 
    def thrust(self):
        if self.fuel <= 0:
            self.vel = vec(0, 0)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed() # This is going to show us what keys are being pressed
        if keys[self.key_left]:
            self.rot_speed = PLAYER_ROTATION_SPEED
        if keys[self.key_right]:
            self.rot_speed = -PLAYER_ROTATION_SPEED
        if keys[self.key_up]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            self.fuel -= 1 # When pressing key_up, the spacship will use fuel 
# Here we will decide the rate of fire and fire key.
        if keys[self.key_fire]:
            current_shot = pygame.time.get_ticks()
            if current_shot - self.prev_shot > LASER_RATE:
                self.prev_shot = current_shot
                direction = vec(1, 0).rotate(-self.rot)
                pos = self.pos + LASER_OFFSET.rotate(-self.rot)
                Laser(self.game, pos, direction)

        
    def update(self):
        self.get_keys()
        self.thrust()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt 
        self.pos.y += PLAYER_GRAVITY
        # We use self.x not rect.x because of integer values in a rectangle, and we will then lose some values.
        self.hitbox.centerx = self.pos.x
        collision_obstacles(self, self.game.meteors, 'x')
        self.hitbox.centery = self.pos.y
        collision_obstacles(self, self.game.meteors, 'y')
        self.rect.center = self.hitbox.center
        self.hitbox.centerx = self.pos.x

        self.hitbox.centerx = self.pos.x
        collision_obstacles(self, self.game.players1, 'x')
        self.hitbox.centery = self.pos.y
        collision_obstacles(self, self.game.players1, 'y')
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



class Meteor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.meteors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.meteor_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y

class Laser(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction):
        self.groups = game.all_sprites, game.lasers1, game.lasers2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.laser_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos) # This copies the pos vector, otherwise both laser and player use same pos
        # Result is when fire laser button is pressed, both bullet and player moves.
        self.rect.center = pos
        self.vel = direction * LASER_SPEED
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > LASER_LIFETIME:
            self.kill()

class Barrel(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.barrels
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.barrel_img
        self.rect = self.image.get_rect()
        self.rect.center = pos
