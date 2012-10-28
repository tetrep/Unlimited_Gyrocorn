import pygame

class GUI(object):
    #a general solution is so very very much trouble.
    def __init__(self):
        """Initialize the GUI object"""
        super(GUI, self).__init__()
        self.objects = []
        self.subMenuObjects = []
        #mode control for menu/submenu
        for i in range (0, 4):
            #represent equipment
            o = GUIObject()
            o.equipID = i
            o.slotID = -1
            o.x = 32
            o.y = i * 24 * 5 + j * 24
            o.width = 128
            o.height = 24
            self.objects.append(o)
            for j in range (0, 4):
                #represent slots
                o = GUIObject()
                o.equipID = i
                o.slotID = j
                o.x = 32
                o.y = i * 24 * 5 + j * 24
                o.width = 128
                o.height = 24
                self.objects.append(o)
    
    def update(self, g):
        """update method"""
        #probably not needed?
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
        
        pass
    
    def get_input(self, g):
        """handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    #event.pos[x, y] are mouse x, y coordinates.
                    for x in self.objects:
                        if x.pos_in( (event.pos[0], event.pos[1]) ) == True:
                            if x.slotID == -1: #Equipment
                                if g.player.equipment[x.equipID].locked == True and \
                                g.player.exp > -1:
                                    g.player.equipment[x.equipID].unlock()
                            else: #Slot
                                if g.player.equipment[x.equipID].slot[x.slotID].locked == True:
                                    g.player.equipment[x.equipID].unlock_slot()
                                elif g.player.equipment[x.equipID].slot[x.slotID].modCode == 0: #uninitialized
                                    #open the assignment sub-menu
                                    pass
                                else:
                                    g.player.equipment[x.equipID].slot[x.slotID].upgrade()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #g.mode = 0
                    #kill this object
                    pass
        
    def draw(self, g):
        """draw method"""
        width = 480
        height = 480
        temp = pygame.Surface( (width, height) )
        img = pygame.image.load("Art/GUI.png").convert()
        img.set_colorkey( (255, 0, 255) )
        for x in self.objects:
            temp.blit(img, pygame.Rect(x.x, x.y, 4, 4), pygame.Rect(0, 0, 4, 4) ) #top left corner
            temp.blit(img, pygame.rect(x.x + x.width - 4, x.y, 4, 4), pygame.Rect(8, 0, 4, 4) ) #top right corner
            temp.blit(img, pygame.rect(x.x, x.y + x.height - 4, 4, 4), pygame.Rect(0, 8, 4, 4) ) #bottom left corner
            temp.blit(img, pygame.rect(x.x + x.width - 4, x.y + x.height - 4, 4, 4), pygame.Rect(8, 8, 4, 4) ) #bottom right corner

            #left edge
            temp2 = pygame.Surface( (4, 1))
            temp2.blit(img, pygame.Rect(0, 0, 4, 1), pygame.Rect(0, 5, 4, 1) )
            temp2 = pygame.transform( temp2, (4, x.height - 8) )
            temp.blit( temp2, pygame.Rect(x.x, x.y + 4, 4, x.height - 8) )
            #right edge
            temp2 = pygame.Surface( (4, 1))
            temp2.blit(img, pygame.Rect(0, 0, 4, 1), pygame.Rect(8, 5, 4, 1) )
            temp2 = pygame.transform( temp2, (4, x.height - 8) )
            temp.blit( temp2, pygame.Rect(x.x + x.width - 4, x.y + 4, 4, x.height - 8) )
            #top edge
            temp2 = pygame.Surface( (1, 4))
            temp2.blit(img, pygame.Rect(0, 0, 1, 4), pygame.Rect(5, 0, 4, 1) )
            temp2 = pygame.transform( temp2, (4, x.height - 8) )
            temp.blit( temp2, pygame.Rect(x.x, x.y + 4, 4, x.height - 8) )
            #bottom edge
            

            #temp.blit(img, pygame.rect(x.x, x.y + 4, 4, x.height), pygame.Rect(0, 5, 4, 1) ) #left edge
            #temp.blit(img, pygame.rect(x.x, x.y, 4, x.height), pygame.Rect(8, 5, 4, 1) ) #right edge
            #temp.blit(img, pygame.rect(x.x, x.y, x.width, 4), pygame.Rect(5, 0, 4, 1) )#top edge
            #temp.blit(img, pygame.rect(x.x, x.y, x.width, 4), pygame.Rect(5, 8, 1, 4) )#bottom edge
            
            #temp.blit(img, pygame.rect(x.x, x.y, 4, 1), pygame.Rect(5, 5, 1, 1) )#center
            #zoom/stretch/tile the edges.
            #pygame.transform.Scale(surface, (x, y)) #returns new surface, scaled to new resolution
            pass
        #submenu?
        pass

class GUIObject(object):
    def __init__(self):
        """initialize GUI object"""
        self.equipID = 0
        self.slotID = 0
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.text = ""
        self.icon = 0
    def pos_in(self, (x, y)):
        """determines if (x, y) is within this object"""
        if x >= self.x and x <= self.x + self.width:
            if y >= self.y and y <= self.y+ self.height:
                return True
            
        return False
