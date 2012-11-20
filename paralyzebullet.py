import pygame
import time
from bullet import *

class ParalyzeBullet(Bullet):
    ## the ParalyzeBullet update
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
        
        # deal damage to the creeps it collides with
        # after colliding with creeps it dies
        for target in game.creeps:
            if self.rect.colliderect(target.rect):
                if self.attack_area_of_effect == 0:
                    target.applyParalyzed()
                else:
                    for creep in game.creeps:
                        creep_distance = math.sqrt( (target.x - creep.x)**2 + (target.y - creep.y)**2 )
                        if creep_distance < self.attack_area_of_effect:
                            creep.applyParalyzed()
                self.dead = True
                