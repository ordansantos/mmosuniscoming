
import pygame
from pygame.locals import *
import Screen
import Person
import Sun
import Bot
import Sound
import PathFind
from collections import deque
import sys

class Game:
    
    def __init__(self, screen, width, height, master_name='Master Example', character_path='../characters/sprites/ordan.png'):
        
        self.mouse_pos_right_click = None
        
        self.width = width
        self.height = height

        self.clock = pygame.time.Clock()
        self.frame = Screen.Screen(screen, width, height)
        self.txt = self.frame.txt
        
        self.sound = Sound.Sound()
        
        self.arrow_states = {
            K_UP: [False, -1],
            K_DOWN: [False, 1],
            K_LEFT: [False, -1],
            K_RIGHT: [False, 1],
        }
        
        self.arrow = [0, 0]
        
        self.sun = Sun.Sun()
        
        self.p = Person.Person.getNewPlayer(733, 896, master_name, character_path)
        
        Person.Person.setMaster(self.p.getId())
        self.path_deque = deque()
        
        # Bot.BotController.putNewBot((1700, 1700), '../characters/skeleton.png')
        Bot.BotController.putNewBot ((912, 482), '../characters/sprites/black_man.png')
        
        Bot.BotController.putNewBot ((739, 498), '../characters/sprites/blond_man.png')
        Bot.BotController.putNewBot ((935, 602),  '../characters/sprites/dumb_woman.png')
        Bot.BotController.putNewBot ((981, 633), '../characters/sprites/blond_man.png')
        Bot.BotController.putNewBot ((975, 597), '../characters/sprites/blond_woman.png')
        Bot.BotController.putNewBot ((1029, 622), '../characters/sprites/brunette_woman.png')
    
        # Bot.BotController.putNewBot((600, 800))
        # Bot.BotController.putNewBot((1000, 2000))
        
        """ self.client = ClientSocket.ClientSocket() """
    
    def run(self):
        
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
        
        self.sound.backgroundPlay()
        died = False
        
        while True:
            
            self.clock.tick(30)
            
            if self.p.life != 0:
            
                # handle events
                switch = self.doEvent()
                
                pygame.event.pump()
                
                if switch == 'ESCAPE':
                    self.sound.stopAll()
                    return 'ESCAPE'
                elif switch == 'QUIT':
                    self.sound.stopAll()
                    return 'QUIT'
                
                # update title
                pygame.display.set_caption('%d %d - Sun Is Coming - Master(%d)' %(self.p.x, self.p.y, self.p.life))
                
                # draw frame
                self.frame.draw(self.p, self.sun)
                
                # update player
                self.p.updateDeath(self.sun.getPeriod())
                transform = self.p.updateTransform()
                
                # update sound
                self.sound.updateBackground(transform)

                # move player
                if (len(self.path_deque)):
                    x1, y1 = self.path_deque.popleft()
                    self.p.doAMovement((x1, y1))
                else:
                    self.p.move(self.arrow)
                
            else: # if player died...
                time = pygame.time.get_ticks()
                if died == False:
                    self.txt.updateReaderMessage(self.p.name + ' died!')
                    time_died = time
                    died = True
                if time - time_died < 1500:
                    self.frame.draw(self.p, self.sun)
                else:
                    self.sound.stopAll()
                    return 'DIED'

            
            '''client_event = self.client.get()
            
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_LEFT:
                        self.client.sendMovement("left")
                    if e.key == K_RIGHT:
                        self.client.sendMovement("right")
                    if e.key == K_DOWN:
                        self.client.sendMovement("down")
                    if e.key == K_UP:
                        self.client.sendMovement("up")

            for e in client_event['moves']:
                if e == 'up':
                    self.p.up()
                if e == 'down':
                    self.p.down()
                if e == 'left':
                    self.p.left()
                if e == 'right':
                    self.p.right()'''
                
    def doEvent(self):
        
        # close game
        if pygame.event.peek(QUIT):
            pygame.quit()
            return 'QUIT'
        
        events = pygame.event.get()
        
        for e in events:
            
            # return menu
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return 'ESCAPE'
            
            # check click and get mouse position
            self.clicked(e)
            mouse_pos = pygame.mouse.get_pos()

            if (pygame.mouse.get_pressed()[2]):
                self.mouse_pos_right_click = mouse_pos

            if (not pygame.mouse.get_pressed()[2] and self.mouse_pos_right_click != None):
                self.updateMovementPath(self.mouse_pos_right_click)
                self.mouse_pos_right_click = None
            
            # handle writer box
            if self.txt.writing_now and self.arrow == [0, 0]:
                message = self.txt.handleWriterBox(events)
                if message != None:
                    full_nome = unicode('[' + self.p.name + ']: ', 'utf8')
                    full_message = full_nome + message
                    self.txt.updateReaderMessage(full_message)
            
            else:
                
                # handle reader box
                self.txt.handleReaderBox(e)
                
                # handle character movement
                if e.type == KEYUP:
                    
                    if (len(self.path_deque)):
                        self.p.stopped
                        self.path_deque.clear()
                        
                    if e.key in self.arrow_states.keys():
                        self.arrow_states[e.key][0] = False
                        self.updateArrows()
                    
                    if e.key == K_LSHIFT:
                        self.p.updateSpeed(False)
                
                elif e.type == KEYDOWN:
                    
                    if (len(self.path_deque)):
                        self.p.stopped
                        self.path_deque.clear()
                        
                    if e.key in self.arrow_states.keys():
                        self.arrow_states[e.key][0] = True
                        self.updateArrows()
                    
                    if e.key in self.p.attack_keys.keys():
                        self.p.attack(e.key)
                    
                    if e.key == K_LSHIFT:
                        self.p.updateSpeed(True)
        
        return 'NEXT'
    
    def clicked(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.txt.updateWriting()
        return True
    
    def updateArrows(self):
        self.arrow = [0, 0]
        if self.arrow_states[K_UP][0]:
            self.arrow[1] += self.arrow_states[K_UP][1]
        if self.arrow_states[K_DOWN][0]:
            self.arrow[1] += self.arrow_states[K_DOWN][1]
        if self.arrow_states[K_LEFT][0]:
            self.arrow[0] += self.arrow_states[K_LEFT][1]
        if self.arrow_states[K_RIGHT][0]:
            self.arrow[0] += self.arrow_states[K_RIGHT][1]
    
    def updateMovementPath(self, mouse_pos):
        x, y = self.frame.getMousePositionOnMap(self.p, mouse_pos)
        self.path_deque = PathFind.PathFind.getPath (self.p.getPosition(), (x, y), True)
        
