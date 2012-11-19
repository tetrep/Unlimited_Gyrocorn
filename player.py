import pygame
from mod_enum import *
from equipment import *
from skill import *
from superclass import *
from bulletfactory import *
from target import *

class Player(SuperClass):
    #  @param img a reference to a pygame.Surface containing the spritesheet to be used for draw calls.
    #  @param img2 a refence to a pygame.Surface containing the spritesheet to use when the player is not active.
    def __init__(self, game, img, img2, pos=(0,0)):
        """initialize player"""
        super(Player, self).__init__()
        self.game = game
        self.update_functions = None
        self.img = img
        self.img2 = img2
        self.font = pygame.font.Font(None, 32)
        
        self.x = pos[0] #position in pixels
        self.y = pos[1]-8 #position in pixels
        self.rect = pygame.Rect(self.x, self.y, 24, 32) #collision box
        self.speed = 64.0 #speed in pixels/sec
        self.direction = [0, 0] #-1, 0, or 1 x multiplier for orientation of motion along x and y axes
        self.collision = [False, False] #whether the x or y axes of motion are obstructed

        #mechanical variables
        self.active = False
        self.dead = False
        self.deadt = 0
        self.reviveTime = 30

        self.bulletFactory = BulletFactory()
        self.attackTimer = 0
        self.attackDelay = 1.0
        
        self.exp = 10000000
        self.gold = 1000
        self.hp = [100.0, 100]  #hp [current, max]
        self.mana = [100.0, 100]#mana [current, max]
        self.baseAttack = 100   #base attack
        self.baseDefense = 100  #base defense
        self.baseSpeed = 64.0   #base speed
        
        self.attack = 100       #total attack (cap: 1,700) (ABS CAP: 10,000)
        self.defense = 100      #total defense (cap: 1,600)(ABS CAP: 10,000)
        self.absorbtion = 0     #damage absorbtion: applied 50% before and 50% after defense
        self.regen = 0.00       #life regen (HP / sec)
        self.lifeLeech = 0.00   #% damage stolen as life per hit
        self.crit = 0.00        #% chance of scoring a critical hit
        self.attackSpeedMultiplier = 1.0
        self.moveSpeedMultiplier = 1.0
        

        self.buffs = []
        self.equipment = [Equipment(), Equipment(), Equipment(), Equipment()]
        self.skill = [Skill(), Skill(), Skill(), Skill()]

        #animation variables
        self.frame = 0          #current frame in animation
        self.frameMax = 7       #number of frames in animation
        self.frameDirection = 0 #parsed player facing
        self.frameTimer = 0     #ms spent in current frame
        self.frameDelay = 100   #time between frames in ms
        
    def update_stats(self):
        """updates stats used for calculations based on equipment"""
        modEnum = Mod_Enum()
        self.attack = self.baseAttack + self.get_stat(modEnum.MOD_ATTACK)
        self.defense = self.baseDefense + self.get_stat(modEnum.MOD_DEFENSE)
        self.hp[1] = 100 * ( 1 + self.get_stat(modEnum.MOD_HP) )
        self.absorbtion = self.get_stat(modEnum.MOD_ABSORB)
        self.regen = 0.00 + self.get_stat(modEnum.MOD_REGEN)
        self.lifeLeech = 0.00 + self.get_stat(modEnum.MOD_LEECH)
        self.crit = 0.00 + self.get_stat(modEnum.MOD_CRIT)
        self.attackSpeedMultiplier = 1.0 + self.get_stat(modEnum.MOD_ATTACK_SPEED)
        self.moveSpeedMultiplier = 1.0 + self.get_stat(modEnum.MOD_MOVE_SPEED)
        #cap move speed
        if self.moveSpeedMultiplier > 4.0:
            self.moveSpeedMultiplier = 4.0 + 0.25 * (self.moveSpeedMultiplier - 4.0)
        
        self.speed = self.baseSpeed * self.moveSpeedMultiplier


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
    
    def take_damage(self, dmg, dtype = 1):
        """applies modifiers to damage, then takes it"""
        self.game.hit_sound.play()
        
        #DR% = 1 - (100 / x). 
        damageMultiplier = 100.0 / float(self.defense)
        #Apply defense buffs/debuffs
        #calculate damage:
        dmg -= self.absorbtion
        dmg *= damageMultiplier
        #apply damage
        self.hp[0] -= dmg

    def reset_movement(self):
        """Reset the player's movement vector."""
        self.direction = [0, 0]

    def activate(self):
        """give player control over this unit"""
        self.active = True
        
    def deactivate(self):
        """give AI control over this unit"""
        self.active = False

    def use_skill(self, g, i, x, y):
        """uses the player's ith skill"""
        # @ param g a reference to the game engine
        # @ param i the index of the skill (basically what skill)
        # @ param x the x target coordinate in game pixels
        # @ param y the y target coordinate in game pixels
        if self.attackTimer < self.attackDelay:
            print("attack on CD")
            return
        
        if self.skill[i].skillAttr == 0:
            g.fire_skill_sound.play()
        elif self.skill[i].skillAttr == 1:
            g.ice_skill_sound.play()
        elif self.skill[i].skillAttr == 2:
            g.lightning_skill_sound.play()
        elif self.skill[i].skillAttr == 3:
            g.poison_skill_sound.play()
        
        
        if self.skill[i].skillKey == 0: #Aura
            #turn the aura on/off
            if self.skill[i].active == False:
                print("aura on")
                self.skill[i].active = True
            else:
                self.skill[i].active = False
                print("aura off")
        
        elif self.skill[i].skillKey == 1: #Missile
            if self.mana[0] > self.skill[i].skillCost:
                self.mana[0] -= self.skill[i].skillCost
                self.attackTimer = 0
                target = Target(x, y)
                center_x = self.rect.x + (self.rect.width / 2)
                center_y = self.rect.y + (self.rect.height / 2)
                #bullet types: fire 5, ice 6, lightning 7
                #skill types: fire 0, ice 1, lightning 2
                g.bullets.append(self.bulletFactory.createBullet(g, self.skill[i].skillAttr + 5, 0, self.attack, 1024, target, center_x, center_y))
                print("missile")

        elif self.skill[i].skillKey == 2: #Breath
            #for each creep in the AoE cone, do damage.
            if self.mana[0] > self.skill[i].skillCost:
                self.mana[0] -= self.skill[i].skillCost
                self.attackTimer = 0
                #get low and high angle (-45 degrees and +45 degrees from player -> point angle)
                lowAngle = math.atan2(y - self.rect.centery, x - self.rect.centerx)  - 3.1415 / 2.0
                highAngle = math.atan2(y - self.rect.centery, x - self.rect.centerx) + 3.1415 / 2.0
                for creep in g.creeps:
                    #get angle to creep
                    creepAngle = math.atan2(creep.rect.centery - self.rect.centery, creep.rect.centerx - self.rect.centerx)
                
                    #if angle to the creep is between the two angles
                    if creepAngle > lowAngle and creepAngle < highAngle:
                        #and the distance to the creep is below the skill's range
                        if ( (creep.rect.centerx - self.rect.centerx) ** 2 + (creep.rect.centery - self.rect.centery) ** 2 ) ** 0.5 < 4 * 24:
                            creep.take_damage( self.attack )
                            print("breath")

    def do_ai(self):
        """perform AI actions"""
        skillID = []
        for i in range(0, self.skill.__len__() ):
            #1: if the player has less than 10% mana, deactivate all auras
            #   else, activate all auras
            if self.skill[i].skillKey == 0: #Aura
                if self.mana[0] < 0.1 * self.mana[1]:
                    self.skill[i].active = False
                else:
                    self.skill[i].active = True
            else: #non-aura
                #aim it at the nearest creep
                mindist = 9999
                x = 0
                y = 0
                for creep in self.game.creeps:
                    dist = ( (creep.rect.centerx - self.rect.centerx) ** 2 + (creep.rect.centery - self.rect.centery) ** 2 ) ** 0.5
                    if dist < mindist:
                        mindist = dist
                        x = creep.rect.centerx
                        y = creep.rect.centery
                #if a target was found, use the skill
                if mindist < 9999:
                    self.use_skill( self.game, i, x, y )
                
    
    
    #  @param g a reference to the Game class that is currently running.    
    def update(self, g):
        """update the player (per frame), using data from game g"""
        
        self.game = g
        
        #if the player is dead, KILL THEM
        if self.hp[0] <= 0 and self.dead == False:
            self.dead = True
            self.deadt = 0
            #clear debuffs

        if self.dead == True:
            self.deadt += g.deltaT / 1000.0
            if self.deadt > self.reviveTime: #recussitate after 30 seconds
                self.dead = False
                self.hp[0] = self.hp[1]
            return #if dead, ignore input and all other updates
                
        elif self.dead == False:
            self.hp[0] += self.regen * g.deltaT / 1000.0
            if self.hp[0] > self.hp[1]:
                self.hp[0] = self.hp[1]
            self.mana[0] += g.deltaT / 1000.0
            if self.mana[0] > self.mana[1]:
                self.mana[0] = self.mana[1]
            self.attackTimer += self.attackSpeedMultiplier * g.deltaT / 1000.0
            #check debuffs
            self.checkBurning()
            self.checkChilled()
            self.checkShocked()
            self.checkParalyzed()
            
            
        #AURA
        for skill in self.skill:
            if skill.skillKey == 0 and skill.active == True: #aura is on
                #damage all creeps in AoE
                for creep in g.creeps:
                    if ( (creep.rect.centerx - self.rect.centerx) ** 2 + (creep.rect.centery - self.rect.centery) ** 2 ) ** 0.5 < 4 * 24:
                        creep.take_damage( self.attack * g.deltaT / 1000.0 ) #THIS SHOULD IGNORE ABSORBTION?
                #buff all players in AoE
                #take mana
                self.mana[0] -= float(skill.skillCost) * g.deltaT / 1000.0

        #AI
        if self.active == False and self.attackTimer >= self.attackSpeedMultiplier:
            self.do_ai()
        
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
            
        #tile collision
        for x in range( int(self.x / 24) - 1, int(self.x / 24) + 2):
            for y in range( int( (self.y + 8) / 24) - 1, int( (self.y + 8) / 24) + 2):
                if x > -1 and x < g.mapSize[0] and y > -1 and y < g.mapSize[1]:
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
        #if the player is dead, show the revive counter
        if self.dead == True:
            pos = g.convertGamePixelsToZoomCoorinates( (self.x, self.y) )
            g.screen.blit(self.font.render( str( int( self.reviveTime - self.deadt ) ), 0, (255, 255, 255) ), pygame.Rect( pos[0], pos[1], 64, 32 ) )
            return #don't draw them if they died.
        
        #make a temporary surface to perform transformations on. (DO NOT TRANSFORM the img reference!)
        temp = pygame.Surface( (24, 32) ).convert()
        #transparency
        temp.fill( (255, 255, 0) )
        temp.set_colorkey( (255, 255, 0) )
        if self.active == True:
            temp.blit(self.img, pygame.Rect(0, 0, 24, 32), pygame.Rect(25 * self.frameDirection, 33 * self.frame, 24, 32) )
        else:
            temp.blit(self.img2, pygame.Rect(0, 0, 24, 32), pygame.Rect(25 * self.frameDirection, 33 * self.frame, 24, 32) )
        #make a mapping from gamespace -> view
        pos = g.convertGamePixelsToZoomCoorinates( (self.x, self.y) )
        #zoom logic
        temp = pygame.transform.scale(temp, ( (int)(temp.get_width() * g.zoom), (int)(temp.get_height() * g.zoom) ) )
        
        g.screen.blit(temp, pygame.Rect( pos[0], pos[1], (int)(24 * g.zoom), (int)(32 * g.zoom) ) )
        #screen.blit(self.img, pygame.Rect(self.x, self.y, 24, 32), pygame.Rect(25 * self.frameDirection, 33 * self.frame, 24, 32) )
