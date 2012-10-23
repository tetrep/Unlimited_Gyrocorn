class SuperClass(object):
    def __init__(self, x, y, game):
        """Initialize the superclass object"""
        #super(SuperClass, self).__init__()

        #where we are
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 24, 32)

        #where we want to move to next
        self.x_next = x
        self.y_next = y
        self.rect_next = self.rect
        
        #instance of game we are in
        self.game = game

    def update(self):
        """update method"""
        pass
    def draw(self):
        """draw method"""
        pass

    ## the collision_check function
    #  @brief checks if self.rect_next collides with any rects that block
    #  @todo is this effecient enough? it might be too slow for lots of collisions
    def collision_check(self):
        #iterate over all blocking objects
        for blocker in blockers:
            #are we overlapping?
            if self.rect_next.colliderect(blocker.get_rect()):
                return true
        #nothing is in the way
        return false
