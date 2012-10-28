from mod_enum import *

class Equipment(object):
    def __init__(self):
        """initialize equipment"""
        self.locked = True
        self.slots = [Slot(), Slot(), Slot(), Slot()]
        
    def unlock(self):
        """unlocks the equipment"""
        self.locked = False

    #returns 0 normally. returns -1 if item is completely unlocked.
    def unlock_slot(self):
        """unlock the next slot"""
        for i in range(0, 4):
            if self.slots[i].locked == True:
                self.slots[i].locked = False
                return 0
        #already completely unlocked
        return -1

    # @ param code the mod code of the stat to get the total of
    def get_stat(self, code):
        """get the total amount of the stat meant by <code> across all slots in this equipment"""
        #the mod codes are specified in the mod_enum class
        total = 0
        for x in self.slots:
            total += x.get_stat(code)
        return total

class Slot(object):
    def __init__(self):
        """initialize the slot"""
        self.locked = True
        self.modCode = 0    #a code representing a stat
        self.modTier = 0    #the tier for that stat.
        self.modValue = 0   #a value for that stat, which is a function of the stat and tier.
        self.modEnum = Mod_Enum()   #an enum storing mod codes as constants. (memory inefficient)

    # @ param code the mod code of the stat.
    # @ param tier the tier of the stat modifier, bounded between (1, 4)
    def assign_slot(self, code, tier):
        """DOES STAT SCALING. assigns the proper mod code, tier, and value to the slot."""
        modCode = code
        modTier = tier
        #cap: the value if all 16 slots are tier 4 for one stat. This is the effective max for the stat, but should never happen.
        #expected: players will probably max 4 different attributes of the 8.
        
        
        if code == self.modEnum.MOD_ATTACK: #attack
            #cap: 1,600, expected: 400
            #scales the same as defense b/c it opposes defense. (PVP logic for PVE?)
            #12.5, 25, 50, 100
            modValue = 12.5 * 2 ** (tier - 1)
        elif code == self.modEnum.MOD_DEFENSE: #defense
            #cap: 1,600 (~93%), expected: 400 (75%)
            #values double each tier due to how defense scaling works.
            #12.5, 25, 50, 100
            modValue = 12.5 * 2 ** (tier - 1)
        elif code == self.modEnum.MOD_HP: #HP
            #should give as much benefit as armor (4x)
            #cap: 16 (+1,500 or 16x), expected: 4(+300 or 4x)
            #0.25, 0.5, 0.75, 1.0
            modValue = tier / 4.0
        elif code == self.modEnum.MOD_REGEN: #Regen
            #cap: 20/sec, expected: 5/sec
            #5/16, 10/16, 15/16, 20/16 or 5/4
            modValue = tier * 5.0 / 16.0
        elif code == self.modEnum.MOD_ABSORB: #Damage Absorbtion
            #1/2 of it is amplified by armor (@ 75% DR or 4x => this gets 3x)
            #cap: 10, expected: 2.5
            #linear to max of: 2.5/4
            modValue = tier * 2.5 / 16.0
        elif code == self.modEnum.MOD_LEECH: #Life Leech
            #cap at 10% of max hp
            #cap: 10, expected: 2.5
            #linear to cap of 2.5 / 4
            modValue = tier * 2.5 / 16.0
        elif code == self.modEnum.MOD_CRIT: #Critical Hit Chance
            #cap: 100, expected: 25
            #linear to cap of 25 / 4 (may want exponential to reduce diminishing returns)
            modValue = tier * 25.0 / 16.0
        elif code == self.modEnum.MOD_ATTACK_SPEED: #Attack Speed
            #cap: 4, expected: 1
            #linear to cap of 1 / 4
            modValue = tier / 16.0
        elif code == self.modEnum.MOD_MOVE_SPEED: #Move Speed
            #special case. HARD CAPPED. 1 slot = all you need
            #cap: 1, expected: 1
            modValue = tier / 4.0

    def upgrade(self):
        """bump this slot up a tier. Returns 0 on sucess, -1 if it fails."""
        code = self.modCode
        tier = self.modTier
        if tier < 4:
            assign_slot(self, code, tier + 1)
            return 0
        else:
            return -1

    # @ param code the mod code of the stat to get the value of
    def get_stat(self, code):
        """get the modValue for modCode <code>"""
        if modCode == code:
            return modValue
        else:
            return 0
        
    def decode_mod(self, code):
        """mod code -> string specifying the attribute"""
        #enumeration containing equipment attributes.
        #mod code of an attribute = index in enum.
        enum = ["BLANK", "ATTACK", "DEFENSE", "HP", "Regen", "Damage Absorbtion", \
                "Life Leech", "Critical Hit Chance", "Attack Speed", "Move Speed"]
        if code > -1 and code < enum.__len__():
            return enum[code]
        else:
            return "VOID"

    # @ param code the mod code of the stat
    # @ param tier the tier of the upgrade
    def get_price(self, code, tier):
        """get the price of the specified upgrade"""
        if tier > 4 or tier < 1: #invalid upgrade
            return 0
        
        price = 0
        if code == self.modEnum.MOD_DEFENSE:
            price = tier * 150
        elif code == self.modEnum.MOD_MOVE_SPEED:
            price = tier * 1000
        else:
            price = tier * 100
        return price
            
