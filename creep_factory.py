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
        #find a path for our lovely creeps if we don't have one
        if self.game.cp.pathed == False:
            self.game.cp.find_path()

        if(len(self.game.tiles.spawns) != 0):
            tempnum = random.randint(0, len(self.game.tiles.spawns)-1)
            x = self.game.tiles.spawns[tempnum][0]*self.game.tiles.tileSize.width
            y = self.game.tiles.spawns[tempnum][1]*self.game.tiles.tileSize.height
        else:
            x = random.randint(30, 300)
            y = random.randint(30, 300)

        ctype = (random.randint(self.game.level//2, self.game.level)+1, random.randint(self.game.level//2, self.game.level)+1, random.randint(self.game.level//2, self.game.level)+1)

        #print "spawn: (", self.x, ',', self.y, ',', cnum, ')'
        if cnum == 1:
            return Creep(self.game.imgCreep, x, y, self.game, ctype)
        elif cnum == 2:
            return FireCreep(self.game.imgCreepFire, x, y, self.game, ctype)
        elif cnum == 3:
            return ElectricCreep(self.game.imgCreepLightning, x, y, self.game, ctype)
        elif cnum == 4:
            return IceCreep(self.game.imgCreepFrost, x, y, self.game, ctype)
        elif cnum == 5:
            return ChargeCreep(self.game.imgCreepArmored, x, y, self.game, ctype)
