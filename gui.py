import pygame
from gui_object import *

class GUI(object):
    # @ param g a reference to the game class. Created at initialization because it will be used ALOT.
    def __init__(self, g):
        """Initialize the GUI object"""
        super(GUI, self).__init__()
        self.img = pygame.image.load("Art/GUI.png").convert()
        self.img2 = pygame.image.load("Art/GUI2.png").convert()
        self.font = pygame.font.Font(None, 20)
        
        self.objects = []
        self.g = g #stores a reference to the game engine
        
        self.PID = g.playerIndex  #stores the player index
        self.EID = 0              #stores the equipment index
        self.SID = 0              #stores the slot index
        #mode control for menu/submenu
        self.subMenuOpen = False

        self.generate_GUI_objects()


    def generate_GUI_objects(self):
        """builds the GUI"""
        #[ ]equip 1     |  Atk          lv. 1
        #    [ ]slot 1  |  Def          lv. 1
        #    [ ]slot 2  |  Hp           lv. 1
        #    [ ]slot 3  |  Regen        lv. 1
        #    [ ]slot 4  |  Absorb       lv. 1
        #[ ]equip 2     |  Life Leech   lv. 1
        #    [ ]slot 1  |  Move Speed   lv. 1
        #    [ ]slot 2  |  Attack Speed lv. 1
        #    [ ]slot 3  |  Crit         lv. 1
        #    [ ]slot 4  |  
        #[ ]equip 3     |  
        #    [ ]slot 1  |  
        #    [ ]slot 2  |  
        #    [ ]slot 3
        #    [ ]slot 4
        #[ ]equip 4
        #    [ ]slot 1
        #    [ ]slot 2
        #    [ ]slot 3
        #    [ ]slot 4
        
        #generate objects
        g = self.g #enable shorthand

        #stat totals
        #HP
        #damage (includes IAS, crit)
        #defense %
        #absorbtion
        #regen/sec
        #move speed
        #attack speed
        #crit
        #lifesteal
        
        x = g.screenSize[0] - 256
        y = 24

        #Player exp
        temp = GUIObject(x, 0, 256 - 24, 24, self.null_action, [])
        temp.text = [["EXP: ", g.players[self.PID].exp]]
        self.objects.append( temp )
        
        #x out button
        temp = GUIObject(x + 256 - 24, 0, 24, 24, self.exit_action, [])
        temp.text = [["X"]]
        self.objects.append( temp )
        
        #equipment and slots
        for i in range(0, 4):
            #equipment
            x = g.screenSize[0] - 256 - 24
            temp = GUIObject(x, y, 256 + 24, 24, self.equip_action, [self.PID, i])
            temp.text = [ ["LOCKED", ], ["Equipment "] ]
            if g.players[self.PID].equipment[i].locked == False:
                temp.textIndex = 1
            self.objects.append( temp )
            y += 24
            for j in range(0, 4):
                #slots
                x = g.screenSize[0] - 256
                temp = GUIObject(x, y, 256, 24, self.slot_action, [self.PID, i ,j])
                temp.text = [ ["LOCKED", ], \
                    [ self.g.players[self.PID].equipment[0].slot[0].decode_mod( g.players[self.PID].equipment[i].slot[j].modCode ), \
                    "  lv. ", g.players[self.PID].equipment[i].slot[j].modTier, "  xp: ",\
                    self.g.players[self.PID].equipment[0].slot[0].get_price( g.players[self.PID].equipment[i].slot[j].modCode, g.players[self.PID].equipment[i].slot[j].modTier + 1)] ]
                if g.players[self.PID].equipment[i].slot[j].locked == False:
                    temp.textIndex = 1
                self.objects.append( temp )
                y += 24
        #sub menu objects
        for i in range(1, 10):
            x = g.screenSize[0]
            y = i * 24
            temp = GUIObject(x, y, 256, 24, self.mod_action, [i])
            temp.text = [ [self.g.players[self.PID].equipment[0].slot[0].decode_mod(i), "  lv. 1", "  xp: ",\
                    self.g.players[self.PID].equipment[0].slot[0].get_price( i, 1 )]]
            self.objects.append( temp )

        #open submenu
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

    #GUI OBJECT FUNCTION DEFINITIONS
    def null_action(self, arg):
        """for GUI Objects that do nothing when clicked"""
        pass

    def equip_action(self, arg):
        """function for use with equipment"""
        # @ param args a list of arguments.
        # @ param arg[0] = the player id
        # @ param arg[1] = the equipment id
        g = self.g #enable shorthand
        
        #if this equipment is locked, unlock it.
        if g.players[arg[0]].equipment[arg[1]].locked == True and g.players[arg[0]].exp > 100:
            g.players[arg[0]].equipment[arg[1]].unlock()
            g.players[arg[0]].exp -= 100
            #update text
            del self.objects[:]
            self.generate_GUI_objects()

    def slot_action(self, arg):
        """function for use with slots"""
        # @ param args a list of arguments.
        # @ param arg[0] = the player ID
        # @ param arg[1] = the equipment ID
        # @ param arg[2] = the slot ID
        g = self.g #enable shorthand

        #if the equipment is still locked, make the error noise
        if g.players[arg[0]].equipment[arg[1]].locked == True:
            pass
            #error noise
        #if the player has unlocked the equipment the slot is a part of
        elif g.players[arg[0]].equipment[arg[1]].locked == False:
            #if the slot is locked, unlock it
            if g.players[arg[0]].equipment[arg[1]].slot[arg[2]].locked == True and g.players[arg[0]].exp > 100:
                g.players[arg[0]].equipment[arg[1]].slot[arg[2]].unlock()
                g.players[arg[0]].exp -= 100
                #update text
                del self.objects[:]
                self.generate_GUI_objects()
                
            #if the slot is unlocked
            elif g.players[arg[0]].equipment[arg[1]].slot[arg[2]].locked == False:
                #calculate cost of the upgrade
                code = g.players[arg[0]].equipment[arg[1]].slot[arg[2]].modCode
                tier = g.players[arg[0]].equipment[arg[1]].slot[arg[2]].modTier
                cost = g.players[arg[0]].equipment[0].slot[0].get_price( code, tier )
                
                #if the slot has no mod, select a mod for it (open submenu)
                if g.players[arg[0]].equipment[arg[1]].slot[arg[2]].modCode == 0:
                    #save currently selected playerID, equipmentID, and slotID
                    self.PID = arg[0]
                    self.EID = arg[1]
                    self.SID = arg[2]
                    #open submenu, if it's not already open
                    if self.subMenuOpen == False:
                        self.subMenuOpen = True
                        for x in self.objects:
                            x.rect.move_ip( -256, 0 )
                
                #if the slot has a mod, and the player can afford it, upgrade it
                elif g.players[arg[0]].equipment[arg[1]].slot[arg[2]].modTier < 4 and g.players[arg[0]].exp >= cost:

                    g.players[arg[0]].equipment[arg[1]].slot[arg[2]].upgrade()
                    g.players[arg[0]].exp -= cost
                    #update text
                    del self.objects[:]
                    self.generate_GUI_objects()
        

    def mod_action(self, arg):
        """function to assign an intial mod to an equipment slot"""
        # @ param args a list of arguments
        # @ param arg[0] = the mod ID
        g = self.g #enable shorthand
        #calculate cost
        cost = g.players[self.PID].equipment[0].slot[0].get_price( arg[0], 1)
        #if the upgrade is affordable, assign it + close the submenu
        if g.players[self.PID].exp >= cost:
            g.players[self.PID].exp -= cost
            g.players[self.PID].equipment[self.EID].slot[self.SID].assign_slot( arg[0], 1 )
            #close submenu
            self.subMenuOpen = False
            #update text
            del self.objects[:]
            self.generate_GUI_objects()
        #else, leave the menu open, and do nothing.
        else:
            #play the error sound
            pass

    def exit_action(self, arg):
        """x out of the menu. Actions should not be done in parts."""
        self.g.gameState = 0
