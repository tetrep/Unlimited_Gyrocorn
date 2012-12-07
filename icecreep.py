from creep import *
from weapon import *
import random

##  @class IceCreep
#   @brief this is the ice-type creep class
class IceCreep(Creep):
    def __init__(self, img, x, y, game, ctype):
        #intitialize inherited stats
        super(IceCreep, self).__init__(img, x, y, game, (ctype[0], ctype[1], ctype[2], 16))

        #use a ice weapon
        self.weapon = IceWeapon(game)
