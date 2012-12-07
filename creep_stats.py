import random

##  @class CreepStats
#   @brief a class for holding stat formulas to initialize creeps
class CreepStats(object):
    def __init__(self):
        #intitialize inherited stats
        super(CreepStats, self).__init__()

        self.level = 0

        self.defenseBase = 100
        self.defenseGrowth = 0
        
        self.absorbtionBase = 0
        self.absorbtionGrowth = 1
        
        self.healthBase = 200
        self.healthGrowth = 30

    def randomize_level(self, minimum, maximum):
        """assigns a random level within range to the stats"""
        self.level = random.randint(minimum, maximum)

    def get_health(self):
        """get the total health"""
        return self.healthBase + self.healthGrowth * self.level

    def get_defense(self):
        """get the total defense"""
        return self.defenseBase + self.defenseGrowth * self.level

    def get_absorbtion(self):
        """get the total absorbtion"""
        return self.absorbtionBase + self.absorbtionGrowth * self.level

    def set_health_growth(self, i):
        """set the health increase / level"""
        self.healthGrowth = i

    def set_absorbtion_growth(self, i):
        """set the absorbtion increase / level"""
        self.absorbtionGrowth = i

    def set_defense_growth(self, i):
        """set the defense increase / level"""
        self.defenseGrowth = i

    def set_health_base(self, i):
        """set the health increase / level"""
        self.healthBase = i

    def set_absorbtion_base(self, i):
        """set the absorbtion increase / level"""
        self.absorbtionBase = i

    def set_defense_base(self, i):
        """set the defense increase / level"""
        self.defenseBase = i
