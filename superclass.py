import pygame

class SuperClass(object):
    def __init__(self, x, y, game, defense = 100, absorbtion = 100, health = 100, speed = 100):
        """Initialize the superclass object"""
        
        #where we are
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 24, 32)

        #where we want to move to next
        self.x_next = x
        self.y_next = y
        
        #stats
        self.defense = defense
        self.max_defense = defense
        self.absorbtion = absorbtion
        self.max_aborbtion = absorbtion
        self.health = health
        self.max_health = health
        self.speed = speed
        self.max_speed = speed
        
        #instance of game we are in
        self.game = game

        self.timeBurning = -1
        self.timeChilled = -1
        self.timeShocked = -1
        self.timeParalyzed = -1
        self.burningCounter = 0
        self.damage_multiplier = 1
        
    def update(self, game):
        """update method"""
        checkBurning(game.deltaT)
        checkChilled(game.deltaT)
        checkShocked(game.deltaT)
        checkParalyzed(game.deltaT)
        
    def draw(self):
        """draw method"""
        pass

    def take_damage(self, dmg, type):
        """applies modifiers to damage, then takes it"""
        #DR% = 1 - (100 / x). 
        damageMultiplier = 100.0 / float(self.defense)
        #Apply defense buffs/debuffs
        #calculate damage:
        dmg -= self.absorbtion / 2.0
        dmg *= damageMultiplier * self.damage_multiplier
        dmg -= self.absorbtion / 2.0
        #apply damage
        self.health -= dmg
        
    def applyBurning(self):
        self.timeBurning = 0
    
    def checkBurning(self, deltaT):
        if self.timeBurning != -1:
            self.timeBurning = self.timeBurning + deltaT
            if self.timeBurning >= 4000:
                self.timeBurning = -1
                self.burningCounter = 0
            elif self.timeBurning > 500 * self.burningCounter:
                self.burningCounter = self.burningCounter + 1
                self.take_damage(5, 1)
    
    def applyChilled(self):
        self.timeChilled = 0
        self.speed = self.max_speed * 0.5
        
    def checkChilled(self, deltaT):
        if self.timeChilled != -1:
            self.timeChilled = self.timeChilled + deltaT
            if self.timeChilled >= 4000:
                self.timeChilled = -1
                self.speed = self.max_speed       
    
    def applyShocked(self):
        self.timeShocked = 0
        self.damage_multiplier = 2.5
        
    def checkShocked(self, deltaT):
        if self.timeShocked != -1:
            self.timeShocked = self.timeShocked + deltaT
            if self.timeShocked >= 4000:
                self.timeShocked = -1
                self.damage_multiplier = 1
    
    def applyParalyzed(self):
        self.timeParalyzed = 0
        self.speed = 0
        
    def checkParalyzed(self, deltaT):
        if self.timeParalyzed != -1:
            self.timeParalyzed = self.timeParalyzed + deltaT
            if self.timeParalyzed >= 2000:
                self.timeParalyzed = -1
                self.speed = self.max_speed
            
    
    
    
    
    
    
    
    
    
    
    
    
    
