import Entity

class Terrain(object):
    def __init__ (self,engine=None):
        super(Terrain,self).__init__(self)
        self.items = []
        self.engine = engine
        
    def update(self):
        for item in self.items:
            if item.rect.colliderect(self.engine.get_attribute('window').get_rect()):
                item.update()
        
        self.items = [item for item in self.items if item.rect.colliderect(self.engine.get_attribute('window').get_rect())]
            
    def draw(self):
        for item in self.items:
            item.draw()
            
    def __getitem__(self, key):
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.items):
            raise IndexError
        return self.items[key]
        
    def __setitem__(self, key, value):
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.items):
            raise IndexError
        self.items[key]=values
        
    def __delitem__(self, key):
        if not isinstance(key,int):
            raise TypeError
        if key > len(self.items):
            raise IndexError
        del(self.items[key])
        
    def __len__(self):
        return len(self.items)
        
    def append (self,value):
        self.items.append(value)
    
    def remove(self,value):
        if value in self.items:
            self.items.remove(value)
        
    def __iter__(self):
        return self.items.__iter__()