import pygame
import Queue
import threading
import sys

## @class CreepPath
#  @brief this class controls the path the creeps will follow
#  @todo figure out how the path can change and adapt the optimal one
class CreepPath(object):
    ## the constructor
    #  @brief sets the goal of the creeps
    #  @param source a tuple of the x/y coordinates of the destination tile
    #  @param num_threads the number of threads to use to find the path
    #  @param game the instance of the game this path is in
    def __init__(self, source, num_threads, game):
        #where we want to go, the goal
        self.source = source

        #our game
        self.game = game

        #the queue of tiles to check and values to give them
        self.queue = Queue.Queue(0)

        t1 = threading.Thread(target=self.path_queue)
        t1.daemon = True
        t1.start()

        self.pathed = False

    ## the reset path function
    #  @brief resets creep_value of all the tiles
    def reset_path(self):
        for y2 in range(0, self.game.mapSize[0]):
            for x2 in range(0, self.game.mapSize[1]):
                self.game.tiles[x2][y2].creep_value = 999

        self.pathed = False

    ## the find path function
    #  @brief gives all the tiles values, so creeps know where to go, lower is better
    def find_path(self):
        #self.reset_path()

        #recurse!
        #self.path_recursion(0, self.game)

        """
        t1 = threading.Thread(target=self.path_queue)
        t1.daemon = True
        t1.start()

        t2 = threading.Thread(target=self.path_queue)
        t2.daemon = True
        t2.start()
        #"""

        #start the queue
        self.queue.put((self.source[0], self.source[1], 0))

        self.queue.join()

        self.pathed = True

        """
        temp = ""
        temp2 = 0
        for y2 in range(0, self.game.mapSize[0]):
            for x2 in range(0, self.game.mapSize[1]):
                temp += str(self.game.tiles[x2][y2].effective_value()) + " "
                temp2 += self.game.tiles[x2][y2].effective_value()
            print temp
            temp = ""
        print temp2

        #sys.exit()
        #"""

    ## the path_queue function
    #  @brief starting from the source, flow outwards with threads to find the shortest path
    #  @todo optimize
    def path_queue(self):
        while True:
            info = self.queue.get()

            #process the tile
            self.process_tile(info[0], info[1], info[2])

            #we're done
            self.queue.task_done()

    ## the process_tile function
    #  @brief replaces the given tiles creep_value with value, and then check its neighbors
    #  @param x the x coordinate of the tile
    #  @param y the y coordinate of the tile
    #  @param value the value we want to replace creep_value with
    #  @todo optimize with tile reference instead of coords
    def process_tile(self, x, y, value):

        #we've found a shorter path, update
        tile = self.game.tiles[x][y]
        if value < tile.creep_value:
            tile.creep_value = value
        #if value < self.game.tiles[x][y].creep_value:
            #self.game.tiles[x][y].creep_value = value


            #ev = self.game.tiles[x][y].effective_value()
            ev = tile.effective_value()

            #check up-left
            if y > 0 and x > 0 and ev + 1.4 < self.game.tiles[x-1][y-1].creep_value:
                self.queue.put((x-1, y-1, ev+1.4))
            #check up
            if y > 0 and ev + 1 < self.game.tiles[x][y-1].creep_value:
                self.queue.put((x, y-1, ev+1))
            #check up-right
            if y > 0 and x+1 < self.game.mapSize[0] and ev + 1.4 < self.game.tiles[x+1][y-1].creep_value:
                self.queue.put((x+1, y-1, ev+1.4))
            #check right
            if x+1 < self.game.mapSize[0] and ev + 1 < self.game.tiles[x+1][y].creep_value:
                self.queue.put((x+1, y, ev+1))
            #check right-down
            if x+1 < self.game.mapSize[0] and y+1 < self.game.mapSize[1] and ev + 1.4 < self.game.tiles[x+1][y+1].creep_value:
                self.queue.put((x+1, y+1, ev+1.4))
            #check down
            if y+1 < self.game.mapSize[1] and ev + 1 < self.game.tiles[x][y+1].creep_value:
                self.queue.put((x, y+1, ev+1))
            #check down-left
            if y+1 < self.game.mapSize[1] and x > 0 and ev + 1.4 < self.game.tiles[x-1][y+1].creep_value:
                self.queue.put((x-1, y+1, ev+1.4))
            #check left
            if x > 0 and ev + 1 < self.game.tiles[x-1][y].creep_value:
                self.queue.put((x-1, y, ev+1))

"""
    ## the path_recursion function
    #  @brief starting at the source, it flows outward giving higher values to tiles
    #  @param x the x coordinate of the tile to be inspected
    #  @param y the y coordinate of the tile to be inspected
    #  @param value the value we want to attempt to apply to the tile
    #  @param game the instance of the game where the tiles we want to inspect are
    #  @todo this is broken, recursion does not terminate normally, work around not ideal
    def path_recursion(self, x, y, value, game):
        #have we found a shorter path?
        if value < game.tiles[x][y].creep_value:
            #check
            #print value, " < ", game.tiles[x][y].creep_value
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
            #check upper-left
            if x > 0 and y > 0:
                self.path_recursion(x-1, y-1, value+1.4, game)
            #check the upper-right
            if x < 31 and y > 0:
                self.path_recursion(x+1, y-1, value+1.4, game)
            #check the bottom-right
            if x < 31 and y < 31:
                self.path_recursion(x+1, y+1, value+1.4, game)
            #check the bottom-left
            if x > 0 and y < 31:
                self.path_recursion(x-1, y+1, value+1.4, game)
"""
