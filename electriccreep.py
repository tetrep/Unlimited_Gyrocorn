from creep import *
from weapon import *
import random

##  @class ElectricCreep
#   @brief this is the electric-type creep class
class ElectricCreep(Creep):
    def __init__(self, img, x, y, game, ctype):
        #intitialize inherited stats
        super(ElectricCreep, self).__init__(img, x, y, game, (ctype[0]*5, ctype[1]*12.5, ctype[2]*5, 40))

        #use an electric weapon
        self.weapon = ElectricWeapon
