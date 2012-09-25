import pygame

class Player(object):
    def __init__(self, img):
        """initialize player"""
        self.img = img
        
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, 24, 32)
        self.speed = 64.0 #speed in pixels/sec
        self.direction = [0, 0]
        self.collision = [False, False]

        self.frame = 0
        self.frameMax = 7
        self.frameDirection = 0
        self.frameTimer = 0
        self.frameDelay = 100 #time between frames in ms
        
    def update(self, g):
        """update the player (per frame), using data from game g"""
        #collision detection
        self.collision = [False, False]
        #Need floats to ensure no "sticking" behaviour occurs (int rounding imprecision with rects)
        self.futurex = self.x + self.speed * self.direction[0] * g.deltaT / 1000.0
        self.futurey = self.y + self.speed * self.direction[1] * g.deltaT / 1000.0
        
        #bounds
        if self.futurex < 0 or self.futurex + self.rect.width > g.mapSize[0] * 24:
            #cannot move in x
            self.collision[0] = True
        if self.futurey < 0 or self.futurey + self.rect.height > g.mapSize[1] * 24:
            #cannot move in y
            self.collision[1] = True
            
        #tile collision (brute force now, OPTIMIZE THIS LATER)
        for x in range(0, g.mapSize[0]):
            for y in range(0, g.mapSize[1]):
                if g.tiles[x][y].blocking == True:
                    #test if you would be in them (24 x 24 area, cut off head top)
                    if self.futurex >= x * 24 and self.futurex <= x * 24 + 24 or \
                    self.futurex + 24 >= x * 24 and self.futurex + 24 <= x * 24 + 24:
                        if self.futurey + 8 >= y * 24 and self.futurey + 8 <= y * 24 + 24 or \
                        self.futurey + 24 + 8 >= y * 24 and self.futurey + 24 + 8 <= y * 24 + 24:
                            self.collision[0] = True
                            self.collision[1] = True
                    
            
        #move (or don't)
        if self.collision[0] == False:
            self.x += self.speed * self.direction[0] * g.deltaT / 1000.0
            self.rect.move_ip( (int)(self.x - self.rect.x), 0)
        if self.collision[1] == False:
            self.y += self.speed * self.direction[1] * g.deltaT / 1000.0
            self.rect.move_ip( 0, (int)(self.y - self.rect.y) )
        
        #parse direction
        if self.direction[0] == 1:
            self.frameDirection = 1
        elif self.direction[0] == -1:
            self.frameDirection = 3
        if self.direction[1] == 1:
            self.frameDirection = 0
        elif self.direction[1] == -1:
            self.frameDirection = 2
            
        #animate
        if self.direction != [0, 0]: #player is moving
            self.frameTimer += g.deltaT
            if self.frameTimer > self.frameDelay:
                self.frameTimer = 0
                self.frame += 1
            if self.frame > self.frameMax:
                self.frame = 0
        else: #player is idle
            self.frame = 0
    def draw(self, screen):
        """draw the player to the screen"""
        screen.blit(self.img, pygame.Rect(self.x, self.y, 24, 32), pygame.Rect(25 * self.frameDirection, 33 * self.frame, 24, 32) )
