from creep import *
import random

##  @class ChargeCreep
#   @brief this is the charge-type creep class
class ChargeCreep(Creep):
    def __init__(self, img, x, y, game, ctype):
        #intitialize inherited stats
        super(ChargeCreep, self).__init__(img, x, y, game, (ctype[0]*12.5, ctype[1]*1.2, ctype[2]*3.5, 48))

        #we want to charge in liens
        self.update_functions.append((11, self.charge))

        #sort the list so go in order
        self.update_functions = sorted(self.update_functions, key=lambda function_tuple: function_tuple[0])

        self.old_m = (0, 0)
        self.speed = self.max_speed // 5
        self.charge_wait = 0

    ## the charge function
    #  @brief increases our move speed if we don't change direction
    def charge(self):
        #are we going in the same direction?
        if self.old_m == self.m:
            #have we increased our speed too recently?
            if self.charge_wait >= 500:
                #are we already going at max speed?
                if self.speed < self.max_speed:
                    self.speed += 2
                    #not allowed to go faster than max speed
                    if self.speed > self.max_speed:
                        self.speed = self.max_speed
            #increment waiting time
            else:
                self.charge_wait += self.game.deltaT
        #we changed direction, reset speed
        else:
            self.speed = self.max_speed // 5

        self.old_m = self.m
