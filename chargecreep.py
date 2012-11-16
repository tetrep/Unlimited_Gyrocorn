from creep import *
import random

##  @class ChargeCreep
#   @brief this is the charge-type creep class
class ChargeCreep(Creep):
    def __init__(self, img, x, y, game, ctype = (100, 100, 100, 100)):
        #intitialize inherited stats
        super(ChargeCreep, self).__init__(img, x, y, game, (ctype[0]*12.5, ctype[1]*8, ctype[2]*3.5, ctype[3]*0.01))
        self.speed_mod = 1
