import pygame

from superclass import *
from weapon import *

import sys
import math

##   @class Creep
#    @brief this is the Creep class
class Creep(SuperClass):
    ## the constructor
    #  @param img the sprite for the creep to use
    #  @param x the x position the creep occupies
    #  @param y the y position the creep occupies
    #  @param game the instance of the game this Creep is in
    #  @param ctype a tuple of creep attributes, optional
    def __init__(self, img, x, y, game, ctype = (100, 100, 100, 24)):
        #initialze super class variables
        super(Creep, self).__init__(x, y, game, *ctype)

        #set creep sprite
        self.img = img

        #set current and destination tile positions
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24
        self.x_tile_next = self.x_tile
        self.y_tile_next = self.y_tile

        #vector we want to move along
        self.x_move = 0.0
        self.y_move = 0.0
        self.x_real = self.x
        self.y_real = self.y
        self.m = 0

        #our weapon
        self.weapon = Weapon()

        #append our needed functions
        self.update_functions.append((0, self.update_tile))
        self.update_functions.append((10, self.next_move))
        self.update_functions.append((20, self.move))
        self.update_functions.append((30, self.attack))

        #sort our wonderful list so they occur in order
        self.update_functions = sorted(self.update_functions, key=lambda function_tuple: function_tuple[0])


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
        if self.y_tile > 0 and self.game.tiles[self.x_tile][self.y_tile-1].effective_value() <= self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "up"
            self.x_tile_next = self.x_tile
            self.y_tile_next = self.y_tile - 1
        #look down [][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.game.tiles[self.x_tile][self.y_tile+1].effective_value() <= self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "down"
            self.x_tile_next = self.x_tile
            self.y_tile_next = self.y_tile + 1
        #look left [-1][]
        if self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile].effective_value() <= self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile
        #look right [+1][]
        if self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile].effective_value() <= self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "right"
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile
        #look up-left [-1][-1]
        if self.y_tile > 0 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile-1].effective_value() <= self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and not (self.game.tiles[self.x_tile][self.y_tile-1].blocking or self.game.tiles[self.x_tile-1][self.y_tile].blocking):
            #print "up-left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile - 1
        #look up-right [+1][-1]
        if self.y_tile > 0 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile-1].effective_value() <= self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and not (self.game.tiles[self.x_tile][self.y_tile-1].blocking or self.game.tiles[self.x_tile+1][self.y_tile].blocking):
            #print "up-right"
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile - 1
        #look down-left [-1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile+1].effective_value() <= self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and not (self.game.tiles[self.x_tile][self.y_tile+1].blocking or self.game.tiles[self.x_tile-1][self.y_tile].blocking):
            #print "down-left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile + 1
        #look down-right [+1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile+1].effective_value() <= self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value() and not (self.game.tiles[self.x_tile][self.y_tile+1].blocking or self.game.tiles[self.x_tile+1][self.y_tile].blocking):
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
        self.x_real += (self.x_move * self.speed) * self.game.deltaT / 1000
        self.y_real += (self.y_move * self.speed) * self.game.deltaT / 1000

        #print '(', self.x_real, ',', self.y_real, ')'

        #update our rect
        self.rect.move_ip(int(self.x_real) - self.x, int(self.y_real) - self.y)

        #update our x/y positon
        self.x = int(self.x_real)
        self.y = int(self.y_real)

        #print '(', self.x_tile_next, ',', self.y_tile_next, ')', '(', self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value(), ',', self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value(), ')'

    ## the reap function
    #  @brief handles what to do if we are dead
    def reap(self):
        #are we dead?
        if self.health <= 0:
            self.game.give_xp(self.xp_value)
            self.game.give_gold(self.gold_value)
            return True
        #we're not dead yet
        else:
            return False

    ## the update tile
    #  @brief calculates the current tile we occupy
    def update_tile(self):
        #update our current tile position
        self.x_tile = self.rect.centerx // 24
        self.y_tile = self.rect.centery // 24

        #have we arrived?
        if (self.x_tile, self.y_tile) == self.game.tiles.target:
            self.game.creep_won()
            self.health = 0

        #print '(', self.x_tile, ',', self.y_tile, ')'
        #print '(', self.rect.centerx, ',', self.rect.centery, ')'

    ## the draw function
    #  @brief draws the creep to the screen, called once per frame
    #  @todo this should just be inherited
    def draw(self):
        #blit it!
        #zoom logic
        pos = self.game.convertGamePixelsToZoomCoorinates( (self.rect.x, self.rect.y) )
        temp = pygame.Surface( ( 24, 32 ) )
        temp.fill( (255, 0, 255) )
        temp.set_colorkey( (255, 0, 255) )
        temp.blit( self.img, pygame.Rect(0, 0, 24, 32), pygame.Rect(0, 0, 24, 32) )
        temp = pygame.transform.scale(temp, ( (int)(temp.get_width() * self.game.zoom), (int)(temp.get_height() * self.game.zoom) ) )
        self.game.screen.blit(temp, pygame.Rect( pos[0], pos[1], int(self.rect.width * self.game.zoom), int(self.rect.height * self.game.zoom) ) )

    ## the attack function
    #  @brief attacks all players in range
    def attack(self):
        #have we attacked too recently?
        if self.attack_wait >= self.attack_speed:
            #iterate through the players, attacking the first one that collides
            for player in self.game.players:
                if(self.rect.colliderect(player.rect)):
                    #so we don't attack too quickly
                    self.attack_wait = 0
                    #attack the player with our weapon
                    self.weapon.attack(player)
                    break
        #wait for attack_speed ms before we can attack again
        else:
            self.attack_wait += self.game.deltaT

    ## the print neighbors function
    #  @brief prints the effective value of the current and neighboring tiles
    def print_neighbors(self):
        print self.game.tiles[self.x_tile-1][self.y_tile-1].effective_value(), ' ', self.game.tiles[self.x_tile][self.y_tile-1].effective_value(), ' ', self.game.tiles[self.x_tile+1][self.y_tile-1].effective_value()
        print self.game.tiles[self.x_tile-1][self.y_tile].effective_value(), ' ', self.game.tiles[self.x_tile][self.y_tile].effective_value(), ' ', self.game.tiles[self.x_tile+1][self.y_tile].effective_value()
        print self.game.tiles[self.x_tile-1][self.y_tile+1].effective_value(), ' ', self.game.tiles[self.x_tile][self.y_tile+1].effective_value(), ' ', self.game.tiles[self.x_tile+1][self.y_tile+1].effective_value()
        print "============"
