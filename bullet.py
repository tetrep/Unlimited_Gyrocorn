import pygame
import time
import math
from bullet import *

## @class Bullet
#  @brief this is the Bullet class
class Bullet(object):
    ## the Bullet constructor
    #  @param starting attack values, point to move towards,and starting point
    def __init__(self, game, img, sound, starting_area_of_effect, starting_attack_damage, starting_attack_range, starting_attack_damage_type, target, starting_x = 0, starting_y = 0):
        self.img = img
        self.rect = self.img.get_rect()
        
        #sets the starting position of the turret
        #players place the base of the turret
        self.x = starting_x
        self.rect.x = starting_x
        self.y = starting_y
        self.rect.y = starting_y
        self.dead = False
    
        #attacking statistics
        self.speed = 400
        self.attack_damage = starting_attack_damage
        self.attack_range = starting_attack_range
        self.attack_area_of_effect = starting_area_of_effect
        self.attack_damage_type = starting_attack_damage_type
        self.attack_direction_x = target.rect.x
        self.attack_direction_y = target.rect.y
        self.moving = 0

        
        self.distance = math.sqrt((self.rect.x - self.attack_direction_x)**2 + (self.rect.y - self.attack_direction_y)**2)
        self.x_movement = self.speed * (self.rect.x - self.attack_direction_x ) / self.distance
        self.y_movement = self.speed * (self.rect.y - self.attack_direction_y) / self.distance
        self.distance = math.sqrt(self.attack_direction_x**2 + self.attack_direction_y**2)
        
        sound.play()
        
    ## the Bullet update
    #  @param game the instance of the class Game that this Turret resides in
    def update(self, game):
        """update the bullet(per frame)"""
        #self.distance = math.sqrt((self.rect.x - self.attack_direction_x)**2 + (self.rect.y - self.attack_direction_y)**2)
        #if self.attack_direction_x != self.rect.x and self.attack_direction_y != self.rect.y:
        self.moving = self.moving + game.deltaT
        if self.moving <= self.attack_range * 1000.0:
            #x_movement = self.speed * game.deltaT / 1000.0 * (self.rect.x - self.attack_direction_x) / self.distance
            #y_movement = self.speed * game.deltaT / 1000.0 * (self.rect.y - self.attack_direction_y) / self.distance
            self.rect.move_ip( - (self.x_movement * game.deltaT / 1000.0), -(self.y_movement * game.deltaT / 1000.0))
            self.x = self.rect.x
            self.y = self.rect.y
        else:
            #dies if it has reached its initial destination
            self.dead = True
        
        # deal damage to the creeps it collides with
        # after colliding with creeps it dies
        for target in game.creeps:
            if self.rect.colliderect(target.rect):
                if self.attack_area_of_effect == 0:
                    target.take_damage(self.attack_damage, self.attack_damage_type)
                else:
                    for creep in game.creeps:
                        creep_distance = math.sqrt( (target.x - creep.x)**2 + (target.y - creep.y)**2 )
                        if creep_distance < self.attack_area_of_effect:
                            creep.take_damage(self.attack_damage, self.attack_damage_type)
                self.dead = True
               
    
    ## the Bullet draw
    # @param g a reference to the Game that is currently running
    def draw(self, g):
        """draw the bullet to the screen"""
        #declare a temporary surface to apply transformations to
        temp = pygame.Surface( (self.rect.width, self.rect.height) ).convert()
        #set up transparency
        temp.fill( (255, 255, 0) )
        temp.set_colorkey( (255, 255, 0) )
        #draw img to temp
        temp.blit(self.img, pygame.Rect(0, 0, self.rect.width, self.rect.height) )
        #calculate offset
        offset = [-1 *( g.focus[0] - g.view[0] / 2 ), -1 * ( g.focus[1] - g.view[1] / 2 ) ]
        #zoom logic
        temp = pygame.transform.scale(temp, ( (int)(self.rect.width * g.zoom), (int)(self.rect.height * g.zoom) ))
        #draw to the game screen
        g.screen.blit( temp, pygame.Rect( (int)(self.x * g.zoom) + offset[0], (int)(self.y * g.zoom) + offset[1], \
            (int)(self.rect.width * g.zoom), (int)(self.rect.height * g.zoom) ) )
            