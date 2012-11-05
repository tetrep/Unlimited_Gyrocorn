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
        self.subMenuObjects = []
        self.g = g #stores a reference to the game engine
        #mode control for menu/submenu

        #generate objects
        #x out
        temp = GUIObject(128, 0, 24, 24, self.exit_action, [])
        self.objects.append( temp )
        #equipment and slots
        x = 0
        y = 24
        for i in range(0, 4):
            #equipment
            x = 0
            temp = GUIObject(x, y, 128 + 24, 24, self.equip_action, [])
            self.objects.append( temp )
            y += 24
            for j in range(0, 4):
                #slots
                x = 24
                temp = GUIObject(x, y, 128, 24, self.slot_action, [0, i ,j])
                self.objects.append( temp )
                y += 24
        #sub menu objects
        
    
    def update(self):
        """update method"""
        #generate appropriate text, images, borders.
        #stat display pane (non-interactive) | equipment pane
        #x map -> equip pane
        #y map -> equip / equip and slot

        #error display (must unlock equipment first)
        
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
        
        #click equip to unlock. (cost xp)
        #click slot to unlock OR assign OR upgrade
        #  locked: unlock
        #  unassigned: assign
        #  assigned + not max tier: upgrade
        #assignment: pane opens to right w/ list, everything shifts left.
        #  during this, no other input accepted.
        #  esc -> gives cash back, undoes unlock?
        
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
                            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    self.exit_action( [] )
        
    def draw(self):
        """draw method"""
        width = 480
        height = 480
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
        self.g.screen.blit(temp, pygame.Rect(0, 0, width, height) )
    
    def null_action(self, arg):
        """pass to GUI Objects that do nothing when clicked"""
        pass

    def equip_action(self, arg):
        """function for use with equipment"""
        # @ param args a list of arguments.
        # @ param arg[0] = the player id
        # @ param arg[1] = the equipment id
        g = self.g #enable shorthand
        
        #if this equipment is locked, unlock it.
        if g.player.equipment[arg[1]].locked == True and g.player.exp > -1:
            g.player.equipment[arg[1]].unlock()
            g.player.exp -= 0

    def slot_action(self, arg):
        """function for use with slots"""
        # @ param args a list of arguments.
        # @ param arg[0] = the player ID
        # @ param arg[1] = the equipment ID
        # @ param arg[2] = the slot ID
        g = self.g #enable shorthand
        
        #if the player has unlocked the equipment the slot is a part of
        if g. player.equipment[arg[1]].locked == False:
            #if the slot is locked, unlock it
            if g.player.equipment[arg[1]].slot[arg[2]].locked == True and g.player.exp > -1:
                g.player.equipment[arg[1]].slot[arg[2]].unlock()
                self.player.exp -= 0
                
            #if the slot is unlocked
            elif g.player.equipment[arg[1]].slot[arg[2]].locked == False:
                #if the slot has no mod, select a mod for it (open submenu)
                if g.player.equipment[arg[1]].slot[arg[2]].modCode == 0:
                    #open submenu
                    pass
                
                #if the slot has a mod, upgrade it
                elif g.player.equipment[arg[1]].slot[arg[2]].modTier < 4 and g.player.exp > -1:
                    g.player.equipment[arg[1]].slot[arg[2]].upgrade()
                    g.player.exp -= 0
        

    def mod_action(self, arg):
        # @ param args a list of arguments
        # @ param arg[0] = the Player ID
        # @ param arg[1] = the equipment ID
        # @ param arg[2] = the slot ID
        # @ param arg[3] = the mod ID
        #if the upgrade is affordable, assign + close the submenu
        #else, leave the menu open, and do nothing.
        g = self.g #enable shorthand
        pass

    def exit_action(self, arg):
        """x out of the menu. Actions should not be done in parts."""
        self.g.mode = 0
#input handling (from call from game)
#mouseover handling (update)
#function defining
