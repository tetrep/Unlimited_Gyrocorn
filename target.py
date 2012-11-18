import pygame

# @ brief a class used to create bullets headed toward a player-specified destination
class Target(object):
    def __init__(self, x, y):
        """initialize the target"""
        super(Target, self).__init__()
        self.rect = pygame.Rect( x, y, 1, 1)
