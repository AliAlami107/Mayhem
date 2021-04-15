"""
Authors: Ali Alami, Kasper Hansen
This module contains all sprite classes. 
"""

import pygame
from config import *
vector = pygame.math.Vector2

"""
Metero():
Class for the meteor obstacle. 
"""

class Meteor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.meteors # Added to all_sprite & meteors groups.
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.meteor_image
        self.game = game
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x 
        self.rect.y = y

"""
collision_obstacles:
Before the player class, we have made a couple of methods do deal with collision with obstacle.
Calls the collision_hitbox method inside the spritecollide(). 
Checks the position of hitbox center in both y and x direction.
Also adds values to score and changes velocity on collision.
"""

def collision_obstacles(sprite, group, direction):
    # Checking collisin for both y and x direction with obstacles. 
    if direction == 'y':
        contact = pygame.sprite.spritecollide(sprite, group, False, collision_hitbox) # Using function in 
        if contact:                                                                   # spritecollide
            if contact[0].rect.centery < sprite.hitbox.centery:
                sprite.pos.y = contact[0].rect.bottom + sprite.hitbox.height // 2 # The center of hitbox
            if contact[0].rect.centery > sprite.hitbox.centery:
                sprite.pos.y = contact[0].rect.top - sprite.hitbox.height // 2
            # Player score is decreased when crashing.
            sprite.hitbox.centery = sprite.pos.y
            sprite.score -= PLAYER_SCORE
            # When conact with obstacle, set the velocity to 0. 
            sprite.vel.y = 0

    if direction == 'x':
        contact = pygame.sprite.spritecollide(sprite, group, False, collision_hitbox)
        if contact:
            if contact[0].rect.centerx < sprite.hitbox.centerx:
                sprite.pos.x = contact[0].rect.right + sprite.hitbox.width // 2
            if contact[0].rect.centerx > sprite.hitbox.centerx:
                sprite.pos.x = contact[0].rect.left - sprite.hitbox.width // 2
            sprite.hitbox.centerx = sprite.pos.x
            sprite.score -= PLAYER_SCORE
            sprite.vel.x = 0

# Collision between sprite and object rectangles.
def collision_hitbox(this, other):
    return this.hitbox.colliderect(other.rect)

"""
Laser():
Here is the class for the lasers the player shoots. 
Has a update() method to limit how many lasers that can be shot in a given time.
Is added to both lasers groups.
"""
class Laser(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction):
        self.groups = game.all_sprites, game.lasers1, game.lasers2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.laser_image
        self.rect = self.image.get_rect()
        self.pos = vector(pos) # This copies the pos vectortor, otherwise both laser and player use same pos
        # Result is when fire laser button is pressed, both bullet and player moves.
        self.rect.center = pos
        self.vel = direction * LASER_SPEED
        self.create_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.create_time > LASER_LIFETIME: # This code decides range of laser
            self.kill()

