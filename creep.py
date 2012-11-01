import pygame
from superclass import *
from node import *
import sys

##   @class Creep
#    @brief this is the Creep class
#    @todo attacks, deaths, animations
class Creep(SuperClass):
    ## the constructor
    #  @param img the sprite for the creep to use
    #  @param number the value used to determine the creeps attributes
    #  @param x the x position the creep occupies
    #  @param y the y position the creep occupies
    #  @param game the instance of the game this Creep is in
    def __init__(self, img, number, x, y, game):
        #get x/y/rect set up
        super(Creep, self).__init__(x, y, 1, 1, 10, game)

        #remember the game
        self.game = game

        #set creep sprite
        self.img = img

        #set current and destination tile positions
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24
        self.x_tile_next = self.x_tile
        self.y_tile_next = self.y_tile

        #speed
        # @todo we really shouldn't reach into game like this!
        self.speed = 10.0
        self.speed_mod = 100.0

        #vector we want to move along
        self.m = 0
        self.b = 0

        #initialize our unique attributes
        self.weapons = []
        self.number = number
        self.init_attributes()

        #x and y are not swapped
        self.swap = False


    ## the init_attributes function
    #  @brief generates a class of creep based on the give number
    #  @param number determines what type of creep to generate
    #  @todo add more creeps!
    def init_attributes(self):
        #generic and boring
        if self.number == 0:
            self.health = 5
        elif self.number == 1 or self.number == 666:
            self.health = 40
        elif self.number == 2:
            self.health = 10
        else:
            self.health = 25

    ## the vroom function
    #  @brief returns our calculated speed, based on various factors
    def vroom(self):
        if self.number != 666:
          return (self.speed * self.speed_mod)//1000
        else:
          return (self.speed * 100.0)//1000

    ## the swap_xy function
    #  @brief swaps x and y so we can move vertically
    def swap_xy(self):
        #swap x/y
        self.temp = self.x
        self.x = self.y
        self.y = self.temp

        #swap x/y _dest
        self.temp = self.x_dest
        self.x_dest = self.y_dest
        self.y_dest = self.temp

        #toggle swap bool
        if self.swap:
            print "unswap2"
            self.swap = False
        else:
            print "swap2"
            self.swap = True

    ## the move_vector function
    #  @brief using x/y and x/y _next for tiles, finds m and b of vector between the two tiles
    #  @todo optimize
    def move_vector(self):
        #for our charging creep
        self.m_old = self.m
        self.b_old = self.b

        #dont want to break on vertical movement, so swap x/y
        if self.x == self.x_dest:
           #swap x and y
           print "swap"
           self.swap_xy()

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

    ## the attack function
    #  @brief use each weapon on its given tarets
    def attack(self):
        for weapon in weapons:
            weapon.attack()

    ## the find_targets function
    #  @brief finds targets for each weapon
    def find_targets(self):
        for weapon in weapons:
            weapon.find_targets()

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
        if self.y_tile > 0 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile-1].creep_value < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "up-left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile - 1
        #look up-right [+1][-1]
        if self.y_tile > 0 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile-1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "up-right"
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile - 1
        #look down-left [-1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            #print "down-left"
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile + 1
        #look down-right [+1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
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

            if self.swap:
                print "unswap"
                self.swap_xy()

            sys.exit()

        #we want to move
        else:
            if self.number != 666:
                #self.print_neighbors()
                pass

            #calculate our next x/y coords
            self.x_next = int(self.x + self.vroom())
            self.y_next = int(self.m * self.x_next + self.b)

            print '(', self.x_next, ',', self.y_next, ')'

            if self.swap:
                print "unswap3"
                self.swap_xy()

            #update our rect
            self.rect.move_ip(self.x_next - self.x, self.y_next - self.y)

            #update our x/y positon
            self.x = self.x_next
            self.y = self.y_next

    ## the reduce_damage function
    #  @brief the function that will take all our defenses into account, and reduce damage accordingly
    #  @todo should be replaced, just a placeholder for now
    def reduce_damage(self, damage):
        return damage

    ## the receive_damage function
    #  @brief the function to be called by whatever wants to hurt our poor creep
    #  @todo should be replaced, just a placeholder for now
    def receive_damage(self, damage):
        #reduce it!
        damage = self.reduce_damage(damage)

        self.health -= damage

    ## the take_damage function
    #  @brief because bitches love wrappers
    #  @todo this shouldn't be a wrapper
    def take_damage(self, damage):
        self.receive_damage(damage)

    ## the reap function
    #  @brief handles what to do if we are dead
    def reap(self):
        #are we dead?
        if self.health <= 0:
            if self.number == 666:
                #offspring!
                self.game.spawn_creep(self.img, 1, self.x, (self.y_tile-4)*24)
                self.game.spawn_creep(self.img, 1, (self.x_tile-4)*24, (self.y_tile-4)*24)
                #print "==================================================="

            return True
        #we're not dead yet
        else:
            return False
            

    ## the update function
    #  @brief handles all creep operations per frame
    def update(self):
        #update our current tile position (can't do this before draw)
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24

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
