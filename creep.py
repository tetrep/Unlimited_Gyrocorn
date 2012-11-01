import pygame
from superclass import *
from node import *

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
        self.speed = 100 * self.game.deltaT / 1000
        self.speed_mod = 1

        #vector we want to move along
        self.m = 0
        self.b = 0

        #initialize our unique attributes
        self.weapons = []
        self.number = number
        self.init_attributes()


    ## the init_attributes function
    #  @brief generates a class of creep based on the give number
    #  @param number determines what type of creep to generate
    #  @todo add more creeps!
    def init_attributes(self):
        #generic and boring
        if self.number == 0:
            self.health = 5
            self.speed = 1
        elif self.number == 1 or self.number == 666:
            self.health = 40
            self.speed = 1
        elif self.number == 2:
            self.health = 10
            self.speed = 1
        else:
            self.health = 25
            self.speed = 1

    ## the move_vector function
    #  @brief using x/y and x/y _next for tiles, finds m and b of vector between the two tiles
    #  @todo optimize
    def move_vector(self):
        #find the slope
        #dont want to divide by zero
        if self.x_tile == self.x_tile_next:
            self.m = 0
        else:
            self.m = (self.y_tile_next - self.y_tile) / (self.x_tile_next - self.x_tile)

        #find the y-intercept
        self.b = self.y_tile + (-1 * self.m * self.x_tile)


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
        if self.y_tile > 0 and self.game.tiles[self.x_tile][self.y_tile-1].blocking == False and self.game.tiles[self.x_tile][self.y_tile-1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            self.x_tile_next = self.x_tile
            self.y_tile_next = self.y_tile - 1
        #look down [][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.game.tiles[self.x_tile][self.y_tile+1].blocking == False and self.game.tiles[self.x_tile][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            self.x_tile_next = self.x_tile
            self.y_tile_next = self.y_tile + 1
        #look left [-1][]
        if self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile].blocking == False and self.game.tiles[self.x_tile-1][self.y_tile].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile
        #look right [+1][]
        if self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile].blocking == False and self.game.tiles[self.x_tile+1][self.y_tile].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile
        #look up-left [-1][-1]
        if self.y_tile > 0 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile-1].blocking == False and self.game.tiles[self.x_tile-1][self.y_tile-1].creep_value < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile - 1
        #look up-right [+1][-1]
        if self.y_tile > 0 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile-1].blocking == False and self.game.tiles[self.x_tile+1][self.y_tile-1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile - 1
        #look down-left [-1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile+1].blocking == False and self.game.tiles[self.x_tile-1][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            self.x_tile_next = self.x_tile - 1
            self.y_tile_next = self.y_tile + 1
        #look down-right [+1][+1]
        if self.y_tile < self.game.mapSize[1]-1 and self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile+1].blocking == False and self.game.tiles[self.x_tile+1][self.y_tile+1].effective_value() < self.game.tiles[self.x_tile_next][self.y_tile_next].effective_value():
            self.x_tile_next = self.x_tile + 1
            self.y_tile_next = self.y_tile + 1

        #move rect to next spot
        self.rect_next = self.rect.move(int(self.x_next - self.x), int(self.y_next - self.y))

    ## the move function
    #  @brief handles what happens when the creep can actually move to its desired location
    def move(self):
        #update our rect's position
        self.rect = self.rect_next

        #update our actual position
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

    ## the reap function
    #  @brief handles what to do if we are dead
    def reap(self):
        #are we dead?
        if self.health <= 0:
            if self.number == 666:
                #offspring!
                self.game.spawn_creep(self.img, 0, self.x, self.y-30)
                self.game.spawn_creep(self.img, 0, self.x-30, self.y-30)

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

        #set our x/y movement based on our destination
        self.next_move()

        self.move_vector()

        self.move()

    ## the draw function
    #  @brief draws the creep to the screen, called once per frame
    #  @param screen the screen that the creep should be drawn to
    def draw(self, game):
        #blit it!
        game.screen.blit(self.img, self.rect, pygame.Rect(25*2, 33 * 2, 24, 32))
