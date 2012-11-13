import pygame
import time
from bullet import *
from piercingbullet import *
from mortarbullet import *
from paralyzebullet import *
from firebullet import *
from icebullet import *
from lightningbullet import *

class BulletFactory():
    def __init__(self):
        # load bullet images
        self.imgBasicBullet = pygame.image.load("Art/items/itm-glaive.png").convert()
        self.imgBasicBullet.set_colorkey( (255, 0, 255) )
        self.imgSniperBullet = pygame.image.load("Art/items/sniperbullet.png").convert()
        self.imgSniperBullet.set_colorkey( (255, 0, 255) )
        self.imgPiercingBullet = pygame.image.load("Art/items/piercingbullet.png").convert()
        self.imgPiercingBullet.set_colorkey( (255, 0, 255) )
        self.imgMortarBullet = pygame.image.load("Art/items/mortarbullet.png").convert()
        self.imgMortarBullet.set_colorkey( (255, 0, 255) )
        self.imgParalyzeBullet = pygame.image.load("Art/items/paralyzebullet.png").convert()
        self.imgParalyzeBullet.set_colorkey( (255, 0, 255) )
        self.imgFireBullet = pygame.image.load("Art/items/firebullet.png").convert()
        self.imgFireBullet.set_colorkey( (255, 0, 255) )
        self.imgIceBullet = pygame.image.load("Art/items/icebullet.png").convert()
        self.imgIceBullet.set_colorkey( (255, 0, 255) )
        self.imgLightningBullet = pygame.image.load("Art/items/lightningbullet.png").convert()
        self.imgLightningBullet.set_colorkey( (255, 0, 255) )
        
    def createBullet(self, game, type, target, starting_x = 0, starting_y = 0):
        # bullet constructor is game, image, attack damage, damage type, target, starting x, starting y

        # Basic Bullet
        if type == 0:
            return Bullet(game, self.imgBasicBullet, 2, 1, target, starting_x, starting_y)
        # Sniper Bullet
        elif type == 1:
            return Bullet(game, self.imgSniperBullet, 30, 1, target, starting_x, starting_y)
        # Piercing Bullet
        elif type == 2:
            return PiercingBullet(game, self.imgPiercingBullet, 10, 1, target, starting_x, starting_y)
        # Mortar Bullet
        elif type == 3:
            return MortarBullet(game, self.imgMortarBullet, 8, 1, target, starting_x, starting_y)
        # Paralyze Bullet
        elif type == 4:
            return ParalyzeBullet(game, self.imgParalyzeBullet, 0, 1, target, starting_x, starting_y)
        # Fire Bullet
        elif type == 5:
            return FireBullet(game, self.imgFireBullet, 10, 2, target, starting_x, starting_y)
        # Ice Bullet
        elif type == 6:
            return IceBullet(game, self.imgIceBullet, 10, 3, target, starting_x, starting_y)
        # Lightning Bullet
        elif type == 7:
            return LightningBullet(game, self.imgLightningBullet, 10, 4, target, starting_x, starting_y)