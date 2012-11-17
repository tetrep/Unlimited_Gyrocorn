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
        self.ctype = (random.randint(1, self.game.level), random.randint(1, self.game.level), random.randint(self.game.level//2, self.game.level))

        #print "spawn: (", self.x, ',', self.y, ',', cnum, ')'
        if cnum == 1:
            return Creep(self.img, self.x, self.y, self.game, self.ctype)
        elif cnum == 2:
            return FireCreep(self.img, self.x, self.y, self.game, self.ctype)
        elif cnum == 3:
            return ElectricCreep(self.img, self.x, self.y, self.game, self.ctype)
        elif cnum == 4:
            return IceCreep(self.img, self.x, self.y, self.game, self.ctype)
        elif cnum == 5:
            return ChargeCreep(self.img, self.x, self.y, self.game, self.ctype)
