import pygame

# what we need to optimize
# @xrefitem opt "Optimizations" "Optimizations List"


##   @class Creep
#    @brief this is the Creep class
#    @todo attacks, deaths, animations
class Creep(object)
    ## the constructor
    #  @param img the sprite for the creep to use
    def __init__(self, img):

        #set creep sprite
        self.img = img

        #initialize coordinates to 240,240
        self.x = self.y = 240

        #initialize our current destination to -1, -1
        self.x_next = self.y_next = -1

        #initialize rect, h/w: 24/32
        self.rect = pygame.Rect(self.x, self.y, 24, 32)

        #speed in pixels/tick
        self.x_speed = 10.0
        self.y_speed = 10.0

        #x movement, -1 to 1
        self.x_move = 0

        #y movement, -1 to 1
        self.y_move = 0

    ## the next_move function
    #  @brief sets some local variables of the Creep to indicate its next attempted move
    #  @todo not be a roomba, we dont like roombas
    def next_move()
        if self.x_move = 0:
            self.x_move = 1
        elif self.x_move = 1:
            self.x_move = -1
        elif self.x_move = -1:
            self.x_move = 0
        if self.y_move = 0:
            self.y_move = 1
        elif self.y_move = 1:
            self.y_move = -1
        elif self.y_move = -1:
            self.y_move = 0

        #set x/y next
        self.x_next = self.x + self.x_move * self.x_speed
        self.y_next = self.y + self.y_move * self.y_speed

    ## the update function
    #  @brief handles all creep operations per frame
    #  @param game the instance of the class Game that this Creep resides in
    def update(self, game):
        #set our x/y movement based on our destination
        self.next_move()

        if not check_collision(game):
            self.x = self.x_next
            self.y = self.y_next

    ## the collision detection function
    #  @brief checks for a colision
    #  @param game the instance of the class Game that this Creep resides in
    #  @opt this is horrible, and probably can be shared with players
    def check_collision(self, game):
        #loop it!
        try:
            for x_tile in range(0, game.mapSize[0]):
                for y_tile in range(0, game.mapSize[1]):
                    if game.tiles[x][y].blocking == True:
                        #are we colliding to the left?
                        if self.x_move = -1 and self.x_next <= x_tile * 24:
                            #are we colliding up?
                            if self.y_move = -1 and self.y_next <= y_tile * 24:
                                raise iceberg()
                            #are we colliding down?
                            elif self.y_move = 1 and self.y_next >= y_tile * 24 - 24:
                                raise iceberg()
                            #are we colliding across?
                            elif self.y_move = 0 and (self.y_next <= y_tile * 24 and self.y_next >= y_tile * 24 - 24:
                                raise iceberg()
                        #are we colliding to the right?
                        elif self.x_move = 1 and self.x_next >= x_tile * 24 - 24:
                            #are we colliding up?
                            if self.y_move = -1 and self.y_next <= y_tile * 24:
                                raise iceberg()
                            #are we colliding down?
                            elif self.y_move = 1 and self.y_next >= y_tile * 24 - 24:
                                raise iceberg()
                            #are we colliding across?
                            elif self.y_move = 0 and (self.y_next <= y_tile * 24 and self.y_next >= y_tile * 24 - 24:
                                raise iceberg()
                        #are we not moving in the x direction?
                        elif self.x_move = 0
                            #are we colliding up?
                            if self.y_move = -1 and self.y_next <= y_tile * 24:
                                raise iceberg()
                            #are we colliding down?
                            elif self.y_move = 1 and self.y_next >= y_tile * 24 - 24:
                                raise iceberg()
        except iceberg:
            return True
