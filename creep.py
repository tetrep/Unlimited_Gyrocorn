import pygame
from superclass import *
import sys
import math

##   @class Creep
#    @brief this is the Creep class
class Creep(SuperClass):
    ## the constructor
    #  @param img the sprite for the creep to use
    #  @param number the value used to determine the creeps attributes
    #  @param x the x position the creep occupies
    #  @param y the y position the creep occupies
    #  @param game the instance of the game this Creep is in
    def __init__(self, img, x, y, game, ctype = (100, 100, 100, 100)):
        #initialze super class variables
        super(Creep, self).__init__(x, y, game, *ctype)

        #set creep sprite
        self.img = img

        #set current and destination tile positions
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24
        self.x_tile_next = self.x_tile
        self.y_tile_next = self.y_tile

        self.timeBurning = -1
        self.timeChilled = -1
        self.timeShocked = -1
        self.timeParalyzed = -1
        self.burningCounter = 0
        self.damage_multiplier = 1
        
        #vector we want to move along
        self.x_move = 0.0
        self.y_move = 0.0
        self.x_real = self.x
        self.y_real = self.y
        self.m = 0

        #x and y are not swapped
        self.swap = False

    ## the vroom function
    #  @brief returns our calculated speed, based on various factors
    def vroom(self):
          return self.speed

    ## the move_vector function
    #  @brief using x/y and x/y _next for tiles, finds m and b of vector between the two tiles
    #  @todo optimize
    def move_vector(self):
        #horizontal?
        if self.x_real == self.x_dest:
            self.x_move = 0
            #up by default
            self.y_move = 1
            #whoops, we need down
            if(self.y_dest < self.y_real):
                self.y_move = -1
                #negative safely unreald slope
                self.m = (-999,1)
            #positive safely unreal slope
            else:
                self.m = (999,1)

        #we have vertical movement, find slope
        else:
            self.m = ((self.y_dest - self.y_real), (self.x_dest - self.x_real))

        self.y_move = self.m[0]/(abs(self.m[0])+abs(self.m[1]))
        self.x_move = 1 - self.y_move

        #make sure the sign is correct
        self.y_move = math.copysign(self.y_move, self.m[0])
        self.x_move = math.copysign(self.x_move, self.m[1])

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
        if self.y_tile > 0 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile-1].creep_value < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and not (self.game.tiles[self.x_tile][self.y_tile-1].blocking or self.game.tiles[self.x_tile-1][self.y_tile].blocking):
            #print "up-left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile - 1
        #look up-right [+1][-1]
        if self.y_tile > 0 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile-1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and not (self.game.tiles[self.x_tile][self.y_tile-1].blocking or self.game.tiles[self.x_tile+1][self.y_tile].blocking):
            #print "up-right"
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile - 1
        #look down-left [-1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and not (self.game.tiles[self.x_tile][self.y_tile+1].blocking or self.game.tiles[self.x_tile-1][self.y_tile].blocking):
            #print "down-left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile + 1
        #look down-right [+1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and not (self.game.tiles[self.x_tile][self.y_tile+1].blocking or self.game.tiles[self.x_tile+1][self.y_tile].blocking):
            #print "down-right"
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile + 1

        #update x/y next
        self.x_dest = self.x_tile_next * 24 + 12
        self.y_dest = self.y_tile_next * 24 + 12

        """
        print self.x_tile, ',', self.y_tile
        print self.x_tile_next, ',', self.y_tile_next
        print "====="
        #"""

        #find our line
        self.move_vector()

    ## the move function
    #  @brief handles what happens when the creep can actually move to its desired location
    def move(self):
        #calculate our next x/y coords
        self.x_real += (self.x_move * self.vroom())
        self.y_real += (self.y_move * self.vroom())

        #print '(', self.x_real, ',', self.y_real, ')'

        #update our rect
        self.rect.move_ip(int(self.x_real) - self.x, int(self.y_real) - self.y)

        #update our x/y positon
        self.x = int(self.x_real)
        self.y = int(self.y_real)

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
