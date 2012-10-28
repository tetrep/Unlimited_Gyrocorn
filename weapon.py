import pygame

## @class Weapon
#  @brief this is the Weapon super-class, all damage will be dealt by weapons
#  @todo add more weapons
class Weapon(object):
    ## the constructor
    #  @param owner the owner of the weapon
    #  @param game the instance of the game this Weapon is in
    def __init__(self, owner, game):
        self.damage = 10;
        self.targets = []
        self.owner = owner
        self.game = game

    def attack(self): 
        for target in targets:
            target.take_damage(10)


    def find_targets
