from creep import *
import random

##  @class IceCreep
#   @brief this is the ice-type creep class
class IceCreep(Creep):
    def __init__(self, img, x, y, game, ctype = (100, 100, 100, 100)):
        #intitialize inherited stats
        super(IceCreep, self).__init__(img, x, y, game, ctype)
