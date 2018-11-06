import pygame
from pygame.locals import *

class CustomSprites(pygame.sprite.Sprite):

    def __init__(self,images_values,rect):
        super(CustomSprites, self).__init__()
        self.image_table = images_values
        self.images = []
        self.rect = rect
        self.index = 0
        self._width = self.rect.width
        self._height = self.rect.height
        for i in self.image_table:
            self.images.append(self.load_image('./assets/game/'+ i))
        self._flipoffset = 35
        self.image = pygame.transform.scale(self.images[self.index],(self._width,self._height))
        self.timer = 0

    def load_image(self,name):
        self.sprite = pygame.image.load(name)
        self.sprite_transform = pygame.transform.scale(self.sprite,(self._width,self._height))
        return self.sprite_transform

    def update(self,x,y,direction):
        self.rect.x = x - self._flipoffset
        self.direction(direction)
        self.rect.y = (y - 30)
        self.timer += 1
        if self.timer == 5:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            if direction == 'left':
                self.image = pygame.transform.flip(self.images[self.index],True,False)
            elif direction =='right':
                self.image = pygame.transform.flip(self.images[self.index],False,False)

            #self.image = pygame.transform.scale(self.images[self.index],(self._width,self._height))
    def direction(self,direction):
        if direction == 'left':
            self._flipoffset = 90
        elif direction == 'right':
            self._flipoffset = 35