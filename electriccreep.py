from creep import *
import random

##  @class ElectricCreep
#   @brief this is the electric-type creep class
class ElectricCreep(Creep):
    def __init__(self, img, x, y, type = 0x1111, game)
        #intitialize inherited stats
        super(ElectricCreep, self).__init__(x, y, type, game)
