import pygame

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
        
        #instance of game we are in
        self.game = game

    def update(self):
        """update method"""
        pass
    def draw(self):
        """draw method"""
        pass
