import pygame, sys, random, os

from tile import *
from player import *

from turret import *
from turretfactory import *

from button import *
from gui_equipment import *
from gui_tower_buy import *
from gui_tower_upgrade import *
from gui_skill import *

from creep_path import *

from node import *
from terrain import *
from turretfactory import *
from creep_factory import *

from save_load import *

import profile, pstats #DEBUG LINE

#  @class Game
#  @brief this class is the game engine. It manages game logic, input, and rendering.
class Game(object):
    def __init__(self):
        """Initialize the game"""
        super(Game, self).__init__()
        pygame.init()
        self.clock = pygame.time.Clock()
        
        
        #screen initialization
        self.screenSize = (768, 768)
        self.screen = pygame.display.set_mode( self.screenSize )
        
        self.maps = []
        
        self.load_assets()
        
        self.gameState=-1
        self.go_to_MainMenu()
        
        self.selectedLevel = 0
        
    def load_assets(self):
        """pre-load all graphics and sound"""
        self.font = pygame.font.Font(None, 20)
        self.bigfont = pygame.font.Font(None, 32)
        self.font = pygame.font.Font(None, 20)
        self.bigfont = pygame.font.Font(None, 32)
        self.imgCreep = pygame.image.load("Art/units/pikeman-red.png").convert()
        self.imgPlayer = pygame.image.load("Art/units/sprite-general-gabe.png").convert()
        self.imgPlayer.set_colorkey( (255, 0, 255) )
        self.imgPlayerAI = pygame.image.load("Art/units/sprite-general-gabe2.png").convert()
        self.imgPlayerAI.set_colorkey( (255, 0, 255) )
        self.imgTile = pygame.image.load("Art/tiles/tile-grass.png").convert()
        self.imgTileWall = pygame.image.load("Art/tiles/obj-wall.png").convert()
        self.imgBasicTurret = pygame.image.load("Art/tiles/obj-guardtowertest3.png").convert()
        self.imgBasicTurret.set_colorkey( (255, 0, 255) )
        
        self.imgButton = pygame.image.load("Art/ButtonBackground.png").convert()
        self.imgButton.set_colorkey((255,0,255))
        self.imgButton = pygame.transform.scale(self.imgButton,
        (int(float(self.imgButton.get_width())/self.imgButton.get_height()*150),150)).convert_alpha()
        
        self.menu_background_sound = pygame.mixer.Sound("Music/menumusic.ogg")
        self.menu_background_sound.set_volume(.7)
        self.battle_background_sound = pygame.mixer.Sound("Music/battlemusic.ogg")
        self.battle_background_sound.set_volume(.7)
        self.build_background_sound = pygame.mixer.Sound("Music/buildmusic.ogg")
        self.build_background_sound.set_volume(.7)
        
        for map in os.listdir("Levels"):
            self.maps.append(Terrain(self,"Levels/"+map))

    def load_tiles(self):
        """generate a level, and store it in tiles[][]"""
        for x in range(0, self.mapSize[0]):
            self.tiles.append( [] )
            for y in range(0, self.mapSize[1]):
                tempTile = Tile(self.imgTile)
                tempTile.x = x * 24
                tempTile.y = y * 24
                if y == 4 and x == 4:
                    tempTile.blocking = True
                    tempTile.img = self.imgTileWall
                self.tiles[x].append( tempTile )

        self.cp = CreepPath(self.tiles.target, 4, self)
        self.cp.find_path()
        
    def update(self):
        """Do logic/frame"""
        #self.deltaT = self.clock.tick()

        #update players
        self.player = self.players[self.playerIndex]
        for player in self.players:
            player.update( self )

        #update creeps
        for creep in self.creeps:
            creep.update()
            #creep.receive_damage(1)

        #update turrets
        for x, turret in enumerate(self.turrets):
            if turret.valid_placement == True:
                turret.update(self)
            else:
                #remove turrets that do not have valid placement
                self.turrets.pop(x)

        #update bullets
        for bullet in self.bullets:
            bullet.update( self )

        #kill creeps
        self.reap()

        #update drawing variables
        self.update_view()

        #check to see if the game has been lost
        if self.game_lost() == True:
            print("GAME OVER")
            #exit
            pygame.quit()
            sys.exit()
            
        if self.gameState != 2:
            self.check_level_over()

    def update_view(self):
        """create view and focus variables (draw control) based on the screen size and zoom level."""
        #do not attempt to understand this. Your head WILL explode. Just accept that it works and don't touch it.
        #on that note, this is targeted for clean-up to make it more understandable.
        #that being said, the math involved is not intuitive.

        #set the size of the viewing area
        self.view[0] = self.screenSize[0]
        self.view[1] = self.screenSize[1]

        #set the size of the game area bounds
        self.viewMax[0] = 24 * self.mapSize[0] * self.zoom
        self.viewMax[1] = 24 * self.mapSize[1] * self.zoom

        #set the focus point, or where the screen will be centered to the player's pos.
        self.focus = [(int)(self.player.x * self.zoom), (int)(self.player.y * self.zoom)]


        #clamp the screen, so the focus shifts from player -> game area at the edges of the game area.        
        if self.focus[0] - self.view[0] / 2 < 0:
            self.focus[0] = (0 + self.view[0] / 2)
        elif self.focus[0] + self.view[0] / 2 > self.viewMax[0]:
            self.focus[0] = (self.viewMax[0] - self.view[0] / 2)

        if self.focus[1] - self.view[1] / 2 < 0:
            self.focus[1] = (0 + self.view[1] / 2)
        elif self.focus[1] + self.view[1] / 2 > self.viewMax[1]:
            self.focus[1] = (self.viewMax[1] - self.view[1] / 2)
            
    def get_input(self):
        """get and handle user input"""
        if self.gameState == 0:
            self.gameInput()
        elif self.gameState == 1:
            self.gui.get_input()
        elif self.gameState == 2:
            self.buildInput()
        elif self.gameState == 3:
            self.menuInput()
        elif self.gameState == 4:
            self.menuInput()
        elif self.gameState == 5:
            self.menuInput()
            
    def gameInput(self):
        for event in pygame.event.get():
            #key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #exit
                    pygame.quit()
                    sys.exit()
                #PLAYER SWITCHING (Must go before movement)
                if event.key == pygame.K_i:
                    #+1
                    self.player.reset_movement()
                    self.player.deactivate()
                    self.playerIndex -= 1
                    if self.playerIndex < 0:
                        self.playerIndex = 3
                    self.players[self.playerIndex].activate()
                if event.key == pygame.K_o:
                    #-1
                    self.player.reset_movement()
                    self.player.deactivate()
                    self.playerIndex += 1
                    if self.playerIndex > 3:
                        self.playerIndex = 0
                    self.players[self.playerIndex].activate()
                #MOVEMENT
                if event.key == pygame.K_w:
                    #up
                    self.player.direction[1] += -1
                if event.key == pygame.K_a:
                    #down
                    self.player.direction[0] += -1
                if event.key == pygame.K_s:
                    #left
                    self.player.direction[1] += 1
                if event.key == pygame.K_d:
                    #right
                    self.player.direction[0] += 1
                # / MOVEMENT
                #MENUS
                
                #CAN WE UPDATE PLAYERS IN THE MIDDLE OF COMBAT?
                #if event.key == pygame.K_p:
                #    #toggle player menu
                #    self.go_to_GUI()
                    
            #key released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.direction[1] += 1
                if event.key == pygame.K_a:
                    self.player.direction[0] += 1
                if event.key == pygame.K_s:
                    self.player.direction[1] += -1
                if event.key == pygame.K_d:
                    self.player.direction[0] += -1

            #mouse controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    #event.pos[0] and event.pos[1] are the mouse x,y coordinates respectively relative to the game window
                    #needs to be converted to give a mapping in game space.
                    #if   map = pos * zoom - (focus - view / 2)
                    #then pos = (map + (focus - view / 2) ) / zoom

                    pos = self.convertZoomCoordinatesToGamePixels( (event.pos[0], event.pos[1]) )

                    #check if there's already a turret here. if so, open upgrade menu. (in build mode)
                    for t in self.turrets:
                        if t.x / 24 == pos[0] / 24 and t.y / 24 + 2 == pos[1] / 24:
                            #open turret upgrade gui
                            self.gui = GUI_Tower_Upgrade( self, t )
                            self.mode = 1
                    
                    #if there's no turret here, and it is affordable, place one. (in build mode)
                    if self.players[self.playerIndex].gold >= self.turretCost:
                        self.turrets.append( self.turretFactory.createTurret( self, self.turretType, pos[0], pos[1] ) )
                        self.players[self.playerIndex].gold -= self.turretCost #TODO: make sure it places turret before taking cash!
                        
                elif event.button == 3: #right mouse click
                    pos = self.convertZoomCoordinatesToGamePixels( (event.pos[0], event.pos[1]) )
                    self.players[self.playerIndex].use_skill(self, 0, pos[0], pos[1])
                    
                elif event.button == 4: #mouse wheel down
                    self.zoom -= .1
                    if self.zoom < 1:
                        self.zoom = 1
                        
                elif event.button == 5: #mouse wheel up
                    self.zoom += .1
                    if self.zoom > 4:
                        self.zoom = 4
                        
    def buildInput(self):
        for event in pygame.event.get():
            #key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #exit
                    pygame.quit()
                    sys.exit()
                #PLAYER SWITCHING (Must go before movement)
                if event.key == pygame.K_i:
                    #+1
                    self.player.reset_movement()
                    self.player.deactivate()
                    self.playerIndex -= 1
                    if self.playerIndex < 0:
                        self.playerIndex = 3
                    self.players[self.playerIndex].activate()
                if event.key == pygame.K_o:
                    #-1
                    self.player.reset_movement()
                    self.player.deactivate()
                    self.playerIndex += 1
                    if self.playerIndex > 3:
                        self.playerIndex = 0
                    self.players[self.playerIndex].activate()
                #MOVEMENT
                if event.key == pygame.K_w:
                    #up
                    self.player.direction[1] += -1
                if event.key == pygame.K_a:
                    #down
                    self.player.direction[0] += -1
                if event.key == pygame.K_s:
                    #left
                    self.player.direction[1] += 1
                if event.key == pygame.K_d:
                    #right
                    self.player.direction[0] += 1
                # / MOVEMENT
                #MENUS
                if event.key == pygame.K_p:
                    #toggle player menu
                    self.go_to_GUI()
                if event.key == pygame.K_t:
                    #toggle build menu
                    #TODO: rewrite/move this code
                    self.go_to_TowerBuy()
                if event.key == pygame.K_k:
                    #open skill menu
                    self.go_to_SkillGUI()
                    
            #key released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.direction[1] += 1
                if event.key == pygame.K_a:
                    self.player.direction[0] += 1
                if event.key == pygame.K_s:
                    self.player.direction[1] += -1
                if event.key == pygame.K_d:
                    self.player.direction[0] += -1

            #mouse controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left click
                    #event.pos[0] and event.pos[1] are the mouse x,y coordinates respectively relative to the game window
                    #needs to be converted to give a mapping in game space.
                    #if   map = pos * zoom - (focus - view / 2)
                    #then pos = (map + (focus - view / 2) ) / zoom

                    pos = self.convertZoomCoordinatesToGamePixels( (event.pos[0], event.pos[1]) )

                    #check if there's already a turret here. if so, open upgrade menu. (in build mode)
                    for t in self.turrets:
                        if t.x / 24 == pos[0] / 24 and t.y / 24 + 2 == pos[1] / 24:
                            #open turret upgrade gui
                            self.gui = GUI_Tower_Upgrade( self, t )
                            self.go_to_TowerUpgrade()
                    
                    #if there's no turret here, and it is affordable, place one. (in build mode)
                    if self.players[self.playerIndex].gold >= self.turretCost:
                        self.turrets.append( self.turretFactory.createTurret( self, self.turretType, pos[0], pos[1] ) )
                        self.players[self.playerIndex].gold -= self.turretCost #TODO: make sure it places turret before taking cash!
                        
                    for button in self.MenuButtons:
                        button.click(pos)

                elif event.button == 3: #right mouse click
                    pos = self.convertZoomCoordinatesToGamePixels( (event.pos[0], event.pos[1]) )
                    self.players[self.playerIndex].use_skill(self, 0, pos[0], pos[1])
                    for button in self.MenuButtons:
                        button.click(pos)
                    
                elif event.button == 4: #mouse wheel down
                    self.zoom -= .125
                    if self.zoom < 1:
                        self.zoom = 1
                        
                elif event.button == 5: #mouse wheel up
                    self.zoom += .125
                    if self.zoom > 4:
                        self.zoom = 4
    
    def menuInput(self):
        for event in pygame.event.get():
            #Key presses
            if event.type == pygame.KEYDOWN:
                #Escape key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Left Click
                if event.button == 1:
                    for button in self.MenuButtons:
                        button.click(event.pos)

    ## the reap function
    #  @brief iterates over the creeps and culls the dead ones
    def reap(self):
        for x, creep in enumerate(self.creeps):
            if creep.reap():
                self.creeps.pop(x)

    ## the spawn creep function
    #  @brief spawns creeps, if no parameters are passed it uses the creep factory
    #  @param img the image the creep will use, optional
    #  @param x the x pixel position of the creep, optional
    #  @param y the y pixel position of the creep, optional
    #  @param ctype the attributes of the creep, optional
    def spawn_creep(self, img = None, x = None, y = None, ctype = None):
        #we want to use the factory
        if(img == None):
            for x in range(1, 2):#random.randint(10, 20)+self.level):
                self.creeps.append(self.cfactory.make(random.randint(1, 5)))
        else:
            self.creeps.append(Creep(img, x, y, self, ctype))

    def game_lost(self):
        """returns true if the game has been lost"""
        for p in self.players:
            if p.dead == False:
                return False
        return True

    def check_level_over(self):
        if len(self.creeps) == 0:
            self.level+=1
            self.go_to_Build()
        
    def draw(self):
        """draw"""
        self.screen.fill( (0, 0, 0) ) #screen wipe
        #draw stuff, from back->front
        
        self.tiles.draw()

        for player in self.players:
            player.draw( self )

        for creep in self.creeps:
            creep.draw()
        
        for turret in self.turrets:
            turret.draw( self )
            
        for button in self.MenuButtons:
            button.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw( self )

        self.draw_HUD()
        
    def draw_tiles(self):
        for x in range(0, self.tiles.__len__() ):
            for y in range(0, self.tiles[x].__len__() ):
                self.tiles[x][y].draw( self ) #[ [(0,0), (0,1), ...], [(1,0),(1,1),...], ...]

    def draw_menu(self):
        self.screen.fill((0,0,0))
        for button in self.MenuButtons:
            button.draw(self.screen)
            
    def draw_HUD(self):
        """Draws the HUD"""
        #xp
        self.screen.blit( self.font.render( str(self.player.exp), 0, (255, 255, 255) ), pygame.Rect(24, 24, 256, 24) )
        #gold
        self.screen.blit( self.font.render( str(self.player.gold), 0, (255, 255, 255) ), pygame.Rect(24, 48, 256, 24) )
        
        #party faces
        #HP/MP bars

        #Active player: HP/MP bars
        #skills
        
        
        #HP bars over players
        for p in self.players:
            barbg = pygame.Surface( (int(26 * self.zoom), 8) ).convert()
            barbg.fill( (0, 0, 0) )
            width = [(int( 26 * self.zoom * float( p.hp[0] ) / float( p.hp[1] ) ) - 2), 0]
            barfg = pygame.Surface( (max( width ), 6) ).convert()
            barfg.fill( (0, 255, 0) )
            pos = self.convertGamePixelsToZoomCoorinates( (p.x, p.y) )
            self.screen.blit( barbg, pygame.Rect( pos[0] - 1,     pos[1] + 32 * self.zoom,     barbg.get_width(), barbg.get_height() ) )
            self.screen.blit( barfg, pygame.Rect( pos[0] - 1 + 1, pos[1] + 32 * self.zoom + 1, barfg.get_width(), barfg.get_height() ) )
        
    def convertGamePixelsToZoomCoorinates(self, (x, y) ):
        #get the offset of the entire zoomed-in game subspace.
        offset = [-1 *( self.focus[0] - self.view[0] / 2 ), -1 * ( self.focus[1] - self.view[1] / 2 ) ]
        #apply the zoom factor and offset.
        return ( (int)( x * self.zoom + offset[0] ), (int)( y * self.zoom + offset[1] ) )

    def convertZoomCoordinatesToGamePixels(self, (x, y) ):
        #reverse the game->zoom conversion                
        return ( (int)( ( x + (self.focus[0] - self.view[0] / 2) ) / self.zoom ) , (int)( ( y + (self.focus[1] - self.view[1] / 2) ) / self.zoom ) )

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#State Machine
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------        

    def start_game(self,targetLevel=0):
        #players
        self.players = [Player(self.imgPlayer, self.imgPlayerAI), Player(self.imgPlayer, self.imgPlayerAI), \
                        Player(self.imgPlayer, self.imgPlayerAI), Player(self.imgPlayer, self.imgPlayerAI)]
        self.playerIndex = 0
        self.player = self.players[self.playerIndex]
        self.player.activate()

        #map
        self.mapSize = [32, 32]
        self.tiles = self.maps[targetLevel]
        self.selectedLevel = targetLevel

        #turrets
        self.turrets = []
        self.turretType = 0          #stores the turret type to build
        self.turretCost = 1000000000 #stores cost to build a turret, impossibly high initialization cost
        self.bullets = []

        #creeps
        self.cfactory = CreepFactory(self.imgCreep, self)
        self.creeps = []
        self.cp = CreepPath((24, 31), 4, self)
        self.cp.find_path()
        self.level = 1 

        #gui
        self.gui = GUI_Equipment( self )

        self.cfactory = CreepFactory(self.imgCreep, self)

        self.level = 1

        #drawing variables
        self.zoom = 1.0
        self.focus = [0, 0]     # the central point of the viewbox
        self.view = [0, 0]      # the width + height of the viewbox
        self.viewMax = [0, 0]   # the width + height of the total screen
        # all draw calls in game-space MUST use zoom and focus. GUI draws don't need to.  

        self.turretFactory = TurretFactory()
        
    def go_to_Game(self,targetLevel=0):
        self.battle_background_sound.play(loops = -1)
        self.menu_background_sound.stop()
        self.build_background_sound.stop()
        
        if self.gameState == 2:     #Returning from the build Phase, just spawn more creeps
            self.spawn_creep()
            
        self.MenuButtons = [] 
        self.gameState = 0
        
    def go_to_GUI(self):
        self.gui = GUI_Equipment( self )
        self.gameState = 1
        
    def go_to_TowerBuy(self):
        self.gui = GUI_Tower_Buy( self )
        self.gameState = 1

    def go_to_TowerUpgrade(self):
        #gui requires a reference to a turret. Created elsewhere.
        self.gameState = 1

    def go_to_SkillGUI(self):
        self.gui = GUI_Skill( self )
        self.gameState = 1
        
    def go_to_Build(self,targetLevel=0):
        if self.gameState != 0 and self.gameState != 1 and self.gameState !=2:  #Coming back from an ingame state, so don't reset
            self.start_game(targetLevel)
            
