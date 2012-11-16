import pygame

class GUIObject(object):
    def __init__(self, x, y, width, height, f, args):
        """initialize GUI object"""
        #rect
        self.rect = pygame.Rect(x, y, width, height)
        #image
        #text
        self.text = ""
        #how do we get the text to output lots of variables from a different class, with unknown indexes?
        #rather than making the data and putting it in here, we could save the PID, EID, and SID, and pass them to get the text...?
        
        #function: note: it must take a list of arguments
        self.f = f
        #args: a list of arguments to pass to the function, when it is called.
        self.args = args
        #special? (enabled, hidden, slide out)
        self.hover = False #true if currently being hovered over.
        
    def function(self):
        """invoke this GUI Object's function"""
        self.f( self.args )
