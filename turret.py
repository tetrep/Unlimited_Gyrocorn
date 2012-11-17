import pygame
import time
#from bullet import *
from bulletfactory import *

## @class Turret
#  @brief this is the Turret class
class Turret(object):
    ## the Turret constructor
    #  @param game the instance of the class Game that this Turret resides in
    #  @param starting_x the x coordinate that marks the middle position of the tower (defaults to 0)
    #  @param starting_y the y coordinate that marks the bottom position of the tower (defaults to 0)
    #  @todo add basics for turret animation, lock tower placement to tiles
    def __init__(self, game, img, type, attack_speed, starting_x = 0, starting_y = 0):
        self.img = img
        self.rect = self.img.get_rect()
        
        tile_position_x = (starting_x - (starting_x % 24) ) / 24
        tile_position_y = (starting_y - (starting_y % 24) ) / 24      
        
        self.x = (tile_position_x * 24)
        self.rect.x = (tile_position_x * 24)
        self.y = (tile_position_y * 24) - self.rect.height + 24
        self.rect.y = (tile_position_y * 24) - self.rect.height + 24
        
        
        #on placement, checks whether a tower is colliding with terrain or another tower
        #colliding towers are cleaned up at the end of update in the game class
        self.valid_placement = True
        
        if game.tiles[int(tile_position_x)][int(tile_position_y)].blocking == True:
            self.valid_placement = False
        
        game.tiles[int(tile_position_x)][int(tile_position_y)].setBlocking(True)  
                
                
        self.attack_speed = attack_speed
        self.attack_area_of_effect = 0
        self.attack_damage = 0
        self.attack_range = 0
        self.type = type
        
        self.damage_level = 1
        self.attack_speed_level = 1
        self.aoe_level = 1
        self.range_level = 1
        
        self.bulletFactory = BulletFactory();
        self.projectiles = []
        self.time_of_last_shot = 0
        self.target = 0
        
    ## the Turret update
    #  @param game the instance of the class Game that this Turret resides in
    #  @todo add attacking and animation
    def update(self, game):
        """update the turret (per frame)"""
    
        #fires a bullet based on attack speed
        if self.time_of_last_shot >= self.attack_speed:
            #keeps track of when you fired the bullet
            #self.time_of_last_shot = self.time_of_last_shot + game.deltaT
            self.time_of_last_shot = 0
            #finds a target for the bullets you fire in this frame
            self.target = self.findTarget(game.creeps)
            #actually fires the bullet
            if self.target != 0:
                center_x = self.rect.x + (self.rect.width / 2)
                center_y = self.rect.y + (self.rect.height / 2)
                self.projectiles.append(self.bulletFactory.createBullet(game, self.type, self.attack_area_of_effect, self.attack_damage, self.attack_range, self.target, center_x, center_y))
            #elif self.time_of_last_shot + self.attack_speed < pygame.time.get_ticks() / 1000.0:   
            #    self.time_of_last_shot = -1
        else:
            self.time_of_last_shot = self.time_of_last_shot + game.deltaT
        
            
        #updates existing bullets
        for b, bullet in enumerate(self.projectiles):
            if bullet.dead == True:
                self.projectiles.pop(b)
            bullet.update(game)
    
    ## the Turret draw
    # @param g a reference to the Game that is currently running
    def draw(self, g):
        """draw the turret to the screen"""
        #declare a temporary surface to apply transformations to
        temp = pygame.Surface( (self.rect.width, self.rect.height) ).convert()
        #set up transparency
        temp.fill( (255, 255, 0) )
        temp.set_colorkey( (255, 255, 0) )
        #draw img to temp
        temp.blit(self.img, pygame.Rect(0, 0, self.rect.width, self.rect.height) )
        #calculate offset
        offset = [-1 *( g.focus[0] - g.view[0] / 2 ), -1 * ( g.focus[1] - g.view[1] / 2 ) ]
        #zoom logic
        temp = pygame.transform.scale(temp, ( (int)(self.rect.width * g.zoom), (int)(self.rect.height * g.zoom) ))
        #draw to the game screen
        g.screen.blit( temp, pygame.Rect( (int)(self.x * g.zoom) + offset[0], (int)(self.y * g.zoom) + offset[1], \
            (int)(self.rect.width * g.zoom), (int)(self.rect.height * g.zoom) ) )
        
        #if self.target != 0:
        #    if self.target.health > 0:   
        #        pygame.draw.line( g.screen, (255, 0, 0) , (self.rect.x + (self.rect.width / 2), self.rect.y + (self.rect.height / 2)), (self.target.x, self.target.y), 1)
            
        for bullet in self.projectiles:
            bullet.draw(g)
        #g.screen.blit(self.img, pygame.Rect(self.x, self.y, self.rect.width, self.rect.height), pygame.Rect(0, 0, self.rect.width, self.rect.height) )
    
    ## find the target for the bullet is it about to fire
    ## right now this only finds the closest enemy to the turret
    # @param the list of creeps to search through
    def findTarget(self, creeps):
        min_distance = -1
        min_creep = -1
        for creep in creeps:
            x_distance = creep.x - self.x
            y_distance = creep.y - self.y
            total_distance = math.sqrt(x_distance**2 + y_distance**2)
            if total_distance < min_distance or min_distance == -1:
                min_distance = total_distance
                min_creep = creep
        if min_creep == -1:
            return 0
        else:
            return min_creep
            
    def getDamageLevel(self):
        return self.damage_level
        
    def getAttackSpeedLevel(self):
        return self.attack_speed_level
        
    def getAoELevel(self):
        return self.aoe_level
        
    def getRangeLevel(self):
        return self.range_level
    
    
    
    def upgradeDamage(self):
        if(self.damage_level >= 5):
            return False
        else:
            self.damage_level = self.damage_level + 1
            self.attack_damage = self.attack_damage + 10
            return True
        
    def upgradeAttackSpeed(self):
        if(self.attack_speed_level >= 5):
            return False
        else:
            self.attack_speed_level = self.attack_speed_level + 1
            self.attack_speed = self.attack_speed - .25
            return True
        
    def upgradeAoE(self):
        if(self.aoe_level >= 5):
            return False
        else:
            self.aoe_level = self.aoe_level + 1
            self.attack_area_of_effect = self.attack_area_of_effect + 5
            return True
        
    def upgradeRange(self):
        if(self.range_level >= 5):
            return False
        else:
            self.range_level = self.range_level + 1
            self.attack_range = self.attack_range + 0.75
            return True
        
