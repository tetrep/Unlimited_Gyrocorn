import pygame

from tile import *


# @class Terrain
# @brief Contains the data for the terrain (grass, water, walls) that make up the gameworld. 
class Terrain(object):

    ## Constructor for the terrain object. Takes a path to the text file from which to load the terrain data
    # @param self The terrain pointer
    # @param engine The game engine (a Game object)
    # @param source String containing a path to the text file containing the terrain data
    def __init__ (self,engine=None,source=''):
        self.engine = engine
                
        self.tiles = [] # The terrain itself, a 2D collection of tiles
        
        terrainSource = open(source)
        lines = terrainSource.readlines()
        self.xSize = len(lines[0].strip()) # The number of columns in the terrain
        self.ySize = len(lines) # The number of rows in the terrains
        
        self.rockimg = pygame.image.load("Art/tiles/rockmap.png") # The 16x1 collection of 24x24 tile imgs for use when the tile is a wall. 
        self.grassimg = pygame.image.load("Art/tiles/tile-grass.png").convert() # The single img for a grasstile
        self.waterimg = pygame.image.load("Art/tiles/tile-water.png").convert() # The single tile for a watertile
        
        #self.tileSize = pygame.Rect(0,0,self.engine.screen.get_width()/self.xSize,self.engine.screen.get_height()/self.ySize) # A rect that defines how big an individual tile on is in the gameworld
        self.tileSize = pygame.Rect(0,0,24,24)# A rect that defines how big an individual tile on is in the gameworld
        
        self.spawns = []    # A list containing the places that creeps will spawn
        self.target = (self.xSize-2, self.ySize-2)
        
        for x in xrange(self.xSize):
            self.tiles.append([])
            for y in xrange(self.ySize):
                offset=0
                if lines[y][x] == 'o':
                    if y!=0 and lines[y-1][x]=='o':
                        offset+=1
                    elif y==0:
                        offset+=1
                    if x<self.xSize-1 and lines[y][x+1]=='o':
                        offset+=2
                    elif x==self.xSize-1:
                        offset+=2
                    if y<self.ySize-1 and lines[y+1][x]=='o':
                        offset+=4
                    elif y==self.xSize-1:
                        offset+=4
                    if lines [y][x-1]=='o':
                        offset+=8
                    elif x==0:
                        offset+=8
                        
                    img = pygame.transform.scale(self.rockimg.subsurface((offset*24,0,24,24)),(self.tileSize.width,self.tileSize.height))
                    
                    
                    blocking = True
                    
                elif lines[y][x] == 'w':
                    img = self.waterimg
                    blocking=True
                elif lines [y][x] == 's':
                    self.spawns.append((x,y))
                    img=self.grassimg
                    blocking = False
                elif lines[y][x] == 't':
                    self.target = (x,y)
                    img=self.grassimg
                    blocking = False
                else:
                    img=self.grassimg
                    blocking = False
                    
                self.tiles[x].append(Tile(img,self.tileSize.move(x*self.tileSize.width,y*self.tileSize.height)))
                self.tiles[x][y].blocking = blocking
        self.create_img()
        
    ## Called once per frame to update the tiles, for now doesn't do much
    # @param self The Terrain object
    # @param deltat How much time has passed since the last frame, scales the changes that will occur
    def update(self, deltat):
        for column in self.tiles:
            for item in column:
                item.update(deltat)
            
    ## Draws the terrain to the screen.
    def draw(self):
        #Draws the img created at the beginning
        #for column in self.tiles:
        #    for item in column:
        #        item.draw(self.engine)
        
        self.engine.screen.blit(self.img,(0,0))
           
    ## Returns the tile at the given x and y location
    # @param self The Terrain object
    # @param refX The x location
    # @param refY The y location
    def get_tile_at(self,refX,refY):
        x = refX/self.tileSize.width
        y = refY/self.tileSize.height
        
        if x >= len(self.tiles):
            return None
        elif x < 0:
            return None
        if y >= len(self.tiles):
            return None
        elif y < 0:
            return None
        
        return self.tiles[x][y]
        
    ## Creates the surface object that the Terrain will blit to the screen
    # @param self The Terrain object
    def create_img(self):
        self.img = pygame.Surface((self.engine.screen.get_width(),self.engine.screen.get_height()))
        for column in self.tiles:
            for item in column:
                self.img.blit(item.img,item.rect)
                
    ## Returns the list of spawn locations (where creeps will spawn)
    def get_spawn_locations(self):
        return self.spawns
        
    ## Returns the target (where creeps will go to)
    def get_target(self):
        return self.target
            
    ## Overloads the getitem function so that the terrain can be accessed by []
    def __getitem__(self, key):
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.tiles):
            raise IndexError
        return self.tiles[key]
        
    ## Overloads the getitem function so that the terrain can be set by []
    def __setitem__(self, key, value):
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.tiles):
            raise IndexError
        self.tiles[key]=values
        
    ## Allows del() to work on terrain
    def __delitem__(self, key):
        
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.tiles):
            raise IndexError
        del(self.tiles[key])
        
    ## Allows len() to work on the terrain, allowing things like iteration
    def __len__(self):
        return len(self.tiles)
        
    ## Allows things to be appended to the terrain. Not strictly useful, but terrain should emulate a list at this point 
    def append (self,value):
        self.tiles.append(value)
    
    ## Allows things to be removed from the terrain. Not strictly useful, but terrain should emulate a list at this point
    def remove(self,value):
        if value in self.tiles:
            self.tiles.remove(value)
        
    ## Allows iteration over the terrain
    def __iter__(self):
        return self.tiles.__iter__()
        
# class Tile (object):
    # def __init__(self,img,rect,contains,blocking):
        # if contains is not None:
            # self.contains = contains
        # else:
            # self.contains = []
        
        # self.blocking=blocking
        # self.rect = rect
        # self.img=img
        
    # def draw(self,displayimg):
        # displayimg.blit(self.img,self.rect)