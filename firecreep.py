from creep import *
import random

##  @class FireCreep
#   @brief this is the fire-type creep class
class FireCreep(Creep):
    def __init__(self, img, x, y, game, ctype = (100, 100, 100, 100)):
        #intitialize inherited stats
        super(FireCreep, self).__init__(img, x, y, ctype, game)

    #we want to explode on death and spawn smaller minions
    def reap(self):
        #are we dead?
        if self.health <= 0:
            #spawn many little minions
            for x in range(1, self.max_health//10):
                self.game.spawn_creep(self.img, random.randint(-24, 24) + self.x, random.randint(-24, 24), ctype)
            return True
        else:
            return False
