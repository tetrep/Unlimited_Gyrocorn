import pygame
import sys

class Button(object):
    def __init__(self, text="", fontSize=32, pos = (0,0), backgroundImg=None, function=None, args=[]):
        super(Button,self).__init__()
        self.text = text
        self.function=function
        self.args=args
        fontObj = pygame.font.Font("freesansbold.ttf",fontSize)
        
        if backgroundImg==None:    #No background image was passed to the button
            tSurface = fontObj.render(self.text, True, (0,0,0,),(55,220,255))
            self.img = pygame.Surface((tSurface.get_width()+30,tSurface.get_height()+30))
            self.img.fill((55,220,225))
            self.img.blit(tSurface,(15,15))
        else:
            tSurface = fontObj.render(self.text, True, (0,0,0),(255,255,255,255))
            self.img=backgroundImg.convert_alpha()
            self.img.blit(tSurface, (self.img.get_width()/2-tSurface.get_width()/2,self.img.get_height()/2-tSurface.get_height()/2))
            
        
        self.rect = pygame.Rect(pos[0],pos[1],self.img.get_width(),self.img.get_height())
        
    
    def click(self, mousePos=(0,0)):
        if self.rect.collidepoint(mousePos):
            self.function(*self.args)
            
    def draw(self,drawImg):
        drawImg.blit(self.img, (self.rect.left,self.rect.top))
        
pygame.init()
window = pygame.display.set_mode((500,500))
img = pygame.image.load("Art/ButtonBackground.png").convert()
img.set_colorkey((255,0,255))
img = pygame.transform.scale(img,(int(float(img.get_width())/img.get_height()*200),200)).convert_alpha()
x = Button("hello",32,(0,0),img,None)
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    x.draw(window)
    pygame.display.flip()