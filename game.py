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

        self.creep_wins = 0
        self.max_creep_wins = 2
        
        self.saver = SaveLoad()
        
    def load_assets(self):
        """pre-load all graphics and sound"""
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.bigfont = pygame.font.Font("freesansbold.ttf", 32)
        self.imgCreep = pygame.image.load("Art/units/pikeman-red.png").convert()
        self.imgCreep.set_colorkey( (255, 0, 255) )
        self.imgCreepArmored = pygame.image.load("Art/units/armored-red.png").convert()
        self.imgCreepArmored.set_colorkey( (255, 0, 255) )
        self.imgCreepFire = pygame.image.load("Art/units/mage-red-fire.png").convert()
        self.imgCreepFire.set_colorkey( (255, 0, 255) )
        self.imgCreepFrost = pygame.image.load("Art/units/mage-red-frost.png").convert()
        self.imgCreepFrost.set_colorkey( (255, 0, 255) )
        self.imgCreepLightning = pygame.image.load("Art/units/mage-red-lightning.png").convert()
        self.imgCreepLightning.set_colorkey( (255, 0, 255) )
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
        self.menu_background_sound.set_volume(.4)
        self.battle_background_sound = pygame.mixer.Sound("Music/battlemusic.ogg")
        self.battle_background_sound.set_volume(.4)
        self.build_background_sound = pygame.mixer.Sound("Music/buildmusic.ogg")
        self.build_background_sound.set_volume(.4)
        
        self.fire_skill_sound = pygame.mixer.Sound("Music/fire.ogg")
        self.fire_skill_sound.set_volume(.7)
        self.ice_skill_sound = pygame.mixer.Sound("Music/ice.ogg")
        self.ice_skill_sound.set_volume(.9)
        self.lightning_skill_sound = pygame.mixer.Sound("Music/lightning.ogg")
        self.poison_skill_sound = pygame.mixer.Sound("Music/poison.ogg")
        self.missile_sound = pygame.mixer.Sound("Music/turretattack.ogg")
        self.missile_sound.set_volume(.7)
        self.buy_sound = pygame.mixer.Sound("Music/cash.ogg")
        self.hit_sound = pygame.mixer.Sound("Music/playerhit.ogg")
        self.hit_sound.set_volume(.7)
        self.enemy_hit_sound = pygame.mixer.Sound("Music/enemyhit.ogg")
        self.enemy_hit_sound.set_volume(.4)
        self.attack_sound = pygame.mixer.Sound("Music/enemyattack.ogg")
        self.attack_sound.set_volume(.7)
        
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

    def creep_won(self):
        self.creep_wins += 1

        if(self.creep_wins > self.max_creep_wins):
            print "YOU LOST HAHAHAHA"
            self.go_to_MainMenu()
        
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

        #updates existing bullets
        for b, bullet in enumerate(self.bullets):
            if bullet.dead == True:
                self.bullets.pop(b)
            bullet.update(self)
            
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
            
        if self.gameState == 0:
            self.check_level_over()
            
    ## Update function that affects the background for menus
    def update_menu_background(self):
        self.timeToNextSpawn += 1
        
        #Spawns creeps every time an interval has passed
        if self.timeToNextSpawn >= self.timeBetweenSpawns:
            for i in xrange(0,5):
                self.spawn_creep()
            
            #Also sets the target view to one of the creeps
            randSize = random.randint(200,760)
            self.targetViewSize = pygame.Rect(0,0,randSize,randSize)
            self.targetViewSize.centerx = self.creeps[0].rect.centerx
            self.targetViewSize.centery = self.creeps[0].rect.centery
            self.targetViewSize.clamp_ip(self.screen.get_rect())
        
            self.timeToNextSpawn = 0
            
        #Zooms view on certain area
        viewSurface = self.screen.subsurface(self.viewSize)
        viewSurface = pygame.transform.scale(viewSurface,
        (self.screen.get_width(),self.screen.get_height()))
        self.screen.blit(viewSurface,(0,0))
        
        #update viewSurface to move it towards target
        xDiff = self.viewSize.left-self.targetViewSize.left
        yDiff = self.viewSize.top-self.targetViewSize.top
        
        #Checks how much farther it has to go, and if it's done, sets a  new target
        if math.fabs(xDiff) < 1.0 and math.fabs(yDiff) < 1.0:
            #If there are no creeps, focusses on a random tower
            if len(self.creeps) == 0:
                if len(self.turrets) > 0:
                    selectedTurret = random.randint(0,len(self.turrets)-1)
                    randSize = random.randint(300,500)
                    self.targetViewSize = pygame.Rect(0,0,randSize,randSize)
                    self.targetViewSize.centerx = self.turrets[selectedTurret].rect.centerx
                    self.targetViewSize.centery = self.turrets[selectedTurret].rect.centery
                    self.targetViewSize.clamp_ip(self.screen.get_rect())
                #No creeps, and no turrets
                else:
                    randSize = random.randint(500,760)
                    self.targetViewSize = pygame.Rect(random.randint(0,768),random.randint(0,768),randSize,randSize).clamp(self.screen.get_rect())
            #Else, focusses on one of the creeps
            else:
                selectedCreep = random.randint(0,len(self.creeps)-1)
                randSize = random.randint(300,500)
                self.targetViewSize = pygame.Rect(0,0,randSize,randSize)
                self.targetViewSize.centerx = self.creeps[selectedCreep].rect.centerx
                self.targetViewSize.centery = self.creeps[selectedCreep].rect.centery
                self.targetViewSize.clamp_ip(self.screen.get_rect())
                
                self.targetCreepView = selectedCreep
        
        if xDiff>0:
            xDiff=1
        elif xDiff<0:
            xDiff=-1
        else:
            xDiff=0
        if yDiff>0:
            yDiff=1
        elif yDiff<0:
            yDiff=-1
        else:
            yDiff=0
        
        self.viewSize.move_ip(-xDiff,-yDiff)
        
        #Update the viewSurface to resize to targetSize
        wDiff = self.viewSize.width-self.targetViewSize.width
        hDiff = self.viewSize.height-self.targetViewSize.height
        
        if wDiff>0:
            wDiff=1
        elif wDiff<0:
            wDiff=-1
        else:
            wDiff=0
        if hDiff>0:
            hDiff=1
        elif hDiff<0:
            hDiff=-1
        else:
            hDiff=0
        
        self.viewSize.inflate_ip(-wDiff,-hDiff)
        self.viewSize.clamp_ip(self.screen.get_rect())
            

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
        elif self.gameState == 6:
            self.menuInput()
        elif self.gameState == 7:
            self.menuInput()
            
    def gameInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #exit
                    self.go_to_InGameMenu()
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
                        
                if event.button == 3: #right mouse click
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #exit
                    self.go_to_BuildMenu()
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
                    
                #Start Level
                if event.key == pygame.K_RETURN:
                    self.go_to_Game()
                    
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

                    game_starting = False
                    
                    for button in self.MenuButtons:
                        game_starting = button.click(pos)
                           
                    if game_starting == False:
                        #check if there's already a turret here. if so, open upgrade menu. (in build mode)
                        for t in self.turrets:
                            if t.x / 24 == pos[0] / 24 and t.y / 24 + 2 == pos[1] / 24:
                                #open turret upgrade gui
                                self.gui = GUI_Tower_Upgrade( self, t )
                                self.go_to_TowerUpgrade()
                        
                        #if there's no turret here, and this tile isn't blocked, and it is affordable, place one. (in build mode)
                        if self.turretType != -1 and self.tiles[pos[0] / 24][pos[1] / 24].blocking == False:
                            if self.players[self.playerIndex].gold >= self.turretCost:
                                self.turrets.append( self.turretFactory.createTurret( self, self.turretType, pos[0], pos[1] ) )
                                self.players[self.playerIndex].gold -= self.turretCost #TODO: make sure it places turret before taking cash!
                        


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
            for x in range(1, random.randint(self.level//2, self.level) + 10):#random.randint(10, 20)+self.level):
                self.creeps.append(self.cfactory.make(random.randint(1, 5)))
        else:
            self.creeps.append(Creep(img, x, y, self, ctype))

    def give_xp(self, amt):
        """give the players amt xp"""
        for p in self.players:
            p.exp += amt
            

    def give_gold(self, amt):
        """give the players amt gold"""
        for p in self.players:
            p.gold += amt
        

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
        
        self.turrets = sorted(self.turrets, key = lambda turret: turret.y)
        for turret in self.turrets:
            turret.draw( self )

        for bullet in self.bullets:
            bullet.draw( self )

        self.draw_HUD()
        
    def draw_tiles(self):
        for x in range(0, self.tiles.__len__() ):
            for y in range(0, self.tiles[x].__len__() ):
                self.tiles[x][y].draw( self ) #[ [(0,0), (0,1), ...], [(1,0),(1,1),...], ...]

    def draw_menu(self):
        for button in self.MenuButtons:
            button.draw(self.screen)
            
    def draw_HUD(self):
        """Draws the HUD"""
        #xp
        self.screen.blit( self.font.render( "xp: " + str(self.player.exp), 0, (255, 255, 255) ), pygame.Rect(24, 56, 256, 24) )
        #gold
        self.screen.blit( self.font.render( "g : " + str(self.player.gold), 0, (255, 255, 255) ), pygame.Rect(24, 80, 256, 24) )
        #round
        self.screen.blit( self.bigfont.render( "ROUND " + str(self.level), 0, (192, 0, 0) ), pygame.Rect(24, 24, 256, 32) )

        #i was going to do all this, but got lazy.
        #party faces
        #HP/MP bars
        #Active player: HP/MP bars
        
        #skills
        #gray if not enough mana.
        #exception: auras: gray if off
        #symbol for aura, breath, projectile.
        #highlight selected skill
        #mouse wheel to change selection
        
        
        #HP bars under players
        for p in self.players:
            barbg = pygame.Surface( (int(26 * self.zoom), 8) ).convert()
            barbg.fill( (0, 0, 0) )
            width = [(int( 26 * self.zoom * float( p.hp[0] ) / float( p.hp[1] ) ) - 2), 0]
            barfg = pygame.Surface( (max( width ), 6) ).convert()
            barfg.fill( (0, 255, 0) )
            pos = self.convertGamePixelsToZoomCoorinates( (p.x, p.y) )
            self.screen.blit( barbg, pygame.Rect( pos[0] - 1,     pos[1] + 32 * self.zoom,     barbg.get_width(), barbg.get_height() ) )
            self.screen.blit( barfg, pygame.Rect( pos[0] - 1 + 1, pos[1] + 32 * self.zoom + 1, barfg.get_width(), barfg.get_height() ) )

        #MP bars under players
        for p in self.players:
            barbg = pygame.Surface( (int(26 * self.zoom), 5) ).convert()
            barbg.fill( (0, 0, 0) )
            width = [(int( 26 * self.zoom * float( p.mana[0] ) / float( p.mana[1] ) ) - 2), 0]
            barfg = pygame.Surface( (max( width ), 3) ).convert()
            barfg.fill( (0, 64, 224) )
            pos = self.convertGamePixelsToZoomCoorinates( (p.x, p.y) )
            self.screen.blit( barbg, pygame.Rect( pos[0] - 1,     pos[1] + (32 + 8 - 1) * self.zoom,     barbg.get_width(), barbg.get_height() ) )
            self.screen.blit( barfg, pygame.Rect( pos[0] - 1 + 1, pos[1] + (32 + 8 - 1) * self.zoom + 1, barfg.get_width(), barfg.get_height() ) )

        #HP bars under creeps
        for creep in self.creeps:
            barbg = pygame.Surface( (int(26 * self.zoom), 6) ).convert()
            barbg.fill( (0, 0, 0) )
            width = [(int( 26 * self.zoom * float( creep.health ) / float( creep.max_health ) ) - 2), 0]
            barfg = pygame.Surface( (max( width ), 4) ).convert()
            barfg.fill( (255, 32, 0) )
            pos = self.convertGamePixelsToZoomCoorinates( (creep.rect.x, creep.rect.y) )
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

    def game_exit(self):
        pygame.quit()
        sys.exit()
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#State Machine
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------        

    ## Initializes all variables related to a single game. 
    def start_game(self,targetLevel=0):
        #map
        self.mapSize = [32, 32]
        self.selectedLevel = targetLevel
        
        #Resets map to original state
        self.maps[targetLevel] = Terrain(self,self.maps[targetLevel].sourcePath)
        
        self.tiles = self.maps[targetLevel]
        
        #players
        self.players = [Player(self, self.imgPlayer, self.imgPlayerAI, (self.tiles.target[0]*self.tiles.tileSize.width,self.tiles.target[1]*self.tiles.tileSize.height)),
                        Player(self, self.imgPlayer, self.imgPlayerAI, (self.tiles.target[0]*self.tiles.tileSize.width,self.tiles.target[1]*self.tiles.tileSize.height)), \
                        Player(self, self.imgPlayer, self.imgPlayerAI, (self.tiles.target[0]*self.tiles.tileSize.width,self.tiles.target[1]*self.tiles.tileSize.height)), 
                        Player(self, self.imgPlayer, self.imgPlayerAI, (self.tiles.target[0]*self.tiles.tileSize.width,self.tiles.target[1]*self.tiles.tileSize.height))]
        self.playerIndex = 0
        self.player = self.players[self.playerIndex]
        self.player.activate()

        #turrets
        self.turrets = []
        self.turretType = 0          #stores the turret type to build
        self.turretCost = 1000000000 #stores cost to build a turret, impossibly high initialization cost
        self.bullets = []

        #creeps
        self.cfactory = CreepFactory(self.imgCreep, self)
        self.creeps = []
        self.cp = CreepPath(self.tiles.target, 4, self)
        self.level = 1 

        #gui
        self.gui = GUI_Equipment( self )

        #drawing variables
        self.zoom = 1.0
        self.focus = [0, 0]     # the central point of the viewbox
        self.view = [0, 0]      # the width + height of the viewbox
        self.viewMax = [0, 0]   # the width + height of the total screen
        # all draw calls in game-space MUST use zoom and focus. GUI draws don't need to.  

        self.turretFactory = TurretFactory()

    ## Sets the gamestate to the in-game state. Everything is updated in this state, but the player cannot buy or upgrade anything. 
    def go_to_Game(self,targetLevel=0):
        #we're done bulding, we dont want a turrect selected anymore
        self.turretType = -1

        #recalculate path
        self.cp.find_path()

        self.battle_background_sound.play(loops = -1)
        self.menu_background_sound.stop()
        self.build_background_sound.stop()
        
        if self.gameState == 2:     #Returning from the build Phase, just spawn more creeps
            self.spawn_creep()
            
        self.MenuButtons = []
        self.gameState = 0
        
    ## Activates the equipment buy gui
    def go_to_GUI(self):
        self.gui = GUI_Equipment( self )
        self.gameState = 1
        
    ## Activates the tower buying gui
    def go_to_TowerBuy(self):
        self.gui = GUI_Tower_Buy( self )
        self.gameState = 1

    ## Activates the tower upgrade gui
    def go_to_TowerUpgrade(self):
        #gui requires a reference to a turret. Created elsewhere.
        self.gameState = 1

    ## Activates the skill selection gui
    def go_to_SkillGUI(self):
        self.gui = GUI_Skill( self, self.playerIndex )
        self.gameState = 1
        
    ## Sets the gamestate to the build phase and resets certain aspects if coming from certain
    #  game states. Player can buy and upgrade towers, skills and stats. 
    def go_to_Build(self,targetLevel=0):
        self.cp.reset_path()
        #Not coming back from an ingame state, so reset
        if self.gameState != 0 and self.gameState != 1 and self.gameState !=2 and self.gameState != 7:  
            self.start_game(targetLevel)
            
        #Returning from an in-game state, so resets the buttons and sounds
        if self.gameState == 0 or self.gameState == 3 or self.gameState == 4 or self.gameState == 7:
            self.build_background_sound.play(loops = -1)
            self.battle_background_sound.stop()
            self.menu_background_sound.stop()
            self.MenuButtons = []
            self.MenuButtons.append(Button("Start!",32,(self.screen.get_width()-100,self.screen.get_height()-100),None,self.go_to_Game,[]))
            #also, refill the player's transient stats
            for p in self.players:
                p.refill()
            
        self.gameState = 2
    
    ## Sets the gameState to the Main Menu
    #  Also sets up the background by starting a game (the game does not take player input for
    #  this game, and automatically spawns enemies)
    def go_to_MainMenu(self):
    
        #Sounds for the menu
        self.menu_background_sound.play(loops = -1)
        self.battle_background_sound.stop()
        self.build_background_sound.stop()
        
        #Creates the 4 buttons
        self.MenuButtons = [] 
        self.MenuButtons.append(Button("Start",32,(25,25),self.imgButton,self.go_to_Build,[]))
        self.MenuButtons.append(Button("Select Level",32,(25,200),self.imgButton,self.go_to_LevelSelect,[]))
        self.MenuButtons.append(Button("Load",32,(25,375),self.imgButton,self.go_to_Load,[]))
        self.MenuButtons.append(Button("Exit Game",32,(25,550),self.imgButton,self.game_exit,[]))
        
        
        #Sets up the background
        self.start_game()
        
        #Controls automatic creep spawning
        self.timeBetweenSpawns = 900
        self.timeToNextSpawn = 800
        
        #Sets the current view for the screen (screen will only show contents of this rect)
        randSize = random.randint(200,760)
        self.viewSize = pygame.Rect(random.randint(0,768),random.randint(200,768),randSize,randSize).clamp(self.screen.get_rect())
        
        #Sets the target view for the screen (screen will pan and zoom to this rect)
        randSize = random.randint(200,760)
        self.targetViewSize = pygame.Rect(random.randint(0,768),random.randint(0,768),randSize,randSize).clamp(self.screen.get_rect())
        
        #Creates towers of random type on the map
        for i in xrange(0,10):
            pos = [random.randint(1,31),random.randint(1,31)]
            if not self.tiles[pos[0]][pos[1]].blocking:
                self.turrets.append( self.turretFactory.createTurret( self, random.randint(0,5), pos[0]*24, pos[1]*24 ) )
        
        self.gameState=3
        
    ## Sets gameState to the Level Select state, creating the appropriate buttons
    def go_to_LevelSelect(self):
    
        #Resets the buttons and adds one that returns to the main menu
        self.MenuButtons = []
        self.MenuButtons.append(Button("Return To Menu",32,(50,50),self.imgButton,self.go_to_MainMenu,[]))
        
        #Adds buttons that go to the given levels
        for i in xrange(len(self.maps)):
            self.MenuButtons.append(Button("",32,
            ((i*265)%(self.screen.get_width()-265)+100,(215+(i/2)*265)),
            pygame.transform.scale(self.maps[i].img,(250,250)),self.go_to_Build,[i]))
        
        self.gameState=4
        
    ## Sets gameState to the Save/Load state, creating the appropriate buttons
    def go_to_Load(self):
        self.MenuButtons = []
        self.MenuButtons.append(Button("Return To Menu",32,(25,25),self.imgButton,self.go_to_MainMenu,[]))
        #self.MenuButtons.append(Button("Load", 32, (25,200), self.imgButton, self.saver.load_game,[self]))
        #Eventually will display a list of available save files
        
        
        self.gameState=5
        
    def go_to_InGameMenu(self):
        self.MenuButtons = []
        self.MenuButtons.append(Button("Go To Menu", 32, (25,25), self.imgButton, self.go_to_MainMenu,[]))
        self.MenuButtons.append(Button("Return To Game", 32, (25,200), self.imgButton, self.go_to_Game,[]))
        self.MenuButtons.append(Button("Exit Game",32,(25,375),self.imgButton,self.game_exit,[]))
    
        self.gameState=6
        
    def go_to_BuildMenu(self):
        self.MenuButtons = []
        self.MenuButtons.append(Button("Go To Menu", 32, (25,25), self.imgButton, self.go_to_MainMenu,[]))
        self.MenuButtons.append(Button("Return To Game", 32, (25,200), self.imgButton, self.go_to_Build,[]))
        #self.MenuButtons.append(Button("Save",32,(25,375),self.imgButton,self.saver.save_game,[self]))
        self.MenuButtons.append(Button("Exit Game",32,(25,550),self.imgButton,self.game_exit,[]))
    
        self.gameState=7
        
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
            elif self.gameState == 1: #In game GUI
                self.gui.update()
                self.draw()
                self.gui.draw()
            elif self.gameState == 2: #BuildPhase
                self.update()
                self.draw()
                self.draw_menu()
            elif self.gameState == 3: #Main menu
                self.update()
                self.draw()
                self.update_menu_background()
                self.draw_menu()
                """
                for super_dooper_counter_looper in range(0, 100):
                    self.cp.reset_path()
                    self.cp.find_path()
                sys.exit()
                #"""
            elif self.gameState == 4: #Level Selection
                self.update()
                self.draw()
                self.update_menu_background()
                self.draw_menu()
            elif self.gameState == 5: #Load screen (theoretical at this point)
                self.update()
                self.draw()
                self.update_menu_background()
                self.draw_menu()
            elif self.gameState == 6: #InGame Menu
                self.draw()
                self.draw_menu()
            elif self.gameState == 7: #BuildPhase Menu
                self.draw()
                self.draw_menu()
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
"""
profile.run('main()','profile results')
p = pstats.Stats('profile results')
p.sort_stats('cumulative').print_stats()
#"""