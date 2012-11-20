import pygame
import time
from turret import *

class TurretFactory():
    ## the TurretFactory constructor
    def __init__(self):
        # load tower images
        self.imgBasicTurret = pygame.image.load("Art/tiles/obj-guardtower.png").convert()
        self.imgBasicTurret.set_colorkey( (255, 0, 255) )
        self.imgSniperTurret = pygame.image.load("Art/tiles/snipertower.png").convert()
        self.imgSniperTurret.set_colorkey( (255, 0, 255) )
        self.imgPiercingTurret = pygame.image.load("Art/tiles/piercingtower.png").convert()
        self.imgPiercingTurret.set_colorkey( (255, 0, 255) )
        self.imgMortarTurret = pygame.image.load("Art/tiles/mortartower.png").convert()
        self.imgMortarTurret.set_colorkey( (255, 0, 255) )
        self.imgParalyzeTurret = pygame.image.load("Art/tiles/paralyzetower.png").convert()
        self.imgParalyzeTurret.set_colorkey( (255, 0, 255) )
        self.imgFireTurret = pygame.image.load("Art/tiles/firetower.png").convert()
        self.imgFireTurret.set_colorkey( (255, 0, 255) )
        self.imgIceTurret = pygame.image.load("Art/tiles/icetower.png").convert()
        self.imgIceTurret.set_colorkey( (255, 0, 255) )
        self.imgLightningTurret = pygame.image.load("Art/tiles/lightningtower.png").convert()
        self.imgLightningTurret.set_colorkey( (255, 0, 255) )
    
    ## Creates a Turret based on input type
    #  @param game the instance of the class Game that this Turret resides in
    #  @param type the 0-7 value corresponding to a specific type of turret
    #  @param starting_x the x coordinate of the turret (defaults to 0)
    #  @param starting_y the y coordinate of the turret (defaults to 0)
    def createTurret(self, game, type, starting_x = 0, starting_y = 0):
        # turret constructor is game, image, type, attack speed, startign x, starting y
    
        # Basic Turret
        if type == 0:
            return Turret(game, self.imgBasicTurret, 0, 1, starting_x, starting_y)
        # Sniper Turret
        elif type == 1:
            return Turret(game, self.imgSniperTurret, 1, 4, starting_x, starting_y)
        # Piercing Turret
        elif type == 2:
            return Turret(game, self.imgPiercingTurret, 2, 2, starting_x, starting_y)
        # Mortar Turret
        elif type == 3:
            return Turret(game, self.imgMortarTurret, 3, 3, starting_x, starting_y)
        # Paralyze Turret
        elif type == 4:
            return Turret(game, self.imgParalyzeTurret, 4, 4, starting_x, starting_y)
        # Fire Turret
        elif type == 5:
            return Turret(game, self.imgFireTurret, 5, 1, starting_x, starting_y)
        # Ice Turret
        elif type == 6:
            return Turret(game, self.imgIceTurret, 6, 1, starting_x, starting_y)
        # Lightning Turret
        elif type == 7:
            return Turret(game, self.imgLightningTurret, 7, 1, starting_x, starting_y)
      
        