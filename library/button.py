'''
button class that draws buttons for the menu
NICK TKACHOV
'''
import pygame
from pygame.locals import *
from .config import config
pygame.font.init()
button_font = pygame.font.Font('freesansbold.ttf', 14)
WHITE = (255,255,255)
class Button():

    def __init__(self,index,text,icon,highlight,normal,rect):
        #initial values
        self._spacing = 50
        self._buttonw = 150
        self._buttonh = 40
        self._rect =rect
        self._text = text
        self._index = index
        self._icon = icon
        self._font = button_font
        self._visible = True
        self.selected = False
        self.surfaceNormal = normal
        self.surfaceHighlight = highlight
                
    def draw(self,surfaceObj):
        if self._visible:
            #draws the button
            self._rect = pygame.Rect(surfaceObj.get_width()/2 - self._rect.w/2,self._rect.y,self._rect.w,self._rect.h)
            pygame.draw.rect(surfaceObj,(30,30,30),self._rect)
            if self.selected: #different surface if item is selected
                surfaceObj.blit(self.surfaceHighlight,self._rect)
            else:
                surfaceObj.blit(self.surfaceNormal,self._rect)
                
    def _update(self):
        #updates button
        self.surfaceNormal = pygame.transform.smoothscale(self.surfaceNormal,self._rect.size)
        self.surfaceHighlight = pygame.transform.smoothscale(self.surfaceHighlight,self._rect.size)

        w = self._rect.width
        h = self._rect.height
        captionSurf = self._font.render(self._text, False, WHITE)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceHighlight.blit(captionSurf, captionRect)
        
        #draws a border around button if its highlighted
        pygame.draw.rect(self.surfaceHighlight, WHITE, pygame.Rect((0, 0, w, h)), 1) # black border around everything
        pygame.draw.line(self.surfaceHighlight, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self.surfaceHighlight, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self.surfaceHighlight, WHITE, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceHighlight, WHITE, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self.surfaceHighlight, WHITE, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self.surfaceHighlight, WHITE, (w - 2, 2), (w - 2, h - 2))

    def handleEvent(self,eventObj):
        pass
    
    def lclick_event(self, event):
        pass

    def mouse_hover(self,event):
        self.selected = True
    
    def mouse_unhover(self,event):
        self.selected = False
    @staticmethod
    def is_text():
        return False
                
