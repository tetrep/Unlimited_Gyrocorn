import pygame

class SuperClass(object):
    def __init__(self, x = 0, y = 0, game = None, defense = 100, absorbtion = 100, health = 100, speed = 24):
        """Initialize the superclass object"""
        
        #where we are
        self.rect = pygame.Rect(x, y, 24, 32)

        #get our coordinates from center
        self.x = self.x_next = self.rect.centerx
        self.y = self.y_next = self.rect.centery

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

        #our attack speed in ms
        self.attack_speed = 1000
        #how long we've been waiting to attack, stops increment when >= attack_speed
        self.attack_wait = 0

        #default update functions
        self.update_functions = []
        #"""
        self.update_functions.append((99, self.checkBurning))
        self.update_functions.append((99, self.checkChilled))
        self.update_functions.append((99, self.checkShocked))
        self.update_functions.append((99, self.checkParalyzed))
        #"""
        
    ## the update function
    #  @brief iterates over a list of functions and calls them, in order
    def update(self):
        #call all the functions
        for function_tuple in self.update_functions:
            function_tuple[1]()

    def draw(self):
        """draw method"""
        pass

    def take_damage(self, dmg, dtype = 1):
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
    
    #  @todo increment burning counter by 500 each step, instead of 1
    def checkBurning(self):
        if self.timeBurning != -1:
            self.timeBurning += self.game.deltaT
            if self.timeBurning >= 4000:
                self.timeBurning = -1
                self.burningCounter = 0
            elif self.timeBurning > 500 * self.burningCounter:
                self.burningCounter = self.burningCounter + 1
                self.take_damage(5, 1)

    def applyChilled(self):
        self.timeChilled = 0
        self.speed = self.max_speed * 0.5
        
    def checkChilled(self):
        if self.timeChilled != -1:
            self.timeChilled = self.timeChilled + self.game.deltaT
            if self.timeChilled >= 4000:
                self.timeChilled = -1
                self.speed = self.max_speed       
    
    def applyShocked(self):
        self.timeShocked = 0
        self.damage_multiplier = 2.5
        
    def checkShocked(self):
        if self.timeShocked != -1:
            self.timeShocked = self.timeShocked + self.game.deltaT
            if self.timeShocked >= 4000:
                self.timeShocked = -1
                self.damage_multiplier = 1
    
    def applyParalyzed(self):
        self.timeParalyzed = 0
        self.speed = 0
        
    def checkParalyzed(self):
        if self.timeParalyzed != -1:
            self.timeParalyzed = self.timeParalyzed + self.game.deltaT
            if self.timeParalyzed >= 2000:
                self.timeParalyzed = -1
                self.speed = self.max_speed
