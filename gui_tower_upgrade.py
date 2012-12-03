import pygame
from gui_object import *

class GUI_Tower_Upgrade(object):
    # @ param g a reference to the game class. Created at initialization because it will be used ALOT.
    # @ param turret a reference to the turret to upgrade.
    def __init__(self, g, turret):
        """Initialize the GUI object"""
        super(GUI_Tower_Upgrade, self).__init__()
        self.img = pygame.image.load("Art/GUI.png").convert()
        self.img2 = pygame.image.load("Art/GUI2.png").convert()
        self.font = pygame.font.Font(None, 20)
        
        self.objects = []
        self.g = g #stores a reference to the game engine
        self.turret = turret #store the turret to be upgraded

        self.generate_GUI_objects()


    def generate_GUI_objects(self):
        """builds the GUI"""
        #Turret Name
        #  Rate Of Fire   lv. 1  g 100
        #  Damage         lv. 1  g 100
        #  Range          lv. 1  g 100
        #  AoE            lv. 1  g 100
        
        #generate objects
        g = self.g #enable shorthand

        x = g.screenSize[0] - 256
        y = 0
        
        #x out button
        temp = GUIObject(x + 256 - 24, 0, 24, 24, self.exit_action, [])
        temp.text = [["X"]]
        self.objects.append( temp )

        #RoF upgrade
        y += 24
        temp = GUIObject(x, y, 256, 24, self.upgrade_rof, [])
        temp.text = [["Rate of Fire  lv. ", self.turret.getAttackSpeedLevel() , "  g: ", self.get_cost( self.turret.getAttackSpeedLevel() ) ], \
                     ["Rate of Fire  MAX"]]
        if self.turret.getAttackSpeedLevel() == 5:
            temp.textIndex = 1
        self.objects.append( temp )
        #Damage upgrade
        y += 24
        temp = GUIObject(x, y, 256, 24, self.upgrade_damage, [])
        temp.text = [["Damage       lv. ", self.turret.getDamageLevel() , "  g: ", self.get_cost( self.turret.getDamageLevel() ) ],\
                     ["Damage       MAX"]]
        if self.turret.getDamageLevel() == 5:
            temp.textIndex = 1
        self.objects.append( temp )
        #range upgrade
        y += 24
        temp = GUIObject(x, y, 256, 24, self.upgrade_range, [])
        temp.text = [["Range        lv. ", self.turret.getRangeLevel() , "  g: ", self.get_cost( self.turret.getRangeLevel() ) ],\
                     ["Range        MAX"]]
        if self.turret.getRangeLevel() == 5:
            temp.textIndex = 1
        self.objects.append( temp )
        #AoE upgrade (only generate if applicable)
        if self.turret.type == 3: #mortars only
            y += 24
            temp = GUIObject(x, y, 256, 24, self.upgrade_aoe, [])
            temp.text = [["AoE          lv. ", self.turret.getAoELevel() , "  g: ", self.get_cost( self.turret.getAoELevel() ) ], \
                         ["AoE          MAX"]]
            if self.turret.getAoELevel() == 5:
                temp.textIndex = 1
            self.objects.append( temp )

    def get_cost(self, level):
        """gets the cost of an upgrade"""
        # @ param level the tier of the upgrade
        if level < 1 or level > 4:
            return 0
        else:
            return level * 100
        
    
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

    def upgrade_rof(self, junk):
        """upgrades the turret's rate of fire"""
        player = self.g.players[self.g.playerIndex]
        cost = self.get_cost( self.turret.getAttackSpeedLevel() )
        if  player.gold >= cost:
            if self.turret.upgradeAttackSpeed() == True:
                player.gold -= cost
                #update text
                del self.objects[:]
                self.generate_GUI_objects()
        
    def upgrade_damage(self, junk):
        """upgrades the turret's damage"""
        player = self.g.players[self.g.playerIndex]
        cost = self.get_cost( self.turret.getDamageLevel() )
        if  player.gold >= cost:
            if self.turret.upgradeDamage() == True:
                player.gold -= cost
                #update text
                del self.objects[:]
                self.generate_GUI_objects()
        
    def upgrade_range(self, junk):
        """upgrades the turret's range"""
        player = self.g.players[self.g.playerIndex]
        cost = self.get_cost( self.turret.getRangeLevel() )
        if  player.gold >= cost:
            if self.turret.upgradeRange() == True:
                player.gold -= cost
                #update text
                del self.objects[:]
                self.generate_GUI_objects()
        
    def upgrade_aoe(self, junk):
        """upgrades the turret's aoe"""
        player = self.g.players[self.g.playerIndex]
        cost = self.get_cost( self.turret.getAoELevel() )
        if  player.gold >= cost:
            if self.turret.upgradeAoE() == True:
                player.gold -= cost
                #update text
                del self.objects[:]
                self.generate_GUI_objects()

            
    def exit_action(self, arg):
        """x out of the menu. Actions should not be done in parts."""
        self.g.go_to_Build()
