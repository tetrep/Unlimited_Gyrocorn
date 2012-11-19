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
        
    def createBullet(self, game, type, area_of_effect, damage, range, target, starting_x = 0, starting_y = 0):
        # bullet constructor is game, image, area of effect, attack damage, range, damage type, target, starting x, starting y

        # Basic Bullet
        if type == 0:
            return Bullet(game, self.imgBasicBullet, 0 + area_of_effect, 2 + damage, 1 + range, 1, target, starting_x, starting_y)
        # Sniper Bullet
        elif type == 1:
            return Bullet(game, self.imgSniperBullet, 0 + area_of_effect, 30 + damage, 1 + range, 1, target, starting_x, starting_y)
        # Piercing Bullet
        elif type == 2:
            return PiercingBullet(game, self.imgPiercingBullet, 0 + area_of_effect, 10 + damage, 1 + range, 1, target, starting_x, starting_y)
        # Mortar Bullet
        elif type == 3:
            return MortarBullet(game, self.imgMortarBullet, 20 + area_of_effect, 8 + damage, 1 + range, 1, target, starting_x, starting_y)
        # Paralyze Bullet
        elif type == 4:
            return ParalyzeBullet(game, self.imgParalyzeBullet, 0 + area_of_effect, 0 + damage, 1 + range, 1, target, starting_x, starting_y)
        # Fire Bullet
        elif type == 5:
            return FireBullet(game, self.imgFireBullet, 0 + area_of_effect, 10 + damage, 1 + range, 2, target, starting_x, starting_y)
        # Ice Bullet
        elif type == 6:
            return IceBullet(game, self.imgIceBullet, 0 + area_of_effect, 10 + damage, 1 + range, 3, target, starting_x, starting_y)
        # Lightning Bullet
        elif type == 7:
            return LightningBullet(game, self.imgLightningBullet, 0 + area_of_effect, 10 + damage, 1 + range, 4, target, starting_x, starting_y)