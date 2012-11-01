import pygame

class Terrain(object):
    def __init__ (self,engine=None,source=''):
        self.engine = engine
                
        self.tiles = []
        
        terrainSource = open(source)
        lines = terrainSource.readlines()
        self.xSize = len(lines[0].strip())
        self.ySize = len(lines)
        
        self.rockSurface = pygame.image.load("Art/tiles/rockmap.png")
        
        self.tileSize = pygame.Rect(0,0,self.engine.screen.get_width()/self.xSize,self.engine.screen.get_height()/self.ySize)
        
        for x in xrange(self.xSize):
            self.tiles.append([])
            for y in xrange(self.ySize):
                #Needs to pass a rect to the Tile, but cannot calculate how big the rect should be until engine has an attribute controlling size of game area
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
                    surface = pygame.transform.scale(self.rockSurface.subsurface((offset*100,0,100,100)),(self.tileSize.width,self.tileSize.height))
                    
                else:
                    surface=pygame.Surface((self.tileSize.width,self.tileSize.height))
                    surface.fill((255,255,255))
                self.tiles[x].append(Tile(surface,self.tileSize.move(x*self.tileSize.width,y*self.tileSize.height),lines[y][x],False))
                
        self.create_surface()
        
    def update(self, deltat):
        #Updates all tiles in the terrain. 
        for column in self.tiles:
            for item in column:
                item.update(deltat)
            
    def draw(self):
        #Draws the surface created at the beginning
        for column in self.tiles:
            for item in column:
                item.draw()
            
            
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
            
    def __getitem__(self, key):
        #Overloads the getitem function so that the terrain can be accessed by []
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.tiles):
            raise IndexError
        return self.tiles[key]
        
    def __setitem__(self, key, value):
        #Overloads the getitem function so that the terrain can be set by []
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.tiles):
            raise IndexError
        self.tiles[key]=values
        
    def __delitem__(self, key):
        #Allows del() to work on terrain
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.tiles):
            raise IndexError
        del(self.tiles[key])
        
    def __len__(self):
        #Allows len() to work on the terrain, allowing things like iteration
        return len(self.tiles)
        
    def append (self,value):
        #Allows things to be appended to the terrain. Not strictly useful, but terrain should emulate a list at this point 
        self.tiles.append(value)
    
    def remove(self,value):
        #Allows things to be removed from the terrain. Not strictly useful, but terrain should emulate a list at this point
        if value in self.tiles:
            self.tiles.remove(value)
        
    def __iter__(self):
        #Allows iteration over the terrain
        return self.tiles.__iter__()
        
class Tile (object):
    def __init__(self,surface,rect,contains,blocking):
        if contains is not None:
            self.contains = contains
        else:
            self.contains = []
        
        self.blocking=blocking
        self.rect = rect
        self.surface=surface
        
    def draw(self,displaySurface):
        displaySurface.blit(self.surface,self.rect)