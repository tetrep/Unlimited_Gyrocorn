import pygame, sys
from tile import *
from player import *
from turret import *

class Game(object):
    def __init__(self):
        """Initialize the game"""
        super(Game, self).__init__()
        pygame.init()
        self.clock = pygame.time.Clock()
        
        #screen initialization
        self.screenSize = (1024, 768)
        self.screen = pygame.display.set_mode( self.screenSize )
        
        self.load_assets()

        #game objects
        self.player = Player(self.imgPlayer)
        self.mapSize = [32, 32]
        self.tiles = []
        #self.turrets = []
        #self.creeps = []

        self.load_tiles()
        
    def load_assets(self):
        """pre-load all graphics and sound"""
        self.imgPlayer = pygame.image.load("Art/units/sprite-general-gabe.png").convert()
        self.imgPlayer.set_colorkey( (255, 0, 255) )
        self.imgTile = pygame.image.load("Art/tiles/tile-grass.png").convert()
        self.imgTileWall = pygame.image.load("Art/tiles/obj-wall.png").convert()

    def load_tiles(self):
        """generate a level, and store it in tiles[][]"""
        for x in range(0, self.mapSize[0]):
            self.tiles.append( [] )
            for y in range(0, self.mapSize[1]):
                tempTile = Tile(self.imgTile)
                tempTile.x = x * 24
                tempTile.y = y * 24
                if y == 4 and x == 4:
                    tempTile.blocking = True
                    tempTile.img = self.imgTileWall
                self.tiles[x].append( tempTile )
        
    def update(self):
        """Do logic/frame"""
        self.deltaT = self.clock.tick()

        self.player.update(self)
        
    def get_input(self):
        """get and handle user input"""
        #exit on esc
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_w:
                    self.player.direction[1] += -1
                if event.key == pygame.K_a:
                    self.player.direction[0] += -1
                if event.key == pygame.K_s:
                    self.player.direction[1] += 1
                if event.key == pygame.K_d:
                    self.player.direction[0] += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.direction[1] += 1
                if event.key == pygame.K_a:
                    self.player.direction[0] += 1
                if event.key == pygame.K_s:
                    self.player.direction[1] += -1
                if event.key == pygame.K_d:
                    self.player.direction[0] += -1
        
    def draw(self):
        """draw"""
        self.screen.fill( (0, 0, 0) ) #screen wipe
        #draw stuff, from back->front
        self.draw_tiles()
        self.player.draw(self.screen)
        
        #actually draw it
        pygame.display.flip()

    def draw_tiles(self):
        for x in range(0, self.tiles.__len__() ):
            for y in range(0, self.tiles[x].__len__() ):
                self.tiles[x][y].draw( self.screen ) #[ [(0,0), (0,1), ...], [(1,0),(1,1),...], ...]
        
    def main(self):
        """main game loop"""
        while True:
            self.get_input()
            self.update()
            self.draw()

g = Game()
g.main()
        
