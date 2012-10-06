import pygame

## @class CreepPath
#  @brief this class controls the path the creeps will follow
#  @todo figure out how the path can change and adapt the optimal one
class CreepPath(object):
    ## the constructor
    #  @param source a tuple of the x/y coordinates of the destination tile
    #  @brief sets the goal of the creeps
    def __init__(self, source):
        #where we want to go, the goal
        self.source = source

    ## the find path function
    #  @brief gives all the tiles values, so creeps know where to go, lower is better
    #  @param game and instance of the game this class is in
    def find_path(self, game):
        #start at the beginning
        x, y = self.source
        #recurse!
        self.path_recursion(x, y, 0, game)

    ## the path recursion function
    #  @brief starting at the source, it flows outward giving higher values to tiles
    #  @param x the x coordinate of the tile to be inspected
    #  @param y the y coordinate of the tile to be inspected
    #  @param value the value we want to attempt to apply to the tile
    #  @param game the instance of the game where the tiles we want to inspect are
    def path_recursion(self, x, y, value, game):
        #have we found a shorter path?
        if value < 50 and value < game.tiles[x][y].creep_value:
            #update tile to have shorter path
            game.tiles[x][y].creep_value = value

            #check up
            if y > 0:
                self.path_recursion(x, y-1, value+1, game)
            #check right
            if x < 31:
                self.path_recursion(x+1, y, value+1, game)
            #check down
            if y < 31:
                self.path_recursion(x, y+1, value+1, game)
            #check left
            if x > 0:
                self.path_recursion(x-1, y, value+1, game)
