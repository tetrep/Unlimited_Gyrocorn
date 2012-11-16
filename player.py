import pygame
from mod_enum import *
from equipment import *

class Player(object):
    #  @param img a reference to a pygame.Surface containing the spritesheet to be used for draw calls.
    def __init__(self, img):
        """initialize player"""
        self.img = img
        
        self.x = 0 #position in pixels
        self.y = 0 #position in pixels
        self.rect = pygame.Rect(self.x, self.y, 24, 32) #collision box
        self.speed = 64.0 #speed in pixels/sec
        self.direction = [0, 0] #-1, 0, or 1 x multiplier for orientation of motion along x and y axes
        self.collision = [False, False] #whether the x or y axes of motion are obstructed

        #mechanical variables
        self.exp = 0
        self.gold = 0
        self.hp = [100.0, 100]  #hp [current, max]
        self.baseAttack = 0     #base attack
        self.baseDefense = 100  #base defense
        
        self.attack = 0         #total attack (cap: 10,000)
        self.defense = 0        #total defense (cap: 10,000)
        self.absorbtion = 0     #damage absorbtion: applied 50% before and 50% after defense
        self.regen = 0.00       #life regen (HP / sec)
        self.lifeLeech = 0.00   #% damage stolen as life per hit
        self.crit = 0.00        #% chance of scoring a critical hit
        self.attackSpeedMultiplier = 1.0
        self.moveSpeedMultiplier = 1.0
        

        self.buffs = []
        self.equipment = [Equipment(), Equipment(), Equipment(), Equipment()]

        #animation variables
        self.frame = 0          #current frame in animation
        self.frameMax = 7       #number of frames in animation
        self.frameDirection = 0 #parsed player facing
        self.frameTimer = 0     #ms spent in current frame
        self.frameDelay = 100   #time between frames in ms

    # path generation to dest.
    #rules: adjacent motion allowed if non-blocking
    #diagonal motion allowed if both cardinal directions are unblocking:
    # 000    000    000
    # 0X0 => 1X0 => 1X0
    # 000    000    010
    #should do this recursively? (careful for infinite looping) PF generation?
    
    # in update, follow path.

    def update_stats(self):
        """updates stats used for calculations based on equipment"""
        modEnum = Mod_Enum()
        self.attack = self.baseAttack + self.get_stat(modEnum.MOD_ATTACK)
        self.defense = self.baseDefense + self.get_stat(modEnum.MOD_DEFENSE)
        self.hp[1] = 100 * self.get_stat(modEnum.MOD_HP)
        self.absorbtion = self.get_stat(modEnum.MOD_ABSORB)
        self.regen = 0.00 + self.get_stat(modEnum.MOD_REGEN)
        self.lifeLeech = 0.00 + self.get_stat(modEnum.MOD_REGEN)
        self.crit = 0.00 + self.get_stat(modEnum.MOD_CRIT)
        self.attackSpeedMultiplier = 1.0 + self.get_stat(modEnum.MOD_ATTACK_SPEED)
        self.moveSpeedMultiplier = 1.0 + self.get_stat(modEnum.MOD_MOVE_SPEEED)


    # @ param code the mod code of the stat
    def get_stat(self, code):
        """returns the total amount of the stat (specified by code) that the player's equipment has"""
        total = 0
        for x in self.equipment:
            total += x.get_stat(code)
        return total

    # @ param key a key for the buff/debuff
    # @ param magnitude the value associated with the effect (dmg/sec, buff as %)
    # @ param duration the amount of time (in s) that the effect will last.
    def take_buff(self, key, magnitude, duration):
        """applies a buff/debuff to the player"""
        #EFFECTS: DoT, buffs: (attack, defense, move speed), knockback, stun
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
        self.hp[0] -= dmg
    
    
    #  @param g a reference to the Game class that is currently running.    
    def update(self, g):
        """update the player (per frame), using data from game g"""
        #collision detection
        self.collision = [False, False]
        #Needs to be floats to ensure the player doesn't get stuck in a wall (rounding errors cause this)
        self.futurex = self.x + self.speed * self.direction[0] * g.deltaT / 1000.0
        self.futurey = self.y + self.speed * self.direction[1] * g.deltaT / 1000.0
        
        #can't move outside the bounds of game area
        if self.futurex < 0 or self.futurex + self.rect.width > g.mapSize[0] * 24:
            #cannot move in x
            self.collision[0] = True
        if self.futurey < 0 or self.futurey + self.rect.height > g.mapSize[1] * 24:
            #cannot move in y
            self.collision[1] = True
            
        #tile collision (brute force now, OPTIMIZE THIS LATER)
        for x in range(0, g.mapSize[0]):
            for y in range(0, g.mapSize[1]):
                if g.tiles[x][y].blocking == True:
                    #test if you would be in them (24 x 24 area, cut off head top)
                    if self.futurex >= x * 24 and self.futurex <= x * 24 + 24 or \
                    self.futurex + 24 >= x * 24 and self.futurex + 24 <= x * 24 + 24:
                        if self.futurey + 8 >= y * 24 and self.futurey + 8 <= y * 24 + 24 or \
                        self.futurey + 24 + 8 >= y * 24 and self.futurey + 24 + 8 <= y * 24 + 24:
                            self.collision[0] = True
                            self.collision[1] = True
                    
            
        #move (or don't)
        if self.collision[0] == False:
            self.x += self.speed * self.direction[0] * g.deltaT / 1000.0
            self.rect.move_ip( (int)(self.x - self.rect.x), 0)
        if self.collision[1] == False:
            self.y += self.speed * self.direction[1] * g.deltaT / 1000.0
            self.rect.move_ip( 0, (int)(self.y - self.rect.y) )
        
        #parse direction
        if self.direction[0] == 1:
            self.frameDirection = 1
        elif self.direction[0] == -1:
            self.frameDirection = 3
        if self.direction[1] == 1:
            self.frameDirection = 0
        elif self.direction[1] == -1:
            self.frameDirection = 2
            
        #animate
        if self.direction != [0, 0]: #player is moving
            self.frameTimer += g.deltaT
            if self.frameTimer > self.frameDelay:
                self.frameTimer = 0
                self.frame += 1
            if self.frame > self.frameMax:
                self.frame = 0
        else: #player is idle
            self.frame = 0

    #  @param g a reference to the Game class that is currently running.        
    def draw(self, g):
        """draw the player to the screen"""
        #make a temporary surface to perform transformations on. (DO NOT TRANSFORM the img reference!)
        temp = pygame.Surface( (24, 32) ).convert()
        #transparency
        temp.fill( (255, 255, 0) )
        temp.set_colorkey( (255, 255, 0) )
        temp.blit(self.img, pygame.Rect(0, 0, 24, 32), pygame.Rect(25 * self.frameDirection, 33 * self.frame, 24, 32) )
        #make a mapping from gamespace -> view
        offset = [-1 *( g.focus[0] - g.view[0] / 2 ), -1 * ( g.focus[1] - g.view[1] / 2 ) ]
        #zoom logic
        temp = pygame.transform.scale(temp, ( (int)(temp.get_width() * g.zoom), (int)(temp.get_height() * g.zoom) ) )
        
        g.screen.blit(temp, pygame.Rect( (int)(self.x * g.zoom) + offset[0], (int)(self.y * g.zoom) + offset[1], (int)(24 * g.zoom), (int)(32 * g.zoom) ) )
        #screen.blit(self.img, pygame.Rect(self.x, self.y, 24, 32), pygame.Rect(25 * self.frameDirection, 33 * self.frame, 24, 32) )
