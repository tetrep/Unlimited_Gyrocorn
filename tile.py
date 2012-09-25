import pygame

class Tile(object):
    def __init__(self, img):
        """initialize tile"""
        self.img = img
        
        self.x = 0
        self.y = 0

        self.blocking = False
        
    def draw(self, screen):
        """draw the tile to the screen"""
        screen.blit( self.img, pygame.Rect( self.x, self.y, 24, 24 ) )
