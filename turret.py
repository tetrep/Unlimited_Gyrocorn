import pygame

class Turret(object):
    def __init__(self, img):
        """initialize the turret"""
        self.img = img
        
        self.x = 0
        self.y = 0
        
    def update(self, deltaT):
        """update the turret (per frame)"""
        pass
    
    def draw(self, screen):
        """draw the player to the screen"""
        screen.blit(self.img, pygame.Rect(self.x, self.y, 0, 0), pygame.Rect(0, 0, 0, 0) )
