from creep import *
from weapon import *
import random

##  @class ElectricCreep
#   @brief this is the electric-type creep class
class ElectricCreep(Creep):
    def __init__(self, img, x, y, game, ctype = (100, 100, 100, 100)):
        #intitialize inherited stats
        super(ElectricCreep, self).__init__(img, x, y, game, ctype)

        #use an electric weapon
        self.weapon = ElectricWeapon
