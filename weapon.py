import pygame
from superclass import *

## @class Weapon
#  @brief this is the Weapon super-class, all damage will be dealt by weapons
class Weapon(object):
    ## the constructor
    #  @param damage the amount of health to deduct from the target, optional
    #  @param target the target, optional
    def __init__(self, game, damage = 10, target = None):
        self.damage = damage
        self.game = game

    ## the attack function
    #  @brief attacks the given target
    #  @param target the target we are attacking
    def attack(self, target): 
        self.game.attack_sound.play()
        
        #set target
        self.target = target

        #apply any effects
        self.apply_effects()

        #calculate how much damage will we do
        damage = self.calculate_damage()

        #damage the target
        target.take_damage(damage)

    ## the cacluate_damage function
    #  @brief determines how much damage we should attempt to do to our target
    def calculate_damage(self):
        return self.damage

    ## the apply_effects function
    #  @brief applies any special effects we might have (eg burning)
    def apply_effects(self):
        pass

## @class FireWeapon
#  @brief a great firey weapon
class FireWeapon(Weapon):
    ## the constructor
    #  @param damage the amount of health to deduct from the target, optional
    #  @param target the target, optional
    def __init__(self, game, damage = 10, target = None):
        #initialize inherited attributes
        super(FireWeapon, self).__init__(game, damage, target)

    ## the apply_effects function
    #  @brief the mighty fire weapon burns its foes
    def apply_effects(self):
        #burn target
        self.target.applyBurning()

## @class IceWeapon
#  @brief a great icey weapon
class IceWeapon(Weapon):
    ## the constructor
    #  @param damage the amount of health to deduct from the target, optional
    #  @param target the target, optional
    def __init__(self, game, damage = 10, target = None):
        #initialize inherited attributes
        super(IceWeapon, self).__init__(game, damage, target)

    ## the apply_effects function
    #  @brief the mighty ice weapon chills its foes
    def apply_effects(self):
        #chill target
        self.target.applyChilled()

## @class ElectricWeapon
#  @brief a great electricy weapon
class ElectricWeapon(Weapon):
    ## the constructor
    #  @param damage the amount of health to deduct from the target, optional
    #  @param target the target, optional
    def __init__(self, game, damage = 10, target = None):
        #initialize inherited attributes
        super(ElectricWeapon, self).__init__(game, damage, target)

    ## the apply_effects function
    #  @brief the mighty electric weapon shocks its foes
    def apply_effects(self):
        #shock target
        self.target.applyShocked()
