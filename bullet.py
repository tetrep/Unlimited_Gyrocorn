import pygame
import time
import math
from bullet import *


class Bullet(object):
    def __init__(self, game, starting_attack_damage, starting_attack_area_of_effect, starting_speed, attack_point_x = 0, attack_point_y = 0, starting_x = 0, starting_y = 0):
        self.img = game.imgBasicBullet
        self.rect = self.img.get_rect()
        
        #sets the starting position of the turret
        #players place the base of the turret
        self.x = starting_x
        self.rect.x = starting_x
        self.y = starting_y
        self.rect.y = starting_y
        
    
        #attacking statistics
        self.attack_damage = starting_attack_damage
        self.attack_area_of_effect = starting_attack_area_of_effect
        self.speed = starting_speed
        self.attack_damage_type = "BASIC"
        self.attack_direction_x = starting_x - attack_point_x
        self.attack_direction_y = starting_y - attack_point_y
        self.distance = math.sqrt(self.attack_direction_x**2 + self.attack_direction_y**2)
    
    ## the Bullet update
    #  @param game the instance of the class Game that this Turret resides in
    def update(self, game):
        """update the bullet(per frame)"""
        self.x += self.speed * game.deltaT / 1000.0 * self.attack_direction_x / self.distance * -1
        self.y += self.speed * game.deltaT / 1000.0 * self.attack_direction_y / self.distance * -1
        self.rect.move_ip( (int)(self.x - self.rect.x), (int)(self.y - self.rect.y) )
    
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
            