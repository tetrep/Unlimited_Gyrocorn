import pygame
from gui_object import *

class GUI_Tower_Buy(object):
    # @ param g a reference to the game class. Created at initialization because it will be used ALOT.
    def __init__(self, g):
        """Initialize the GUI object"""
        super(GUI_Tower_Buy, self).__init__()
        self.img = pygame.image.load("Art/GUI.png").convert()
        self.img2 = pygame.image.load("Art/GUI2.png").convert()
        self.font = pygame.font.Font(None, 20)
        
        self.objects = []
        self.g = g #stores a reference to the game engine

        self.generate_GUI_objects()


    def generate_GUI_objects(self):
        """builds the GUI"""
        #Turrets
        # 1 xp 100
        # 2
        # 3
        
        #generate objects
        g = self.g #enable shorthand

        x = g.screenSize[0] - 256
        y = 0
        
        #x out button
        temp = GUIObject(x + 256 - 24, 0, 24, 24, self.exit_action, [])
        temp.text = [["X"]]
        self.objects.append( temp )

        for i in range(0, 7):
            y += 24
            temp = GUIObject(x, y, 256, 24, self.buy_action, [i, self.get_cost(i)])
            temp.text = [ [self.get_name(i), " g: ", self.get_cost(i)] ]
            self.objects.append( temp )

    def get_cost(self, i):
        """get the cost of the tower"""
        # @ param i the turret's type (enumerated int)
        if i == 0:   # basic
            return 100
        elif i == 1: # sniper
            return 200
        elif i == 2: # piercing
            return 300
        elif i == 3: # mortar
            return 300
        elif i == 4: # paralysis
            return 200
        elif i == 5: # fire
            return 200
        elif i == 6: # ice
            return 200
        elif i == 7: # lightning
            return 200
        else:
            return 0
        
    def get_name(self, i):
        """get the name of the tower"""
        # @ param i the turret's type (enumerated int)
        if i == 0:   # basic
            return "Basic Turret"
        elif i == 1: # sniper
            return "Sniper Turret"
        elif i == 2: # piercing
            return "Piercing Turret"
        elif i == 3: # mortar
            return "Mortar"
        elif i == 4: # paralysis
            return "Paralyzing Turret"
        elif i == 5: # fire
            return "Fire Turret"
        elif i == 6: # ice
            return "Ice Turret"
        elif i == 7: # lightning
            return "Lightning Turret"
        else:
            return "ERROR"
        
    
    def update(self):
        """update method"""
        for x in self.objects:
            if x.rect.collidepoint( pygame.mouse.get_pos() ) == True:
                x.hover = True
            else:
                x.hover = False

    
    def get_input(self):
        """handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    #event.pos[x, y] are mouse x, y coordinates.
                    #iterate through each object, check for collision, call function on collision

                    for x in self.objects:
                        if x.rect.collidepoint( (event.pos[0], event.pos[1]) ) == True:
                            x.function()
                            return #1 input/frame (solves an issue with the submenu pulling out and immediately getting input and closing)
                            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    self.exit_action( [] )

        
    def draw(self):
        """draw method"""
        width = self.g.screenSize[0]
        height = self.g.screenSize[1]
        #initialize the GUI canvas
        temp = pygame.Surface( (width, height) )
        temp.fill( (255, 0, 255) )
        temp.set_colorkey( (255, 0, 255) )
        img = self.img
        img.set_colorkey( (255, 0, 255) )
        for x in self.objects:
            #change the look if this object is hovered over
            if x.hover == True:
                img = self.img2
            else:
                img = self.img
            #DRAW THE OBJECT
            temp.blit(img, pygame.Rect(x.rect.x, x.rect.y, 4, 4), pygame.Rect(0, 0, 4, 4) ) #top left corner
            temp.blit(img, pygame.Rect(x.rect.x + x.rect.width - 4, x.rect.y, 4, 4), pygame.Rect(8, 0, 4, 4) ) #top right corner
            temp.blit(img, pygame.Rect(x.rect.x, x.rect.y + x.rect.height - 4, 4, 4), pygame.Rect(0, 8, 4, 4) ) #bottom left corner
            temp.blit(img, pygame.Rect(x.rect.x + x.rect.width - 4, x.rect.y + x.rect.height - 4, 4, 4), pygame.Rect(8, 8, 4, 4) ) #bottom right corner

            #left edge
            temp2 = pygame.Surface( (4, 1))
            temp2.blit(img, pygame.Rect(0, 0, 4, 1), pygame.Rect(0, 5, 4, 1) )
            temp2 = pygame.transform.scale( temp2, (4, x.rect.height - 8) )
            temp.blit( temp2, pygame.Rect(x.rect.x, x.rect.y + 4, 4, x.rect.height - 8) )
            #right edge
            temp2 = pygame.Surface( (4, 1))
            temp2.blit(img, pygame.Rect(0, 0, 4, 1), pygame.Rect(8, 5, 4, 1) )
            temp2 = pygame.transform.scale( temp2, (4, x.rect.height - 8) )
            temp.blit( temp2, pygame.Rect(x.rect.x + x.rect.width - 4, x.rect.y + 4, 4, x.rect.height - 8) )
            #top edge
            temp2 = pygame.Surface( (1, 4))
            temp2.blit(img, pygame.Rect(0, 0, 1, 4), pygame.Rect(5, 0, 1, 4) )
            temp2 = pygame.transform.scale( temp2, (x.rect.width - 8, 4) )
            temp.blit( temp2, pygame.Rect(x.rect.x + 4, x.rect.y, x.rect.width - 8, 4) )
            #bottom edge
            temp2 = pygame.Surface( (1, 4))
            temp2.blit(img, pygame.Rect(0, 0, 1, 4), pygame.Rect(5, 8, 1, 4) )
            temp2 = pygame.transform.scale( temp2, (x.rect.width - 8, 4) )
            temp.blit( temp2, pygame.Rect(x.rect.x + 4, x.rect.y + x.rect.height - 4, x.rect.width - 8, 4) )
            #center
            temp2 = pygame.Surface( (1, 1) )
            temp2.blit(img, pygame.Rect(0, 0, 1, 1), pygame.Rect(5, 5, 1, 1) )
            temp2 = pygame.transform.scale( temp2, (x.rect.width - 8, x.rect.height - 8) )
            temp.blit( temp2, pygame.Rect(x.rect.x + 4, x.rect.y + 4, x.rect.width - 8, x.rect.height - 8) )

            #text
            temp.blit( self.font.render( x.get_text(), 0, (255, 255, 255) ), pygame.Rect(x.rect.x + 4, x.rect.y + 4, x.rect.width - 4, x.rect.height -4) )
        self.g.screen.blit(temp, pygame.Rect(0, 0, width, height) )

    #GUI OBJECT FUNCTION DEFINITIONS
    def null_action(self, arg):
        """for GUI Objects that do nothing when clicked"""
        pass

    def buy_action(self, arg):
        """function for use with equipment"""
        # @ param args a list of arguments.
        # @ param arg[0] = the turret's type (acts like enumerated int)
        # @ param arg[1] = the turret's cost
        g = self.g #enable shorthand

        #if the player can afford this tower
        if g.players[g.playerIndex].gold >= arg[1]:
            #in game, set mode to tower placement.
            #assign the tower type in game.
            g.turretType = arg[0]
            #assign the tower cost in game.
            g.turretCost = arg[1]
            #in game, do cost confirmation on placement.
            #close the menu
            self.exit_action( [] )

    def exit_action(self, arg):
        """x out of the menu. Actions should not be done in parts."""
        self.g.go_to_Game()