<<<<<<< HEAD
        if self.gameState == 0 or self.gameState == 3:
            self.build_background_sound.play(loops = -1)
            self.battle_background_sound.stop()
            self.menu_background_sound.stop()
=======
        if self.gameState == 0 or self.gameState == 3 or self.gameState == 4:
>>>>>>> cf4fa0f76104e4163899df5bb79f6560cbea4689
            self.MenuButtons = []
            self.MenuButtons.append(Button("Start!",32,(self.screen.get_width()-100,self.screen.get_height()-100),None,self.go_to_Game,[]))
            
        self.gameState = 2
    
    def go_to_MainMenu(self):
        self.menu_background_sound.play(loops = -1)
        self.battle_background_sound.stop()
        self.build_background_sound.stop()
        
        self.MenuButtons = [] 
        self.MenuButtons.append(Button("Start",32,(50,50),self.imgButton,self.go_to_Build,[]))
        self.MenuButtons.append(Button("Select Level",32,(50,250),self.imgButton,self.go_to_LevelSelect,[]))
        self.MenuButtons.append(Button("Save or Load",32,(50,450),self.imgButton,self.go_to_SaveLoad,[]))
        
        self.gameState=3
        
    ## Sets gameState to the Level Select state, creating the appropriate buttons
    def go_to_LevelSelect(self):
        self.MenuButtons = []
        self.MenuButtons.append(Button("Return To Menu",32,(50,50),self.imgButton,self.go_to_MainMenu,[]))
        for i in xrange(len(self.maps)):
            self.MenuButtons.append(Button("",32,
            ((i*265)%(self.screen.get_width()-265)+100,(215+(i/4)*265)),
            pygame.transform.scale(self.maps[i].img,(250,250)),self.go_to_Build,[i]))
        
        self.gameState=4
        
    ## Sets gameState to the Save/Load state, creating the appropriate buttons
    def go_to_SaveLoad(self):
        self.MenuButtons = []
        self.MenuButtons.append(Button("Return To Menu",32,(50,50),self.imgButton,self.go_to_MainMenu,[]))
        
        self.gameState=5
        
    def main(self):
        """main game loop"""
        while True:
            #build mode: controls change, GUI access opens up. (clicking on GUI brings it up, changes mode?)
            #pause mode:
            #on mode change, reset direction for player? (if keep)
            #various menu modes
            self.get_input()
            self.deltaT = self.clock.tick()
            if self.gameState == 0: #standard game
                self.update()
                self.draw()
            elif self.gameState == 1: #In game player menu
                self.gui.update()
                self.draw()
                self.gui.draw()
            elif self.gameState == 2: #BuildPhase
                self.update()
                self.draw()
            elif self.gameState == 3: #Main menu
                self.draw_menu()
            elif self.gameState == 4: #Level Selection
                self.draw_menu()
            elif self.gameState == 5: #Save/load screen (theoretical at this point)
                self.draw_menu()
            elif self.gameState == 6: #Win
                pass
            elif self.gameState == 7: #Lose
                pass
            else:   #ABORT, ABORT
                pygame.quit()
                sys.exit()
            pygame.display.flip()

#main only exists so the profiler can call it
def main():
    g = Game()
    g.main()

#don't profile:
main()
#profile the game
#profile.run('main()','profile results')
#p = pstats.Stats('profile results')
#p.sort_stats('cumulative').print_stats()
