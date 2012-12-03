from creep import *
from chargecreep import *
from icecreep import *
from firecreep import *
from electriccreep import *
from creep import *
from creep_stats import *

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

        cStats = CreepStats()
        cStats.randomize_level(self.game.level//2, self.game.level)
        #set stats by creep class
        if cnum == 1: #normal
            pass #default stats are fine
        elif cnum == 2: #fire
            #lower HP
            cStats.set_health_base(160)
            cStats.set_health_growth(15)
        elif cnum == 3: #electric
            #low HP, high absorbtion
            cStats.set_health_base(100)
            cStats.set_health_growth(10)
            cStats.set_absorbtion_base(75)
            cStats.set_absorbtion_growth(2)
        elif cnum == 4: #frost
            #tanky mages. Get nasty later on?
            cStats.set_health_base(100)
            cStats.set_health_growth(60)
            cStats.set_absorbtion_base(0)
            cStats.set_absorbtion_growth(1)
            cStats.set_defense_growth(1)
        elif cnum == 5: #armored
            #HIGH defensive stats, all around.
            cStats.set_health_base(400)
            cStats.set_health_growth(60)
            cStats.set_absorbtion_base(50)
            cStats.set_absorbtion_growth(1)
            cStats.set_defense_growth(2)
            
        ctype = (cStats.get_defense(), cStats.get_absorbtion(), cStats.get_health(), 24)

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
