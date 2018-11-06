'''
Class that handles all character stuff, such as movement, and actions. many variables...
NICK TKACHOV
'''
import pygame
import math
from pygame.locals import *
#imports sprites and entities
from .entities import Entity,Sword_ENT,Body_ENT,FSword_ENT
from .sprites import CustomSprites
class Character():
    #constructs character, with name specified
    
    def __init__(self,name,color,window_obj,floory,floorh,AI,target=None):
        self._name = name
        #variable declaration
        if target is not None:
            self._target = target
        self._ai = AI
        if self._ai:
            self.xcor =550
            self.ycor = 250
            self._direction = 'left'
        else:
            self.xcor = 50
            self.ycor = 250
            self._direction = 'right'
        self._alive = True
        self.color = color
        self._window = window_obj
        self._floory = floory
        self._floorh = floorh
        self._isjumping = False
        self._isattacking = False
        self._last = pygame.time.get_ticks()
        self._speed = 4
        self.height = 80
        self.have_sword = True
        self._realheight = 70
        self.width = 60
        self._swordh = 7
        self._swordposextraX = 60
        self._swordw = 80
        self._swordx = self.xcor + self._swordposextraX
        self._swordpos = 0
        self._sworddict = [-5,10,30]
        self._debug = False
        self._swordposextra = 10
        self._jumpindex = 0
        self._extracrouch = 0
        self._jumptab = [int(math.cos(math.radians(x)) * 15) for x in range(0, 181, 10)]
        self._attacktab = [int(math.cos(math.radians(x)) * 30) for x in range(0, 181, 10)]
        self._attackindex = 0
        self._queue = False
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self._raised = False
        self._crouch = False
        self._ismoving = False
        self.sword_active = []
        self._animposition = 0
        #creates the hitbox and floor, that will be used for collision
        self._floor = pygame.Rect(0,self._floory,self._window.get_width(),self._floorh)
        self.hitbox = pygame.Rect(self.xcor,self.ycor + self._extracrouch,self.width,self.height)
        self.swordbox = pygame.Rect(self._swordx,self.ycor + self._swordposextra,self._swordw,self._swordh)
        self.neutralbox = pygame.Rect(self.xcor,self.ycor,190,120)

        #sprite creation
        #-------------------------------
        self.idle_up = CustomSprites(['anim_up/player1-1.png','anim_up/player1-2.png','anim_up/player1-3.png','anim_up/player1-4.png'],self.neutralbox)
        self.idle_down = CustomSprites(['anim_down/player1-1.png','anim_down/player1-2.png','anim_down/player1-3.png','anim_down/player1-4.png'],self.neutralbox)
        self.idle_neutral = CustomSprites(['anim_neut/player1-1.png','anim_neut/player1-2.png','anim_neut/player1-3.png','anim_neut/player1-4.png'],self.neutralbox)

        self.moving_crouch = CustomSprites(['crouch/crouch-1.png','crouch/crouch-2.png','crouch/crouch-3.png','crouch/crouch-4.png'],self.neutralbox)
        self.idle_naked = CustomSprites(['idle_naked/player-1.png','idle_naked/player-2.png','idle_naked/player-3.png','idle_naked/player-4.png'],self.neutralbox)
        self.idle_crouch = CustomSprites(['crouch-1.png'],self.neutralbox)

        self.idle_jump = CustomSprites(['jumping.png'],self.neutralbox)

        self.moving_anim = CustomSprites(['moving/player-1.png','moving/player-2.png','moving/player-3.png','moving/player-4.png'],self.neutralbox)

        self.moving_sword_anim = CustomSprites(['moving_sword/player-1.png','moving_sword/player-2.png','moving_sword/player-3.png','moving_sword/player-4.png'],self.neutralbox)

        self.idle_aiming = CustomSprites(['aiming.png'],pygame.Rect(self.neutralbox))

        self.hit_top = CustomSprites(['attack_top.png'],pygame.Rect(self.neutralbox))
        self.hit_middle = CustomSprites(['attack_middle.png'],pygame.Rect(self.neutralbox))
        self.hit_bottom = CustomSprites(['attack_bottom.png'],pygame.Rect(self.neutralbox))

        self.idle_up_group = pygame.sprite.Group(self.idle_up)
        self.idle_down_group = pygame.sprite.Group(self.idle_down)
        self.idle_neutral_group = pygame.sprite.Group(self.idle_neutral)
        self.idle_crouch_group = pygame.sprite.Group(self.idle_crouch)
        self.idle_aiming_group = pygame.sprite.Group(self.idle_aiming)
        self.idle_naked_group = pygame.sprite.Group(self.idle_naked)
        self.move_group = pygame.sprite.Group(self.moving_anim)

        self.move_sword_group = pygame.sprite.Group(self.moving_sword_anim)

        self.idle_jumping_group = pygame.sprite.Group(self.idle_jump)

        self.moving_crouch_group = pygame.sprite.Group(self.moving_crouch)
        #----------------------------------
        #sprite creation finished

        self.sprite_groups = [self.idle_up_group,self.idle_neutral_group,self.idle_down_group,self.idle_crouch_group,self.idle_aiming_group,self.moving_crouch_group,self.idle_jumping_group,self.idle_naked_group,self.move_group,self.move_sword_group,pygame.sprite.Group(self.hit_top),pygame.sprite.Group(self.hit_middle),pygame.sprite.Group(self.hit_bottom)]
    def draw(self,surfaceObj):
        #draw image for character
        if self._alive:
            if self._debug:
                pygame.draw.rect(surfaceObj,(255,255,255),self.hitbox)
                pygame.draw.rect(surfaceObj,(255,255,255),self.swordbox)
            else:
                pass
    def _update(self):
        #update all character necessities
        if self._alive:
            if self._ai:
                self.BOT(1,self._target)
            self._swordposextra = self._sworddict[self._swordpos]
            self.moving = self.move_left,self.move_right
            self.sword_active = self.move_left,self.move_right,self._crouch,self._isjumping,self.move_down,self._raised
            if True not in self.moving:
                self._ismoving = False
            else:
                self._ismoving = True

            self._swordx = self.xcor + self._swordposextraX
            self.movement()
            #if char is jumping, move character using a parabola
            if self._isjumping:
                self.ycor -= self._jumptab[self._jumpindex]
                self._animposition = 6
                self.height = 40
                if self._jumpindex >= len(self._jumptab)-1:
                    self._jumpindex = 0
                    self.height = 80
                    self._isjumping = False
                    self._now = pygame.time.get_ticks()
                else:
                    self._jumpindex +=1
            else:
                self.gravity()

            #sets animation positions to use the correct sprite
            if not self._crouch and not self._isattacking and not self._raised and not self._isjumping:
                if self.have_sword:
                    if self._ismoving:
                        self._animposition = 9
                    else:
                        self._animposition = self._swordpos
                else:
                    if self._ismoving:
                        self._animposition = 8
                    else:
                        self._animposition = 7

            #does attacking by moving the hitbox using a parabola
            if self._isattacking:
                try:
                    self._swordx += self._attacktab[self._attackindex]
                except:
                    self._isattacking = False
                    self._attackindex = 0
                    self._now = pygame.time.get_ticks()
                self._animposition = 10 + self._swordpos
                if self._direction == 'right':
                    self.xcor += 1.2
                elif self._direction == 'left':
                    self.xcor -= 1
                if self._attackindex >= len(self._attacktab)-1:
                    self._attackindex = 0
                    self._isattacking = False
                    self._now = pygame.time.get_ticks()
                else:
                    self._attackindex +=1
            if self._crouch:
                self.sword_entities = Sword_ENT.print_entities()
                if self._ismoving:
                    self._animposition = 5
                else:
                    self._animposition = 3
                for z in self.sword_entities:
                    if self.get_hitbox() is not None and self.get_hitbox().colliderect(z.get_rect()) and not self.have_sword:
                        z.pick_up()
                        self.have_sword = True

            if self._raised and self.have_sword:
                self._animposition = 4
            else:
                self._raised = False
            if self._direction == 'right':
                self._swordposextraX = 60
                self._attacktab = [int(math.cos(math.radians(x)) * 50) for x in range(0, 260, 30)]
            elif self._direction == 'left':
                self._swordposextraX = -90
                self._attacktab = [-int(math.cos(math.radians(x)) * 50) for x in range(0, 260, 30)]

            self.sprite_groups[self._animposition].update(self.xcor,self.ycor,self._direction)
            self.sprite_groups[self._animposition].draw(self._window)

            
            #redraw the hitboxes and character
            self.hitbox = pygame.Rect(self.xcor,self.ycor + self._extracrouch,self.width,self.height + 20)
            self.swordbox = pygame.Rect(self._swordx,self.ycor + self._swordposextra,self._swordw,self._swordh)
        else:
            #if player is dead, count down
            self._now = pygame.time.get_ticks()
            if self._now - self._last >= 3000:
                self._last = pygame.time.get_ticks() 
                self._alive = True
                self.have_sword = True
                if self._ai:
                    self.xcor =550
                    self.ycor = 250
                    self._direction = 'right'

                else:
                    self.xcor = 50
                    self.ycor = 250
                    self._direction = 'right'
                self.hitbox = pygame.Rect(self.xcor,self.ycor + self._extracrouch,self.width,self.height + 20)
                self.swordbox = pygame.Rect(self._swordx,self.ycor + self._swordposextra,self._swordw,self._swordh)
                self.move_left = False
                self.move_right = False
        
    #kills player
    def death(self,window_obj):
        self._last = pygame.time.get_ticks() 
        self._alive = False
        Body_ENT(self.xcor,self.ycor,self._floorh,self._floory,self._window,(255,0,0))
        
    #pushes player away, from another player or a border
    def push(self,amount):
        if self._direction == 'left':
            self.xcor +=amount
        elif self._direction == 'right':
            self.xcor -=amount
    #removes sword once you throw it
    def sword_knockout(self):
        if self.have_sword:
            self.have_sword = False
            Sword_ENT(self.xcor,self.ycor,self._floorh,self._floory,self._window)

    #gets sword hitbox
    def get_sword(self):
        if self.have_sword:
            if self._isattacking or True not in self.sword_active:
                return self.swordbox
            else:
                return None
        else:
            return None

    #gets hitbox of char
    def get_hitbox(self):
        if self._alive:
            return self.hitbox
        else:
            return None

    #picks up sword
    def sword_pickup(self,entity):
        Sword_ENT.remove_entities(entity)

    #property used for checking if player is alive 
    def isAlive(self):
        return self._alive

    #gravity, if character happens to be in the air            
    def gravity(self):
        if not self._floor.colliderect(self.hitbox):
            self.ycor +=10
            if self.ycor >= 1000:
                self.death(self._window)

    #update the person that the character is targeting
    def update_target(self,rect):
        self._target = rect

    def get_current_rect(self):
        return self.hitbox

    #throw the sword
    def throw_sword(self,direction):
        if self.have_sword:
            self.have_sword = False
            FSword_ENT(self._swordx,self.ycor + self._swordposextra - self._swordw/2,self._floorh,self._floory,self._window,direction,not self._ai,self._target)
    
    #this is where the values from the main() class are handled
    def movement(self):
        if self.move_left and not self._isattacking:
            self.xcor -= self._speed
            self._direction = 'left'
            
        if self.move_right:
            self.xcor += self._speed
            self._direction = 'right'

        if self.move_up and not self._isattacking:
            self._now = pygame.time.get_ticks()
            if self.have_sword:
                if self._swordpos >= 1  and self._now - self._last >= 100:
                    self._last = pygame.time.get_ticks()  
                    self._swordpos -=1
                elif self._swordpos == 0:
                    self.raise_sword(True)
        else:
            self.raise_sword(False)

        if self.move_down and not self._isattacking:
            self._now = pygame.time.get_ticks()
            if not self.have_sword:
                self.crouch(True)
            else:
                if self._swordpos <= 1  and self._now - self._last >= 100:
                    self._last = pygame.time.get_ticks()    
                    self._swordpos +=1
                elif self._swordpos == 2:
                     self.crouch(True)
        else:
             self.crouch(False)

    #stuff
    def raise_sword(self,state):
        if state:
            self._raised = True
            self._swordposextra = -20
        else:
            self._animposition = self._swordpos
            self._raised = False
    
    #crouches character and also moves the hitbox to make it realistic
    def crouch(self,state):
        if state:
            self._crouch = True
            self.height = 40
            self._speed = 2
            self._extracrouch = self.height
        else:
            self._crouch = False
            self.height = self._realheight
            self._speed = 4
            self._extracrouch = 0

    #jump with cooldown
    def move_jump(self):
        self._now = pygame.time.get_ticks()
        if not self._isjumping and self._floor.colliderect(self.hitbox) and self._now - self._last >= 500 and not self._isattacking:
            self._last = pygame.time.get_ticks()
            self._isjumping = True
            
    #attack with cooldown
    def attack(self):
        self._now = pygame.time.get_ticks()
        if True not in self.sword_active and self._now - self._last >= 300 and not self._isattacking and self.have_sword:
            self._last = pygame.time.get_ticks()    
            self._isattacking = True
        elif self._raised:
            self.throw_sword(self._direction)

    def BOT(self,difficulty,target):
        #john
        pass
        
