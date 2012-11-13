import pygame

## @class Weapon
#  @brief this is the Weapon super-class, all damage will be dealt by weapons
#  @todo add more weapons
class Weapon(object):
    ## the constructor
    #  @param owner the owner of the weapon
    def __init__(self, owner):
        self.damage = 10;
        self.owner = owner

    ## the attack function
    #  @brief attacks the given target
    #  @param target the target we are attacking
    def attack(self, target): 
        damage = self.calculate_damage(target)
        target.take_damage(damage)

    ## the cacluate_damage function
    #  @brief determines how much damage we should attempt to do to the given target
    #  @param target the target we are trying to damage
    #  @todo be practical
    def calculate_damage(self, target):
        damage_mod = 1

        #just an example for 10x damage
        if target.x >= target.y:
            damage_mod = 10

        #calculate how much damage to do
        return self.damage * damage_mod