"""
Player():
A player class that has parameters for its position, key bindings, etc.
We add it to the all_sprites group for it to be drawn.
We have different methods that help make the player object do what we want.
- thrust(), simple method that tells us if fuel is empty, set velocity to 0.
- get_keys(), this makes the player sprite move, shoot and rotate with custom key buttons.
- check_collision(), calls collision_obstacle function to work with meteors and other player.
- update(), updates player image, rotation, adds gravity, health, other methods and boundary collision.
- add_fuel(), make it possible to add fuel when picking up fuel. 

"""
class Player(pygame.sprite.Sprite):
    # The game parameter will give the player a reference to the game. The controls parameters
    # allows us to choose what keys control the player. 
    def __init__(self, game, x, y, left, right, up, fire, lasers, enemy_lasers):
        # Here the player class is added to the all_sprites group, to later draw and update in primary module.
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.hitbox = PLAYER_HITBOX   # Sets a hitbox arount player, is fixed regardless rotation angle.
        self.hitbox.center = self.rect.center 
        self.vel = vector(0, 0)
        self.pos = vector(x, y)
        self.key_left = left 
        self.key_right = right 
        self.key_up = up 
        self.key_fire = fire 
        self.rotation = 0
        self.prev_shot = 0
        self.game, self.score = game, PLAYER_SCORE  # reference to game
        self.fuel, self.health = PLAYER_FUEL, PLAYER_HEALTH
 
    def thrust(self):
        # fuel = empty, no more velocity.
        if self.fuel <= 0:
            self.vel = vector(0, 0)
                
    def check_collision(self):
        # Using the collision_obstacles method for both meteros group and player1 group. 
        
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
        
    def update(self):
        self.get_keys()
        self.thrust()
        # In the update() section we take the self.rotation variable and assign it the value of 
        # it's own rotation added to the rotation speed multiplied to game.dt. Also using modulus % 360 to 
        # prevent the angle from getting bigger and bigger each rotation.  
        self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.player_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt 
        self.pos.y += PLAYER_GRAVITY
        self.check_collision()  
        if self.health <= 0:
            self.kill()
        
        
        # Checking collision with screen borders, adding and subtracting player hitbox width/height
        if self.pos.x >= SCREEN_WIDTH - 30:
            self.pos.x = SCREEN_WIDTH - 30
            self.score -= 1
        if self.pos.x <= 0 + 30:
            self.pos.x = 0 + 30
            self.score -= 1 
        if self.pos.y<= 0 + 30:
            self.pos.y = 0 + 30
            self.score -= 1 
        if self.pos.y >= SCREEN_HEIGHT - 30:
            self.pos.y = SCREEN_HEIGHT - 30 
            self.score -= 1 
# For the rot_right and rotate left buttons, we simply just give the rotation speed the value of 
# PLAYER_ROTATION_SPEED. For the thrust button, we use a vectortor which is easier than trigonometry.
# So we take the vectortor(PLAYER_SPEED, 0) and rotate it by what our rotation is (-self.rotation).
# We are using negative (-self.rotation) because we're rotating the vectortor in the opposite direction of
# the directon the player sprite is pointing so that it can match the rotation of our keys.  

    def get_keys(self):
        self.vel = vector(0, 0)
        self.rotation_speed = 0
        keys = pygame.key.get_pressed() # This is going to show us what keys are being pressed
        if keys[self.key_left]:
            self.rotation_speed = PLAYER_ROTATION_SPEED
        if keys[self.key_right]:
            self.rotation_speed = -PLAYER_ROTATION_SPEED
        if keys[self.key_up]:
            self.vel = vector(PLAYER_SPEED, 0).rotate(-self.rotation)
            self.fuel -= 1 # When pressing key_up, the spacship will use fuel 

# Here we will decide the rate of fire and fire key.
#'current_shot' is a timestamp of the current time 
# self.prev_shot' is a variable that stores what time it was when the last bullet was fired.
# When the player is first created, 'self.prev_shot' is assigned the value of 0, because a laser has
# yet to be fired.
#  When a new laser is fired, 'self.prev_shot' is reassigned the value of the current time ('current_shot'), 
# so that we can loop back to number 4 above in order to decide when to fire the next laser.
        if keys[self.key_fire]:
            current_shot = pygame.time.get_ticks()
            if current_shot - self.prev_shot > LASER_RATE:
                self.prev_shot = current_shot
                pos = self.pos + LASER_OFFSET.rotate(-self.rotation)
                direction = vector(1, 0).rotate(-self.rotation)
                Laser(self.game, pos, direction)
    
    def add_fuel(self, amount):
        self.fuel += amount
        if self.fuel > PLAYER_FUEL:
            self.fuel = PLAYER_FUEL


"""
Barrel():
This is the class for the fuel barrel item. Very simple image with rectangle around it.
Added to barrels group and all_sprites. 
"""
class Barrel(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.barrels
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.barrel_image
        self.rect = self.image.get_rect()
        self.rect.center = pos
