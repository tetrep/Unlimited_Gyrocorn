import pygame
import time
from bullet import *

## @class Turret
#  @brief this is the Turret class
class Turret(object):
    ## the Turret constructor
    #  @param game the instance of the class Game that this Turret resides in
    #  @param starting_x the x coordinate that marks the middle position of the tower (defaults to 0)
    #  @param starting_y the y coordinate that marks the bottom position of the tower (defaults to 0)
    #  @todo add basics for turret animation, lock tower placement to tiles
    def __init__(self, game, starting_attack_speed, starting_attack_damage, starting_attack_area_of_effect, starting_attack_projectile_speed, starting_x = 0, starting_y = 0):
        self.img = game.imgBasicTurret
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
                
        #attacking statistics
        self.should_attack = True
        self.attack_speed = starting_attack_speed
        self.attack_damage = starting_attack_damage
        self.attack_area_of_effect = starting_attack_area_of_effect
        self.attack_projectile_speed = starting_attack_projectile_speed
        self.attack_damage_type = "BASIC"

        
        self.projectiles = []
        self.time_of_last_shot = -1
    
    ## the Turret update
    #  @param game the instance of the class Game that this Turret resides in
    #  @todo add attacking and animation
    def update(self, game):
        """update the turret (per frame)"""
    
        #fires a bullet based on attack speed
        if self.time_of_last_shot == -1:
            #keeps track of when you fired the bullet
            self.time_of_last_shot = pygame.time.get_ticks() / 1000.0
            #finds a target for the bullets you fire in this frame
            target = self.findTarget(game.creeps)
            #actually fires the bullet
            if target != 0:
                self.projectiles.append(Bullet(game, self.attack_damage, self.attack_area_of_effect, self.attack_projectile_speed, target.rect.x, target.rect.y,
                    self.rect.x + (self.rect.width / 2), self.rect.y + (self.rect.height / 2)))
        elif self.time_of_last_shot + self.attack_speed < pygame.time.get_ticks() / 1000.0:   
            self.time_of_last_shot = -1
        
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
    
    ## set the Turret attack speed
    # @param new_attack_speed the attack_speed the Turret will be given (default to 0)
    def setAttackSpeed(self, new_attack_speed = 0):
        self.attack_speed = new_attack_speed
        
    ## set the Turret attack damage
    # @param new_attack_damage the attack_damage the Turret will be given (default to 0)
    def setAttackDamage(self, new_attack_damage = 0):
        self.attack_damage = new_attack_damage
        
    ## set the Turret attack damage type
    # @param new_attack_damage_type the attack_damage_type the Turret will be given (default to "NONE")
    def setAttackDamageType(self, new_attack_damage_type = "NONE"):
        self.attack_damage_type = new_attack_damage_type
        
