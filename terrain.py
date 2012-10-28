import Entity

class Terrain(object):
    def __init__ (self,engine=None,source=''):
        super(Terrain,self).__init__(self)
        self.engine = engine
                
        self.tiles = []
        
        terrainSource = open(source)
        lines = terrainSource.readlines()
        self.xSize = len(lines[0])
        self.ySize = len(lines)
        
        for x in xrange(self.xSize):
            self.tiles.append([])
            for y in xrange(self.ySize):
                #Needs to pass a rect to the Tile, but cannot calculate how big the rect should be until engine has an attribute controlling size of game area
                
                self.tiles[x].append(Tile(lines[y][x]))
                
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
            
    def create_surface(self):
        pass
            
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
    def __init__(self,rect,contains)
        self.isBlocking = False
        self.contains = contains
        
        self.rect = rect
        