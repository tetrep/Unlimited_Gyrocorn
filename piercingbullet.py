import pygame
import time
from bullet import *

class PiercingBullet(Bullet):        
    ## the PiercingBullet update
    #  @param game the instance of the class Game that this Turret resides in
    def update(self, game):
        """update the bullet(per frame)"""
        self.moving = self.moving + game.deltaT
            
        if self.moving <= self.attack_range * 1000.0:
            #calculate our next x/y coords
            self.x_real += -(self.x_movement * game.deltaT / 1000.0)
            self.y_real += -(self.y_movement * game.deltaT / 1000.0)

            #update our rect
            self.rect.move_ip(int(self.x_real) - self.x, int(self.y_real) - self.y)

            #update our x/y positon
            self.x = int(self.x_real)
            self.y = int(self.y_real)
        else:
            #dies if it has reached its initial destination
            self.dead = True
        
        if self.hit_delay > 0.5:
            self.hit_delay = -1
        elif self.hit_delay != -1:
            self.hit_delay = self.hit_delay + game.deltaT / 1000.0
            return

            
        # deal damage to the creeps it collides with
        for target in game.creeps:
            if self.rect.colliderect(target.rect):
                if self.attack_area_of_effect == 0:
                    self.hit_delay = 0
                    target.take_damage(self.attack_damage, self.attack_damage_type)
                else:
                    for creep in game.creeps:
                        creep_distance = math.sqrt( (target.x - creep.x)**2 + (target.y - creep.y)**2 )
                        if creep_distance < self.attack_area_of_effect:
                            self.hit_delay = 0
                            creep.take_damage(self.attack_damage, self.attack_damage_type)
                            