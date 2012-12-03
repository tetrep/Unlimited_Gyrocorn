from creep import *
from weapon import *
import random

##  @class FireCreep
#   @brief this is the fire-type creep class
class FireCreep(Creep):
    def __init__(self, img, x, y, game, ctype):
        #intitialize inherited stats
        super(FireCreep, self).__init__(img, x, y, game, (ctype[0], ctype[1], ctype[2], 28))

        #use a fire weapon
        self.weapon = FireWeapon(game)

    #we want to explode on death and spawn smaller minions
    def reap(self):
        #are we dead?
        if self.health <= 0:
            #spawn many little minions
            for x in range(1, self.max_health//10):
                self.game.spawn_creep(self.img, random.randint(-24, 24) + self.x, random.randint(-24, 24) + self.y, (10,10,10,10))
            return True
        else:
            return False
