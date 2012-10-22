import pygame

##   @class Creep
#    @brief this is the Creep class
#    @todo attacks, deaths, animations
class Creep(object):
    ## the constructor
    #  @param img the sprite for the creep to use
    #  @param game the instance of the game this Creep is in
    def __init__(self, img, number, game):

        #remember the game
        self.game = game

        #set creep sprite
        self.img = img

        #initialize coordinates to 240,240
        self.x = self.y = 240

        #initialize our current destination to -1, -1
        self.x_next = self.y_next = -1

        #initialize rect, h/w: 24/32
        self.rect = pygame.Rect(self.x, self.y, 24, 32)

        #set current tile position
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24

        #speed in pixels/tick
        self.x_speed = 10.0
        self.y_speed = 10.0

        #x movement, -1 to 1
        self.x_move = 0

        #y movement, -1 to 1
        self.y_move = 0

        #initialize our unique attributes
        self.weapons = []
        #self.init_attributes(number)


    ## the init_attributes function
    #  @brief generates a class of creep based on the give number
    #  @param number determines what type of creep to generate
    #  @todo add more creeps!
    def init_attributes(self, number):
        #generic and boring
        if number == 0:
            self.health = 100
            self.speed = 10
            self.weapons.append(Weapon())

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
        self.x_next = self.x + self.x_move * self.x_speed
        self.y_next = self.y + self.y_move * self.y_speed

    ## the move function
    #  @brief handles what happens when the creep can actually move to its desired location
    #  @param x the x coordinate to move to
    #  @param y the y coordinate to move to
    def move(self, new_x, new_y):
        #update our rect's position
        self.rect.move_ip(new_x - self.x, new_y - self.y)

        #update our actual position
        self.x = new_x
        self.y = new_y

    ## the update function
    #  @brief handles all creep operations per frame
    #  @param game the instance of the class Game that this Creep resides in
    def update(self):
        #update our current tile position (can't do this before draw)
        self.x_tile = self.rect.centerx//24
        self.y_tile = self.rect.centery//24

        #set our x/y movement based on our destination
        self.next_move()

        self.move(self.x_next, self.y_next)

    ## the draw function
    #  @brief draws the creep to the screen, called once per frame
    #  @param screen the screen that the creep should be drawn to
    def draw(self, screen):
        #blit it!
        screen.blit(self.img, pygame.Rect(self.x, self.y, 24, 32), pygame.Rect(25*2, 33 * 2, 24, 32))
