from creep import *
import random

##  @class IceCreep
#   @brief this is the ice-type creep class
class IceCreep(Creep):
    def __init__(self, img, x, y, type = 0x1111, game)
        #intitialize inherited stats
        super(IceCreep, self).__init__(x, y, type, game)
