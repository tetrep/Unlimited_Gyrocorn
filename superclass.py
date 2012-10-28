import pygame

class SuperClass(object):
    def __init__(self, x, y, defense, absorbtion, health, game):
        """Initialize the superclass object"""
        #super(SuperClass, self).__init__()

        #where we are
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 24, 32)

        #where we want to move to next
        self.x_next = x
        self.y_next = y
        
        #stats
        self.defense = defense
        self.absorbtion = absorbtion
        self.health = health
        self.max_health = health
        
        #instance of game we are in
        self.game = game

    def update(self):
        """update method"""
        pass
    def draw(self):
        """draw method"""
        pass

    def take_damage(self, dmg):
        """applies modifiers to damage, then takes it"""
        #DR% = 1 - (100 / x). 
        damageMultiplier = 100 / self.defense
        #Apply defense buffs/debuffs
        #calculate damage:
        dmg -= self.absorbtion / 2.0
        dmg *= damageMultiplier
        dmg -= self.absorbtion / 2.0
        #apply damage
        self.health -= dmg