''' 
Font class allows easy creation and manipulation of text, instead of just having a dozen variables
NICK TKACHOV
'''
import pygame
from pygame.locals import *
class Font:
    
    def __init__(self,text,color,size,location,y):
         self._text = text
         self._color = color
         self._width = 100
         self._y = y
         self._x = 0
         self._height = 100
         self._location = location
         self._font = pygame.font.SysFont('Monospace',size)
         self._width,self._height = self._font.size(self._text)
    def _update(self):
        self._rendered = self._font.render(self._text,False,self._color)
        self._width,self._height = self._font.size(self._text)

    def draw(self,surface):
        if self._location == 'center':
            self._x = surface.get_width()/2 - self._width/2
        elif self._location == 'left':
            self._x = (surface.get_width()/2 - self._width/2)/4
        elif self._location == 'right':
            self._x = (surface.get_width()/2 - self._width/2)*1.8

        self._rect = [self._x,self._y,self._width,self._height]

        surface.blit(self._rendered,self._rect)

    def update_text(self,text):
        self._text = text

    @staticmethod
    def is_text():
        return True
    #ronnie
    def get_text(self):
        return self._text