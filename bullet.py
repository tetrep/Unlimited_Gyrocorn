import pygame
import time
import math
from bullet import *

## @class Bullet
#  @brief this is the Bullet class
class Bullet(object):
    ## the Bullet constructor
    #  @param starting attack values, point to move towards,and starting point
    def __init__(self, game, starting_attack_damage, starting_attack_area_of_effect, starting_speed, attack_point_x = 0, attack_point_y = 0, starting_x = 0, starting_y = 0):
        self.img = game.imgBasicBullet
        self.rect = self.img.get_rect()
        
        #sets the starting position of the turret
        #players place the base of the turret
        self.x = starting_x
        self.rect.x = starting_x
        self.y = starting_y
        self.rect.y = starting_y
        self.dead = False
    
        #attacking statistics
        self.attack_damage = starting_attack_damage
        self.attack_area_of_effect = starting_attack_area_of_effect
        #self.speed = starting_speed
        self.speed = 500.0
        self.attack_damage_type = "BASIC"
        self.attack_direction_x = attack_point_x
        self.attack_direction_y = attack_point_y
        self.distance = math.sqrt(self.attack_direction_x**2 + self.attack_direction_y**2)
        
    ## the Bullet update
    #  @param game the instance of the class Game that this Turret resides in
    def update(self, game):
        """update the bullet(per frame)"""
        self.distance = math.sqrt((self.rect.x - self.attack_direction_x)**2 + (self.rect.y - self.attack_direction_y)**2)
        if self.attack_direction_x != self.rect.x and self.attack_direction_y != self.rect.y:
            x_movement = self.speed * game.deltaT / 1000.0 * (self.rect.x - self.attack_direction_x) / self.distance
            y_movement = self.speed * game.deltaT / 1000.0 * (self.rect.y - self.attack_direction_y) / self.distance
            self.rect.move_ip( -x_movement, -y_movement)
            self.x = self.rect.x
            self.y = self.rect.y
        else:
            #dies if it has reached its initial destination
            self.dead = True
        
        # deal damage to the creeps it collides with
        # after colliding with creeps it dies
        for target in game.creeps:
            if self.rect.colliderect(target.rect):
                target.take_damage(10)
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
            