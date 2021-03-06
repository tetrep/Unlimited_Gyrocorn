import pygame
from threading import Lock

class Tile(object):
    #  @param img a reference to a pygame.Surface containing the image to be used for draw calls.
    # @ param rect The tile's rect (i.e. it's location in the Terrain)
    def __init__(self, img, rect=pygame.Rect(0,0,0,0)):
        """initialize tile"""
        self.img = img
        
        self.rect = rect
        
        self.x = rect.left
        self.y = rect.right

        self.blocking = False

        self.creep_value = 999

    ## draws the tile to the screen
    # @param g The game engine(WHO NAMED THIS g?!!?)
    def draw(self, g):
        """draw the tile to the screen"""
        temp = pygame.Surface( (24, 24) )
        temp.blit(self.img, pygame.Rect(0, 0, 24, 24) )
        offset = [-1 *( g.focus[0] - g.view[0] / 2 ), -1 * ( g.focus[1] - g.view[1] / 2 ) ]
        #zoom logic
        temp = pygame.transform.scale(temp, ( (int)(24 * g.zoom), (int)(24 * g.zoom) ))
        g.screen.blit( temp, pygame.Rect( (int)(self.x * g.zoom) + offset[0], (int)(self.y * g.zoom) + offset[1], (int)(24 * g.zoom), (int)(24 * g.zoom) ) )
        #g.screen.blit( self.img, pygame.Rect( self.x, self.y, 24, 24 ) )

        
    ## the effective_value function
    #  @brief returns the creep_value and any modifiers
    def effective_value(self):
      if self.blocking:
          return self.creep_value + 999
      else:
          return self.creep_value
    
    ## Sets the tile to either block or not block creeps and players
    def setBlocking(self, blocking_value):
        self.blocking = blocking_value
