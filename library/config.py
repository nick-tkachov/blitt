'''
config for the game, simply just property classes so no variables were used
NICK TKACHOV
'''
import pygame
from pygame.locals import *

class config():
    
    def __init__(self,up=K_w,down=K_s,left=K_a,right=K_d,dodge=K_SPACE,enter=K_RETURN,escape=K_ESCAPE):
        pass
    @property
    def k_escape(self):
        return K_ESCAPE
    @property
    def k_enter(self):
        return K_ENTER
    @property
    def k_backspace(self):
        return K_BACKSPACE

class p1_controls():
    
    def __init__(self,up=K_w,down=K_s,left=K_a,right=K_d,dodge=K_SPACE,enter=K_RETURN,escape=K_ESCAPE):
        pass
    @property
    def k_w(self):
        return (K_w)
    @property
    def k_s(self):
        return (K_s)
    @property
    def k_a(self):
        return (K_a)
    @property
    def k_d(self):
        return (K_d)
    @property
    def k_escape(self):
        return K_ESCAPE
    @property
    def k_enter(self):
        return K_ENTER
    @property
    def k_jump(self):
        return K_g
    @property
    def k_attack(self):
        return K_f
    
class p2_controls():
    
    def __init__(self,up=K_w,down=K_s,left=K_a,right=K_d,dodge=K_SPACE,enter=K_RETURN,escape=K_ESCAPE):
        pass

    @property
    def k_w(self):
        return (K_UP)
    @property
    def k_s(self):
        return (K_DOWN)
    @property
    def k_a(self):
        return (K_LEFT)
    @property
    def k_d(self):
        return (K_RIGHT)
    @property
    def k_jump(self):
        return K_KP_PERIOD
    @property
    def k_attack(self):
        return K_KP0
    
