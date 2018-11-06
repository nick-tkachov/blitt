#imports essential libraries
import pygame
from sys import exit
from pygame import time
import library
from pygame.locals import *
from .config import config,p1_controls,p2_controls
from .button import Button
from .char import Character
from .entities import Entity,Sword_ENT,Body_ENT
from .file_io import File
from .font import Font
pygame.init()
BLACK = (10,10,10)
WHITE = (255,255,255)

class Game():
    #initialises game
    def __init__(self):
        #reads config to give control keys to players
        #messy variables
        self.config = config()
        self.p1_controls = p1_controls()
        self.p2_controls = p2_controls()
        self.main_buttons = 2
        self.isinmenu = True
        self.isinmainmenu = True
        self._debug = False
        self._leaderboard = False
        self._isselecting = False
        self._score1 = 0
        self._endgame = False
        self._score2 = 0
        self._winnername = []
        self._scores = []
        self._winscore = 3
        self.framespersecond = 60

        self._mfont = pygame.font.SysFont('Monospace',30)
        self._mfont.set_bold(True)
        #creates clock
        self.timer = time.Clock()

        #creates display
        self.game_window = pygame.display.set_mode((640,480))
        self.game_window.fill(BLACK)
        pygame.display.set_icon(pygame.image.load('./assets/game/attack_middle.png'))
        pygame.display.set_caption('blitt v1.0')

        #creates text that will be drawn on screen
        self.p1_text = Font(('PLAYER 1: '+ str(self._score1)),WHITE,30,'left',100)
        self.p2_text = Font(('PLAYER 2: '+ str(self._score2)),WHITE,30,'right',100)
        self.winner_text = Font('WINNER! ENTER NAME!',WHITE,30,'center',100)
        self.title = Font('BLITT',WHITE,75,'center',70)
        self.selecting = Font('Select Game Mode',WHITE,30,'center',120)
        self.winner_name = Font(str(''.join(self._winnername)),WHITE,30,'center',200)

        self.target = pygame.Rect(0,0,0,0)

        #creates players using classes
        self.player1 = Character('Player1',(255,0,0),self.game_window,430,50,False,self.target)
        self.player2 = Character('Player2',(255,0,0),self.game_window,430,50,True,self.target)
        
        self.players = [self.player1,self.player2]
        
        #loads images or tries to
        try:
            self.button_default = pygame.image.load('./assets/menu/button_default.png')
            self.button_highlight = pygame.image.load('./assets/menu/button_select.png')
        except:
            print('Could not load images!')

        #creates buttons that will be used for menu
        self.leaderboard_button = Button(0,'LEADERBOARDS',234,self.button_highlight,self.button_default,pygame.Rect(215,440,200,25))
        self.play_button = Button(0,'PLAY',234,self.button_highlight,self.button_default,pygame.Rect(245,180,150,37))
        self.option_button = Button(1,'SETTINGS',234,self.button_highlight,self.button_default,pygame.Rect(245,240,150,40))
        self.quit_button = Button(2,'QUIT',234,self.button_highlight,self.button_default,pygame.Rect(245,300,150,40))
        self.ok_button = Button(0,'OK',234,self.button_highlight,self.button_default,pygame.Rect(245,300,150,37))
        self.back_button = Button(0,'BACK',234,self.button_highlight,self.button_default,pygame.Rect(245,420,150,37))
        self.bo5 = Button(0,'BO5',234,self.button_highlight,self.button_default,pygame.Rect(245,180,150,37))
        self.bo7 = Button(1,'BO7',234,self.button_highlight,self.button_default,pygame.Rect(245,240,150,40))
        self.bo9 = Button(2,'BO9',234,self.button_highlight,self.button_default,pygame.Rect(245,300,150,40))

        self.ui = [self.option_button,self.play_button,self.quit_button,self.leaderboard_button,self.title]
        self._floor = pygame.Rect(0,440,self.game_window.get_width(),50)
        self.sword_entities = []

    #draws level(its only a floor)
    def draw_level(self):
        if not self.isinmenu:
            pygame.draw.rect(self.game_window,(105,105,105),self._floor)

    #checks when winner is found
    def get_winner(self):
        if self._score1 >= self._winscore or self._score2 >= self._winscore:
            self._endgame = True
            self.isinmenu = True
            self.ui = [self.ok_button,self.winner_name,self.winner_text]
    
    #draws leaderboard
    def leaderboard(self):
        self.ui = []
        #opens file using a custom class
        self._highscores = File('highscores.txt')
        self._scores = self._highscores.open_files()
        for i,v in enumerate(self._scores):
            self.ui.append(Font(str(i+1) +'. '+v,(255,255,255),30,'center',50 * (i+1)))
        self.ui.append(self.back_button)

    #starts the game
    def start_game(self,bo):
        self._winscore = bo
        self.ui = [self.p2_text,self.p1_text]
        self.isinmenu = False

    #new game
    def new_game(self):
        self._endgame = False
        self.isinmenu = True
        self._highscores = File('highscores.txt')
        self._highscores.write_to(self.winner_name.get_text())
        self._winnername = []
        self.game_window.fill(BLACK)
        self.ui = [self.option_button,self.play_button,self.quit_button,self.leaderboard_button,self.title]
        self._score1 = 0
        self._score2 = 0

    #prints all options when settings are pressed
    def draw_options(self):

        print('PLAYER1')
        print('-------------')
        print('FORWARD: D')
        print('BACKWARD: A')
        print('UP: W')
        print('DOWN: S')
        print('ATTACK: F')
        print('JUMP: G')
        print('=============')
        print('PLAYER2')
        print('-------------')
        print('FORWARD: RARROW')
        print('BACKWARD: LARROW')
        print('UP: UPARROW')
        print('DOWN: DOWNARROW')
        print('ATTACK: NUMPAD 0')
        print('JUMP: DEL ON NUMPAD')
        print('=================================')
        print('HOW TO PLAY: USE UP AND DOWN KEYS TO CYCLE BETWEEN SWORD HEIGHT, HOLD UP AND PRESS ATTACK TO THROW THE SWORD AND HOLD DOWN TO CROUCH')
        print('TO DEFEAT THE OPPONENT YOUR SWORD MUST TOUCH THEM, WHILE FLYING OR WHILE IN YOUR HAND')
        print('GOOD LUCK')

    #shuts down the game
    def shutdown(self):
        pygame.quit()
        exit()

    #the main loop of the game
    def main_loop(self):
        while 1:
            self.game_window.fill(BLACK)   
            #all sorts of collision checks (sword-2-sword,player-2-sword,sword-2-player)
            if self.player1.get_sword() is not None and self.player2.get_hitbox() is not None:
                if self.player1.get_sword().colliderect(self.player2.get_hitbox()) and self.player1.isAlive() and self.player2.isAlive():
                    self.player2.death(self.game_window)
                    self._score1 +=1
            if self.player2.get_sword() is not None and self.player1.get_hitbox() is not None:
                if self.player2.get_sword().colliderect(self.player1.get_hitbox()) and self.player2.isAlive() and self.player1.isAlive():
                     self.player1.death(self.game_window)
                     self._score2 +=1
            if self.player1.get_sword() is not None and self.player2.get_sword() is not None:
               if self.player2.get_sword().colliderect(self.player1.get_sword()) and self.player2.isAlive() and self.player1.isAlive():
                   self.player2.push(3)
                   self.player1.push(3)
            for v in self.players:
                if v.get_hitbox() is not None:
                    if v.xcor >= self.game_window.get_width() - 60 or v.xcor <=0 :
                        v.push(7)
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()
                #if player is holding down a key
                if event.type == KEYDOWN or event.type == KEYUP:
                    key_state = (event.type == KEYDOWN)
                    
                    #checks if players are alive
                    if self.players[0].isAlive(): 
                        #checks for key presses, then sends those key checks to the class to proccess
                        if event.key == self.p1_controls.k_d:
                            self.players[0].move_right = key_state
                        elif event.key == self.p1_controls.k_a:
                            self.players[0].move_left = key_state
                        elif event.key == self.p1_controls.k_w:
                            self.players[0].move_up = key_state
                        elif event.key == self.p1_controls.k_s:
                            self.players[0].move_down = key_state
                        elif event.key == self.p1_controls.k_jump:
                            self.players[0].move_jump()
                        elif event.key == self.p1_controls.k_attack:
                            self.players[0].attack()
                    if self.players[1].isAlive():
                        #same as above
                        if event.key == self.p2_controls.k_d:
                            self.players[1].move_right = key_state
                        elif event.key == self.p2_controls.k_a:
                            self.players[1].move_left = key_state
                        elif event.key == self.p2_controls.k_w:
                            self.players[1].move_up = key_state
                        elif event.key == self.p2_controls.k_s:
                            self.players[1].move_down = key_state
                        elif event.key == self.p2_controls.k_jump:
                            self.players[1].move_jump()
                        elif event.key == self.p2_controls.k_attack:
                            self.players[1].attack()

                if event.type == KEYDOWN:
                    if event.key == self.config.k_escape:
                        self.shutdown()
                    #if someone got to the score first
                    if self._endgame:
                        #allows to enter the name
                        if event.key == self.config.k_backspace:
                            if len(self._winnername) > 0:
                                del self._winnername[-1]
                        elif not len(self._winnername) >=10:
                            self._winnername.append(chr(event.key))
                    #for testing purposes
                    if self._debug:
                        if event.key == K_m:
                            self.players[0].sword_knockout()
                        elif event.key == K_n:
                            self.players[0].death(self.game_window,self.players[0].xcor,self.players[0].ycor)
                #if person lets go of mouse click(to click on buttons)
                if event.type == MOUSEBUTTONUP:
                    if self._endgame:
                        if self.ok_button._rect.collidepoint(event.pos):
                            self.new_game()
                    elif self._isselecting:
                        #all the buttons for the menus
                        if self.bo5._rect.collidepoint(event.pos):
                            self.start_game(5)
                        elif self.bo7._rect.collidepoint(event.pos):
                            self.start_game(7)
                        elif self.bo9._rect.collidepoint(event.pos):
                            self.start_game(9)
                        elif self.back_button._rect.collidepoint(event.pos):
                            self.ui = [self.option_button,self.play_button,self.quit_button,self.leaderboard_button,self.title]
                            self._isselecting = False
                    #buttons for another menu
                    elif self.isinmenu:
                        if self.play_button._rect.collidepoint(event.pos):
                            self.ui = [self.bo5,self.bo7,self.bo9,self.back_button,self.selecting]
                            self._isselecting = True
                        elif self.option_button._rect.collidepoint(event.pos):
                            self.draw_options()
                        elif self.leaderboard_button._rect.collidepoint(event.pos):
                            self.leaderboard()
                        elif self.back_button._rect.collidepoint(event.pos):
                            self.ui = [self.option_button,self.play_button,self.quit_button,self.leaderboard_button,self.title]
                        elif self.quit_button._rect.collidepoint(event.pos):
                            self.shutdown()
                #allows the hovering thing to happen
                if event.type == MOUSEMOTION:
                    for i in self.ui:
                        if not i.is_text():
                            if i._rect.collidepoint(event.pos):
                                i.mouse_hover(event)
                            else:
                                i.mouse_unhover(event)
                           
            self.get_winner()
            self.update()
            pygame.display.update()
            self.timer.tick(self.framespersecond)
            self.fps = round(self.timer.get_fps())
    def update(self):
        #this is where the sprites and characters are updated
        #gets entities from the classes
        self.sword_entities = Sword_ENT.print_entities()
        self.body_entities = Body_ENT.print_entities()
        self.draw_level()
        
        #checks if any entities exist
        if len(self.sword_entities) != 0 and not self.isinmenu and not self._endgame:
            for x in self.sword_entities:
                if x.isActive():
                    if x.get_player():
                        #checks for entity collision
                        x.update(self.player2.get_current_rect())
                        if x.get_rect() is not None and self.player2.get_hitbox() is not None:
                            if x.get_rect().colliderect(self.player2.get_hitbox()) and not x.isItem():
                                x.hit_object()
                                self.player2.death(self.game_window)
                                self._score1 +=1
                        elif self.player2.get_sword() is not None and x.get_rect().colliderect(self.player2.get_sword()):
                            x.hit_object()
                    elif not x.get_player():
                        #another entity collision
                        x.update(self.player1.get_current_rect())
                        if x.get_rect() is not None and self.player1.get_hitbox() is not None:
                            if x.get_rect().colliderect(self.player1.get_hitbox()) and not x.isItem():
                                    x.hit_object()
                                    self.player1.death(self.game_window)
                                    self._score2 +=1
                            elif self.player1.get_sword() is not None and x.get_rect().colliderect(self.player1.get_sword()):
                                 x.hit_object()
                else:
                    Sword_ENT.remove_entities(x)
        
        #updates body entities
        if len(self.body_entities) != 0 and not self._endgame and not self.isinmenu:
            for b in self.body_entities:
                b.update(True)

        #updates UI using a table, which is always updated
        for v in self.ui:
            if v.is_text():
                pass
            v._update()
            v.draw(self.game_window)

        #updates the players
        for v in self.players:
            if not self.isinmenu:
                v._update()
                v.draw(self.game_window)

        #updates text
        self.p1_text.update_text(('PLAYER 1:  '+ str(self._score1)))
        self.p2_text.update_text(('PLAYER 2:  '+ str(self._score2)))
        self.winner_name.update_text(''.join(self._winnername))