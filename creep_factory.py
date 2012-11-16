from creep import *
from chargecreep import *
from icecreep import *
from firecreep import *
from electriccreep import *
from creep import *

import random

#  @class CreepFactory
#  @brief handle generation of creeps
class CreepFactory(object):
    def __init__(self, img, game):
        self.img = img
        self.game = game
        pass
    def make(self, cnum):
        self.x = random.randint(30, 300)
        self.y = random.randint(30, 300)
        self.ctype = (random.randint(1, self.game.level), random.randint(1, self.game.level), random.randint(1, self.game.level), random.randint(1, self.game.level))
        if cnum == 1:
            return Creep(img, self.x, self.y, self.game, self.ctype)
        elif cnum == 2:
            return FireCreep(img, self.x, self.y, self.game, self.ctype)
        elif cnum == 3:
            return ElectricCreep(img, self.x, self.y, self.game, self.ctype)
        elif cnum == 4:
            return IceCreep(img, self.x, self.y, self.game, self.ctype)
        elif cnum == 5:
            return ChargeCreep(img, self.x, self.y, self.game, self.ctype)
