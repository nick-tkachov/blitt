'''
Entities for the game. This includes the bodies, swords on the ground or swords that are flying
these classes handle the entities, when they hit stuff or moving them, or updating the look
NICK TKACHOV
'''
import pygame
from pygame.locals import *
import random
sword = pygame.image.load('./assets/game/sword.png')

class Entity:
    #constructs entities, tables are used statically throughout all entities created
    sword_entities = []
    body_entities = []
    #this is just a base classs, it does nothing
    def __init__(self,posx,posy,floorh,floory,window):
        self._posx = posx
        self._posy = posy
        self._floorh = floorh
        self._floory = floory
        self._window = window
        self._debug = False
        self._isActive = True
        
    def __str__(self):
        pass

    def draw(self,surface):
        pass
    
    def update(self):
        pass

    def on_touch(self):
        pass

    def gravity(self):
        pass

    def isActive(self):
        return self._isActive

    @staticmethod
    def print_entities():
        pass

    @staticmethod
    def append_entities(entity):
        pass

    @staticmethod
    def remove_entities(entity):
        pass
        
class Sword_ENT(Entity):

    def __init__(self,posx,posy,floorh,floory,window):
        super().__init__(posx,posy,floorh,floory,window)
        #inherits from entity class, and creates its own variables
        self._posx = posx
        self._window = window
        self._posy = posy
        self._width = 10
        self._height = 90
        self._floorh = floorh
        self._floory = floory+11
        self._image = sword
        self._angle = 0

        #draws the rectangles that will be used as a hitbox
        self._rect = pygame.Rect(self._posx,self._posy,80,9)
        self._floor = pygame.Rect(0,self._floory,self._window.get_width(),self._floorh)
        self._swordsurface = pygame.transform.smoothscale(self._image,self._rect.size)
        self._image = pygame.transform.scale(self._image,(self._width,self._height))
        self._isActive = True
        self.append_entities(self)
        
    def __str__(self):
        return str(self._isActive)

    def draw(self,surface):
        #debug stuff used for testing
        if self._debug:
            pygame.draw.rect(surface,(255,255,255),self._rect)
        self._swordsurface = pygame.transform.rotate(self._image, 90)
        surface.blit(self._swordsurface,self._rect)

    def update(self,target):
        #checks if sword is still not on the floor, then it will have gravity
        if not self._rect.colliderect(self._floor):
            self._posy +=10
        self._rect = pygame.Rect(self._posx,self._posy,80,10)
        self._floor = pygame.Rect(0,self._floory,self._window.get_width(),self._floorh)
        self.draw(self._window)

    def pick_up(self):
        self._isActive = False

    def get_rect(self):
        return self._rect
    
    def hit_object(self):
        return None
    
    def isItem(self):
        return True
    
    def get_player(self):
        return True

    #read only methods
    @staticmethod
    def print_entities():
        return Entity.sword_entities

    @staticmethod
    def append_entities(entity):
        Entity.sword_entities.append(entity)

    @staticmethod
    def remove_entities(entity):
        Entity.sword_entities.remove(entity)

class Body_ENT(Entity):
    #entity used for creating the dead bodies
    def __init__(self,posx,posy,floorh,floory,window,color):
        super().__init__(posx,posy,floorh,floory,window)
        #inherits from another class again
        self._posx = posx
        self._window = window
        dead_char = pygame.image.load('./assets/game/dead_char.png')
        self._posy = posy + random.randint(10,15)
        self._floorh = floorh
        self._floory = floory-5
        self._color = color
        self.append_entities(self)
        self._image = dead_char
        self._rect = pygame.Rect(self._posx,self._posy,80,80)
        self._floor = pygame.Rect(0,self._floory,self._window.get_width(),self._floorh)

    def update(self,target):
        #if body is in the air it will fall
        self._bodysurface = pygame.transform.smoothscale(self._image,self._rect.size)
        if not self._rect.colliderect(self._floor):
            self._posy +=15
        self._rect = pygame.Rect(self._posx,self._posy,80,80)
        self._floor = pygame.Rect(0,self._floory,self._window.get_width(),self._floorh)
        self.draw(self._window)

    def draw(self,surface):
        if self._debug:
            pygame.draw.rect(surface,self._color,self._rect)
        surface.blit(self._bodysurface,self._rect)

    def get_player(self):
        return True

    @staticmethod
    def print_entities():
        return Entity.body_entities

    @staticmethod
    def append_entities(entity):
        Entity.body_entities.append(entity)

    
class FSword_ENT(Entity):
    #entity for the flying sword
    def __init__(self,posx,posy,floorh,floory,window,direction,player,target):
        super().__init__(posx,posy,floorh,floory,window)
        self._posx = posx
        self._window = window
        self._direction = direction
        self._posy = posy
        self._angle = 0
        self._player = player
        self._floorh = floorh
        self._floory = floory-5
        self._width = 10
        self._height = 90
        self._target = target
        self.append_entities(self)
        self._image = sword
        self._image = pygame.transform.scale(self._image,(self._width,self._height))
        #complex formula so sword spins correctly
        self._centerpoint = self._image.get_rect().center
        self._rect = pygame.Rect(self._posx,self._posy+self._height,self._height,self._width)
        self._floor = pygame.Rect(0,self._floory,self._window.get_width(),self._floorh)
     
        #updates sword
    def update(self,target):
        self._target = target
        if self._isActive:
            if self._posx >= self._window.get_width()-80 or self._posx <= 0:
                self.hit_object()
            else:
                if self._direction == 'left':
                    self._posx -= 9
                    self._angle += 25
                elif self._direction == 'right':
                     self._posx += 9
                     self._angle -= 25
            self._floor = pygame.Rect(0,self._floory,self._window.get_width(),self._floorh)
            self._rect = pygame.Rect(self._posx,self._posy+self._height/2,self._height,self._width)

        self.draw(self._window)

    def get_player(self):
        return self._player

    def isItem(self):
        return False
    def draw(self,surface):
        #debug stuff
        if self._debug:
            pygame.draw.rect(surface,(0,255,0),self._rect)
        self._swordsurface = pygame.transform.rotate(self._image, self._angle)
        self._rect = self._swordsurface.get_rect(center=self._rect.center)

        surface.blit(self._swordsurface,self._rect)

    def get_rect(self):
        return self._rect
    #once the sword actually hits something, it will turn into a pickupable object
    def hit_object(self):
        self._isActive = False
        Sword_ENT(self._posx, self._posy,self._floorh,self._floory,self._window)

    #read only methods
    @staticmethod
    def print_entities():
        return Entity.sword_entities

    @staticmethod
    def append_entities(entity):
        Entity.sword_entities.append(entity)
