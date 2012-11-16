import pygame, sys
from tile import *
from player import *
from turret import *
from gui import *

from creep import *
from chargecreep import *
from creep_path import *

from node import *
from turretfactory import *

#  @class Game
#  @brief this class is the game engine. It manages game logic, input, and rendering.
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
        #set game mode (used for menu control)
        self.mode = 0

        #game objects
        self.players = [Player(self.imgPlayer), Player(self.imgPlayer), Player(self.imgPlayer), Player(self.imgPlayer)]
        self.playerIndex = 0
        self.player = self.players[self.playerIndex]
        self.mapSize = [32, 32]
        self.tiles = []
        self.turrets = []
        self.gui = GUI( self )

        self.creeps = []
        self.load_tiles()

        self.spawn_creep(self.imgPlayer, 240, 240)
        self.spawn_creep(self.imgPlayer, 140, 140)
        self.spawn_creep(self.imgPlayer, 140, 240)
        self.spawn_creep(self.imgPlayer, 240, 140)

        #drawing variables
        self.zoom = 2.0
        self.focus = [0, 0]     # the central point of the viewbox
        self.view = [0, 0]      # the width + height of the viewbox
        self.viewMax = [0, 0]   # the width + height of the total screen
        # all draw calls in game-space MUST use zoom and focus. GUI draws don't need to.  

        self.turretFactory = TurretFactory()
        #pos = [ (180 + (self.focus[0] - self.view[0] / 2) ) / self.zoom , (300 + (self.focus[1] - self.view[1] / 2) ) / self.zoom]
        #self.turrets.append( self.turretFactory.createTurret( self, 5, pos[0], pos[1] ) )
        
    def load_assets(self):
        """pre-load all graphics and sound"""
        self.imgPlayer = pygame.image.load("Art/units/sprite-general-gabe.png").convert()
        self.imgPlayer.set_colorkey( (255, 0, 255) )
        self.imgTile = pygame.image.load("Art/tiles/tile-grass.png").convert()
        self.imgTileWall = pygame.image.load("Art/tiles/obj-wall.png").convert()
        self.imgBasicTurret = pygame.image.load("Art/tiles/obj-guardtowertest3.png").convert()
        self.imgBasicTurret.set_colorkey( (255, 0, 255) )

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

        self.player = self.players[self.playerIndex]
        for player in self.players:
            player.update( self )
            
        self.update_view()

        #update creeps
        for creep in self.creeps:
            creep.update(self)
            #creep.receive_damage(1)
        
        for x, turret in enumerate(self.turrets):
            if turret.valid_placement == True:
                turret.update(self)
            else:
                #remove turrets that do not have valid placement
                self.turrets.pop(x)


    def update_view(self):
        """create view and focus variables (draw control) based on the screen size and zoom level."""
        #do not attempt to understand this. Your head WILL explode. Just accept that it works and don't touch it.
        #on that note, this is targeted for clean-up to make it more understandable.
        #that being said, the math involved is not intuitive.

        #set the size of the viewing area
        self.view[0] = self.screenSize[0]
        self.view[1] = self.screenSize[1]

        #set the size of the game area bounds
        self.viewMax[0] = 24 * self.mapSize[0] * self.zoom
        self.viewMax[1] = 24 * self.mapSize[1] * self.zoom

        #set the focus point, or where the screen will be centered to the player's pos.
        self.focus = [(int)(self.player.x * self.zoom), (int)(self.player.y * self.zoom)]


        #clamp the screen, so the focus shifts from player -> game area at the edges of the game area.        
        if self.focus[0] - self.view[0] / 2 < 0:
            self.focus[0] = (0 + self.view[0] / 2)
        elif self.focus[0] + self.view[0] / 2 > self.viewMax[0]:
            self.focus[0] = (self.viewMax[0] - self.view[0] / 2)

        if self.focus[1] - self.view[1] / 2 < 0:
            self.focus[1] = (0 + self.view[1] / 2)
        elif self.focus[1] + self.view[1] / 2 > self.viewMax[1]:
            self.focus[1] = (self.viewMax[1] - self.view[1] / 2)
            
                
    def get_input(self):
        """get and handle user input"""
        #exit on esc
        for event in pygame.event.get():
            #key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #exit
                    pygame.quit()
                    sys.exit()
                #PLAYER SWITCHING (Must go before movement)
                if event.key == pygame.K_i:
                    #+1
                    self.player.reset_movement()
                    self.playerIndex -= 1
                    if self.playerIndex < 0:
                        self.playerIndex = 3
                if event.key == pygame.K_o:
                    #-1
                    self.player.reset_movement()
                    self.playerIndex += 1
                    if self.playerIndex > 3:
                        self.playerIndex = 0
                #MOVEMENT
                if event.key == pygame.K_w:
                    #up
                    self.player.direction[1] += -1
                if event.key == pygame.K_a:
                    #down
                    self.player.direction[0] += -1
                if event.key == pygame.K_s:
                    #left
                    self.player.direction[1] += 1
                if event.key == pygame.K_d:
                    #right
                    self.player.direction[0] += 1
                # / MOVEMENT
                #MENUS
                if event.key == pygame.K_p:
                    #toggle player menu
                    self.gui = GUI( self )
                    self.mode = 1
                    pass

            #key released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.direction[1] += 1
                if event.key == pygame.K_a:
                    self.player.direction[0] += 1
                if event.key == pygame.K_s:
                    self.player.direction[1] += -1
                if event.key == pygame.K_d:
                    self.player.direction[0] += -1

            #mouse controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    #event.pos[0] and event.pos[1] are the mouse x,y coordinates respectively relative to the game window
                    #needs to be converted to give a mapping in game space.
                    #if   map = pos * zoom - (focus - view / 2)
                    #then pos = (map + (focus - view / 2) ) / zoom

                    pos = self.convertZoomCoordinatesToGamePixels( (event.pos[0], event.pos[1]) )

                    #self.turrets.append( Turret( self, 2, pos[0], pos[1] ) )
                    self.turrets.append( self.turretFactory.createTurret( self, 6, pos[0], pos[1] ) )

                    
                elif event.button == 4: #mouse wheel down
                    self.zoom -= .1
                    if self.zoom < 1:
                        self.zoom = 1
                        
                elif event.button == 5: #mouse wheel up
                    self.zoom += .1
                    if self.zoom > 4:
                        self.zoom = 4
        

    def reap(self):
        for x, creep in enumerate(self.creeps):
            if creep.reap():
                self.creeps.pop(x)

    def spawn_creep(self, img, x, y, type = (100, 100, 100, 100)):
        self.creeps.append(ChargeCreep(img, x, y, self, type))

    def draw(self):
        """draw"""
        self.screen.fill( (0, 0, 0) ) #screen wipe
        #draw stuff, from back->front
        self.draw_tiles()

        for player in self.players:
            player.draw( self )
        
        for turret in self.turrets:
            turret.draw( self )
        
        #actually draw it
        #pygame.display.flip()

    def draw_tiles(self):
        for x in range(0, self.tiles.__len__() ):
            for y in range(0, self.tiles[x].__len__() ):
                self.tiles[x][y].draw( self ) #[ [(0,0), (0,1), ...], [(1,0),(1,1),...], ...]

    def convertGamePixelsToZoomCoorinates(self, (x, y) ):
        #get the offset of the entire zoomed-in game subspace.
        offset = [-1 *( self.focus[0] - self.view[0] / 2 ), -1 * ( self.focus[1] - self.view[1] / 2 ) ]
        #apply the zoom factor and offset.
        return ( (int)( x * self.zoom + offset[0] ), (int)( y * self.zoom + offset[1] ) )

    def convertZoomCoordinatesToGamePixels(self, (x, y) ):
        #reverse the game->zoom conversion                
        return ( (int)( ( x + (self.focus[0] - self.view[0] / 2) ) / self.zoom ) , (int)( ( y + (self.focus[1] - self.view[1] / 2) ) / self.zoom ) )
        
    def main(self):
        """main game loop"""
        while True:
            #build mode: controls change, GUI access opens up. (clicking on GUI brings it up, changes mode?)
            #pause mode:
            #on mode change, reset direction for player? (if keep)
            #various menu modes
            if self.mode == 0: #standard game
                self.get_input()
                self.update()
                self.draw()
                pygame.display.flip()
            elif self.mode == 1:
                self.gui.get_input()
                self.gui.update()
                self.draw()
                self.gui.draw()
                pygame.display.flip()

g = Game()
g.main()
        
