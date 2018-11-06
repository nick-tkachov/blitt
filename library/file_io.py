'''
Simple file.io used for importing a text file specified and reading it
NICK TKACHOV
'''
import pygame
from pygame.locals import *

class File:

    def __init__(self,location):
        self._location = location

    def open_files(self):
        return [line.rstrip('\n') for line in open('./data/'+self._location,'r')]

    def write_to(self,values):
        with open('./data/'+self._location,'a') as self._file:
            self._file.write(values + '\n')
        