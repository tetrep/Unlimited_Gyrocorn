class Skill(object):
    def __init__(self):
        """Initialize the skill"""
        super(Skill, self).__init__()
        self.skillKey = -1
        self.skillAttr = 0
        self.skillCost = 0
        self.active = False #for auras
