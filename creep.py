import pygame
from superclass import *
import sys

##   @class Creep
#    @brief this is the Creep class
class Creep(SuperClass):
    ## the constructor
    #  @param img the sprite for the creep to use
    #  @param number the value used to determine the creeps attributes
    #  @param x the x position the creep occupies
    #  @param y the y position the creep occupies
    #  @param game the instance of the game this Creep is in
    def __init__(self, img, x, y, type = (100, 100, 100, 100), game)
        #initialze super class variables
        super(Creep, self).__init__(x, y, type[1], type[2], type[3], type[4], game)

        #set creep sprite
        self.img = img

        #set current and destination tile positions
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24
        self.x_tile_next = self.x_tile
        self.y_tile_next = self.y_tile

        #stats
        self.defense = 100.0
        self.max_defense = 100.0
        self.absorbtion = 0.0
        self.max_aborbtion = 0.0

        self.timeBurning = -1
        self.timeChilled = -1
        self.timeShocked = -1
        self.timeParalyzed = -1
        self.burningCounter = 0
        self.damage_multiplier = 1
        
        #vector we want to move along
        self.m = 0
        self.b = 0

        #x and y are not swapped
        self.swap = False

    ## the vroom function
    #  @brief returns our calculated speed, based on various factors
    def vroom(self):
          return (self.speed * 100.0)//1000

    ## the move_vector function
    #  @brief using x/y and x/y _next for tiles, finds m and b of vector between the two tiles
    #  @todo optimize
    def move_vector(self):
        #for our charging creep
        self.m_old = self.m
        self.b_old = self.b

        #dont want to break on vertical movement, so swap x/y
        if self.x == self.x_dest:
           #set slope
           self.m = 0

        #calculate the slope
        else:
            self.m = (self.y_dest - self.y) / (self.x_dest - self.x)

        #calculate the y-intercept
        self.b = self.y + (-1 * self.m * self.x)

        #are we charging?
        if self.m_old == self.m and self.b_old == self.b:
            self.speed_mod *= 1.01
        else:
            self.speed_mod = 100.0

        """
        print "m=", self.m
        print "b=", self.b
        print "(", self.x, ",", self.y, ")"
        print "(", self.x_dest, ",", self.y_dest, ")"
        print '[', self.x_tile, ',', self.y_tile, ']'
        print '[', self.x_tile_next, ',', self.y_tile_next, ']'
        #"""

    ## the next_move function
    #  @brief look for the next ideal tile to attempt to move to
    #  @todo optimize
    def next_move(self):
        #our default next position
        self.x_tile_next = self.x_tile
        self.y_tile_next = self.y_tile

        #look up [][-1]
        if self.y_tile > 0 and self.game.tiles[self.x_tile][self.y_tile-1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "up"
            self.x_tile_next = self.x_tile
            self.y_tile_next = self.y_tile - 1
        #look down [][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.game.tiles[self.x_tile][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "down"
            self.x_tile_next = self.x_tile
            self.y_tile_next = self.y_tile + 1
        #look left [-1][]
        if self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile
        #look right [+1][]
        if self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "right"
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile
        #look up-left [-1][-1]
        if self.y_tile > 0 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile-1].creep_value < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and !(self.game.tiles[self.x_tile][self.y_tile-1].blocking or self.game.tiles[self.x_tile-1][self.y_tile].blocking):
            #print "up-left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile - 1
        #look up-right [+1][-1]
        if self.y_tile > 0 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile-1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and !(self.game.tiles[self.x_tile][self.y_tile-1].blocking or self.game.tiles[self.x_tile+1][self.y_tile].blocking):
            #print "up-right"
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile - 1
        #look down-left [-1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and !(self.game.tiles[self.x_tile][self.y_tile+1].blocking or self.game.tiles[self.x_tile-1][self.y_tile].blocking):
            #print "down-left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile + 1
        #look down-right [+1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and !(self.game.tiles[self.x_tile][self.y_tile+1].blocking or self.game.tiles[self.x_tile+1][self.y_tile].blocking):
            #print "down-right"
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile + 1


        #print "======"
        #update x/y next
        self.x_dest = self.x_tile_next * 24 + 12
        self.y_dest = self.y_tile_next * 24 + 12

        #find our line
        self.move_vector()

    ## the move function
    #  @brief handles what happens when the creep can actually move to its desired location
    def move(self):
        #do we actually want to move?
        if self.x == self.x_tile_next * 24 + 12 and self.y == self.y_tile_next * 24 + 12:
            self.x_next = self.x
            self.y_next = self.y
        #we want to move
        else:
            #calculate our next x/y coords
            self.x_next = int(self.x + self.vroom())
            self.y_next = int(self.m * self.x_next + self.b)

            #print '(', self.x_next, ',', self.y_next, ')'

            if self.swap:
                #print "unswap3"
                self.swap_xy()

            #update our rect
            self.rect.move_ip(self.x_next - self.x, self.y_next - self.y)

            #update our x/y positon
            self.x = self.x_next
            self.y = self.y_next

    ## the reap function
    #  @brief handles what to do if we are dead
    def reap(self):
        #are we dead?
        if self.health <= 0:
            return True
        #we're not dead yet
        else:
            return False

    ## the update function
    #  @brief handles all creep operations per frame
    def update(self, game):
        #update our current tile position (can't do this before draw)
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24

        super(Creep, self).checkBurning(game.deltaT)
        super(Creep, self).checkChilled(game.deltaT)
        super(Creep, self).checkShocked(game.deltaT)
        super(Creep, self).checkParalyzed(game.deltaT)
        
        #calculate where we want to move to
        self.next_move()

        #move to our destination
        self.move()

    ## the draw function
    #  @brief draws the creep to the screen, called once per frame
    #  @param screen the screen that the creep should be drawn to
    #  @todo this should just be inherited
    def draw(self, game):
        #blit it!
        game.screen.blit(self.img, self.rect, pygame.Rect(25*2, 33 * 2, 24, 32))

    ## the print_neighbors function
    #  @brief for debugging, prints the effective_values of the surrounding tiles
    def print_neighbors(self):
        x_tile = self.x_tile
        y_tile = self.y_tile
        #print up-left, and up, and up-right
        print self.game.tiles[x_tile-1][y_tile-1].effective_value(), "=", self.game.tiles[x_tile][y_tile-1].effective_value(), '=', self.game.tiles[x_tile+1][y_tile-1].effective_value()
        #print left, center, and right
        print self.game.tiles[x_tile-1][y_tile].effective_value(), "=", self.game.tiles[x_tile][y_tile].effective_value(), '=', self.game.tiles[x_tile+1][y_tile].effective_value()
        #print down-left, down, and down-right
        print self.game.tiles[x_tile-1][y_tile+1].effective_value(), "=", self.game.tiles[x_tile][y_tile+1].effective_value(), '=', self.game.tiles[x_tile+1][y_tile+1].effective_value()
        print "=========="
