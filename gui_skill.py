import pygame
from gui_object import *

class GUI_Skill(object):
    # @ param g a reference to the game class. Created at initialization because it will be used ALOT.
    def __init__(self, g):
        """Initialize the GUI object"""
        super(GUI_Skill, self).__init__()
        self.img = pygame.image.load("Art/GUI.png").convert()
        self.img2 = pygame.image.load("Art/GUI2.png").convert()
        self.font = pygame.font.Font(None, 20)
        
        self.objects = []
        self.g = g #stores a reference to the game engine
        
        self.PID = 0        #saves the player to modify
        self.SID = 0        #saves the skill slot #
        self.skillKey = 0   #saves the skill type
        self.skillAttr  = 0 #saves the element modifier/etc.
        #mode control for menu/submenu
        self.subMenuOpen = False

        self.generate_GUI_objects()


    def generate_GUI_objects(self):
        """builds the GUI"""
        #3 skill slots: 2 slots [type, attr/element]
        #aura         |  fire
        #projectiles  |  lightning
        #ray          |  ice
        #AoE          |  poison
        #breath       |
        #melee        |
        
        #generate objects
        g = self.g #enable shorthand

        x = g.screenSize[0] - 256
        y = 0

        #x out button
        temp = GUIObject(x + 256 - 24, y, 24, 24, self.exit_action, [])
        temp.text = [["X"]]
        self.objects.append( temp )

        #
        y += 24
        temp = GUIObject(x - 24, y, 512 + 24, 24, self.skill_buy_action, [])
        temp.text = [ [ "BUY ", self.get_skill_name( self.skillKey ), " : ", self.get_attr_name( self.skillAttr ), "  xp: ", 1000 ] ]
        self.objects.append( temp )
        #
        for i in range(0, 3):
            y += 24
            temp = GUIObject(x, y, 256, 24, self.skill_type_action, [i])
            temp.text = [ [ self.get_skill_name( i ) ] ]
            self.objects.append( temp )

        self.generate_submenu_objects()

    def generate_submenu_objects(self):
        g = self.g #enable shorthand
        
        x = g.screenSize[0]
        y = 24
        for i in range(0, 3):
            y += 24
            temp = GUIObject(x, y, 256, 24, self.skill_attr_action, [i])
            temp.text = [ [ self.get_attr_name( i ) ] ]
            self.objects.append( temp )
            
        #open submenu, if open
        if self.subMenuOpen == True:
            for x in self.objects:
                x.rect.move_ip(-256, 0)
        
    
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

    #helper functions
    def get_skill_name(self, i):
        """gets the name of the skill indexed by i"""
        if i == 0:
            return "Aura"
        elif i == 1:
            return "Missile"
        elif i == 2:
            return "Breath"
        else:
            return "ERROR"
        
    def get_attr_name(self, i):
        """gets the name of the attribute indexed by i"""
        if i == 0:
            return "Fire"
        elif i == 1:
            return "Frost"
        elif i == 2:
            return "Lightning"
        else:
            return "ERROR"

    def get_mana_cost(self, key, attr):
        """get the mana cost of the specified skill"""
        # @ param key an int representing the skill type
        # @ param attr an int representing the skill attribute
        if key == 0: #AURA
            return 1
        elif key == 1: #Missile
            return 0
        elif key == 2: #Breath
            return 20


    #GUI OBJECT FUNCTION DEFINITIONS
    def null_action(self, arg):
        """for GUI Objects that do nothing when clicked"""
        pass

    def skill_buy_action(self, arg):
        """buy the currently selected skill"""
        g = self.g #enable shorthand
        
        cost = 1000
        if g.players[self.PID].exp >= cost:
            g.players[self.PID].exp -= cost
            #assign the skill
            g.players[self.PID].skill[self.SID].skillKey = self.skillKey
            g.players[self.PID].skill[self.SID].skillAttr = self.skillAttr
            g.players[self.PID].skill[self.SID].skillCost = self.get_mana_cost(self.skillKey, self.skillAttr)
            #close the menu
            self.exit_action( [] )
        

    def skill_type_action(self, arg):
        """set the skill type"""
        # @ param arg a list of arguments
        # @ param arg[0] the skill key
        self.skillKey = arg[0]
        #open the submenu
        if self.subMenuOpen == False:
            self.subMenuOpen = True
            for x in self.objects:
                x.rect.move_ip(-256, 0)

    def skill_attr_action(self, arg):
        """set the skill attribute"""
        # @ param arg a list of arguments
        # @ param arg[0] the attribute key
        self.skillAttr = arg[0]
        #close the submenu
        self.subMenuOpen = False
        #update text
        del self.objects[:]
        self.generate_GUI_objects()

    def exit_action(self, arg):
        """x out of the menu. Actions should not be done in parts."""
        self.g.go_to_Game()
