import pygame

class GUIObject(object):
    def __init__(self, x, y, width, height, f, args):
        """initialize GUI object"""
        #rect
        self.rect = pygame.Rect(x, y, width, height)
        #image
        #text
        self.text = [[""],[""]] # 2D list that stores multiple messages made up of multiple parts (strings, variables)
        self.textIndex = 0
        
        #function: note: it must take a list of arguments
        self.f = f
        #args: a list of arguments to pass to the function, when it is called.
        self.args = args
        #special? (enabled, hidden, slide out)
        self.hover = False #true if currently being hovered over.
        
    def function(self):
        """invoke this GUI Object's function"""
        self.f( self.args )

    def get_text(self):
        """returns a string, made by concatenating all the text in self.text stored at the current self.textIndex"""
        txt = ""
        for s in self.text[self.textIndex]:
            txt += str( s )
        return txt
