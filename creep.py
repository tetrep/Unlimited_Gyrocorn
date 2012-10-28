import pygame
from superclass import *
from node import *

##   @class Creep
#    @brief this is the Creep class
#    @todo attacks, deaths, animations
class Creep(SuperClass, Node):
    ## the constructor
    #  @param img the sprite for the creep to use
    #  @param game the instance of the game this Creep is in
    def __init__(self, img, number, x, y, game):
        #get x/y/rect set up
        super(Creep, self).__init__(x, y, game)

        #linked list setup
        #have to do this manually :(
        Node.__init__(self)

        #remember the game
        self.game = game

        #set creep sprite
        self.img = img

        #initialize coordinates to 240,240
        #self.x = self.y = 240

        #initialize our current destination to -1, -1
        #self.x_next = self.y_next = -1

        #initialize rect, h/w: 24/32
        #self.rect = pygame.Rect(self.x, self.y, 24, 32)

        #set current tile position
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24

        #speed in pixels/tick
        self.x_speed = 100.0
        self.y_speed = 100.0
        self.speed_mod = 1


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
    #  @todo use vectors to make it perty
    def next_move(self):
        #remember the lowest creep value
        cur_creep_value = self.game.tiles[self.x_tile][self.y_tile].creep_value

        #default next position
        self.x_move = self.y_move = 0

        #look up
        if self.y_tile > 0 and self.game.tiles[self.x_tile][self.y_tile-1].creep_value < cur_creep_value:
            cur_creep_value = self.game.tiles[self.x_tile][self.y_tile-1].creep_value
            self.y_move = -1
        #look down
        if self.y_tile < self.game.mapSize[1]-1 and self.game.tiles[self.x_tile][self.y_tile+1].creep_value < cur_creep_value:
            cur_creep_value = self.game.tiles[self.x_tile][self.y_tile+1].creep_value
            self.y_move = 1
        #look left
        if self.x_tile > 0 and self.game.tiles[self.x_tile-1][self.y_tile].creep_value < cur_creep_value:
            cur_creep_value = self.game.tiles[self.x_tile-1][self.y_tile].creep_value
            self.x_move = -1
            self.y_move = 0
        #look right
        if self.x_tile < self.game.mapSize[0]-1 and self.game.tiles[self.x_tile+1][self.y_tile].creep_value < cur_creep_value:
            cur_creep_value = self.game.tiles[self.x_tile+1][self.y_tile].creep_value
            self.x_move = 1
            self.y_move = 0

        #set x/y next
        self.x_next = self.x + self.x_move * self.x_speed * self.speed_mod * self.game.deltaT / 1000
        self.y_next = self.y + self.y_move * self.y_speed * self.speed_mod * self.game.deltaT / 1000

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
                self.game.spawn_creep(self.img, self.number, self.x, self.y-30)
                self.game.spawn_creep(self.img, self.number, self.x-30, self.y-30)

            return True
        #we're not dead yet
        else:
            return False
            

    ## the update function
    #  @brief handles all creep operations per frame
    #  @param game the instance of the class Game that this Creep resides in
    def update(self):
        #update our current tile position (can't do this before draw)
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24

        #set our x/y movement based on our destination
        self.next_move()

        self.move()

    ## the draw function
    #  @brief draws the creep to the screen, called once per frame
    #  @param screen the screen that the creep should be drawn to
    def draw(self, screen):
        #blit it!
        screen.blit(self.img, self.rect, pygame.Rect(25*2, 33 * 2, 24, 32))
