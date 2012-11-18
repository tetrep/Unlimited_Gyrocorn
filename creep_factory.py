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
        if(len(self.game.tiles.spawns) != 0):
            tempnum = random.randint(0, len(self.game.tiles.spawns)-1)
            x = self.game.tiles.spawns[tempnum][0]
            y = self.game.tiles.spawns[tempnum][1]
        else:
            x = random.randint(30, 300)
            y = random.randint(30, 300)

        ctype = (random.randint(self.game.level//2, self.game.level), random.randint(self.game.level//2, self.game.level), random.randint(self.game.level//2, self.game.level))

        #print "spawn: (", self.x, ',', self.y, ',', cnum, ')'
        if cnum == 1:
            return Creep(self.img, x, y, self.game, ctype)
        elif cnum == 2:
            return FireCreep(self.img, x, y, self.game, ctype)
        elif cnum == 3:
            return ElectricCreep(self.img, x, y, self.game, ctype)
        elif cnum == 4:
            return IceCreep(self.img, x, y, self.game, ctype)
        elif cnum == 5:
            return ChargeCreep(self.img, x, y, self.game, ctype)
