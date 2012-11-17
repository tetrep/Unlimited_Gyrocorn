import pygame
import time
from bullet import *

class PiercingBullet(Bullet):        
    ## the Bullet update
    #  @param game the instance of the class Game that this Turret resides in
    def update(self, game):
        """update the bullet(per frame)"""
        self.moving = self.moving + game.deltaT
        if self.moving <= self.attack_range * 1000.0:
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
                            