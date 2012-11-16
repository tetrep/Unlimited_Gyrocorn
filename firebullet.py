import pygame
import time
import random
from bullet import *

class FireBullet(Bullet):
    ## the Bullet update
    #  @param game the instance of the class Game that this Turret resides in
    def update(self, game):
        """update the bullet(per frame)"""
        self.moving = self.moving + game.deltaT
        if self.moving <= 4000:
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
                target.take_damage(self.attack_damage, self.attack_damage_type)
                if random.randint(1, 100) <= 30:
                    target.applyBurning()
                self.dead = True
                