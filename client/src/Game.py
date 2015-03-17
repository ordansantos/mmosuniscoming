
import pygame
from pygame.locals import *
import Screen
import Person
import Sun
import Sound
import ClientSocket
import PathFind
from collections import deque
import sys

class Game:
    
    def __init__(self, screen, width, height, path_image):
        
        Person.Person.image =  path_image
        
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
        
        self.path_deque = deque()
        
        self.client = ClientSocket.ClientSocket(self.txt)
        
        thread_client = ClientSocket.ClientConnection(kwargs={'client': self.client})
        thread_client.setDaemon(True)
        thread_client.start()

        
        self.p = Person.Person.getMaster()

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
                    self.client.close = True
                    
                    return 'ESCAPE'
                elif switch == 'QUIT':
                    self.sound.stopAll()
                    self.client.close = True
                    return 'QUIT'
                
                # update title
                pygame.display.set_caption('%d %d - Sun Is Coming - Master(%d)' %(self.p.x, self.p.y, self.p.life))
                
                # draw frame
                self.frame.draw(self.p, self.sun)
                
                # update player
                #print self.p.id
                
                self.p.updateDeath(self.sun.getPeriod())
                transform = self.p.updateTransform()
                
                # update sound
                self.sound.updateBackground(transform)

                # move player
                if (len(self.path_deque)):
                    x1, y1 = self.path_deque.popleft()
                    x, y = self.p.getPosition()
                    
                    if (x1 > x):
                        if (y1 > y):
                            if (self.p.downRight()):
                                self.client.q_moves.put ('dr')
                        elif (y1 < y):
                            if (self.p.upRight()):
                                self.client.q_moves.put ('ur')
                        else:
                            if (self.p.right()):
                                self.client.q_moves.put ('r')
            
                    elif (x1 < x):
                        if (y1 > y):
                            if (self.p.downLeft()):
                                self.client.q_moves.put ('dl')
                        elif (y1 < y):
                            if (self.p.upLeft()):
                                self.client.q_moves.put ('ul')
                        else:
                            if (self.p.left()):
                                self.client.q_moves.put ('l')
            
                    else:
                        if (y1 > y):
                            if (self.p.down()):
                                self.client.q_moves.put ('d')
                        elif (y1 < y):
                            if (self.p.up()):
                                self.client.q_moves.put ('u')
                else:
                    #self.p.move(self.arrow)
                    self.client.setMovementEvent(self.arrow)
                    
            else: # if player died...
                time = pygame.time.get_ticks()
                
                self.client.close = True
                
                if died == False:
                    died_time = time
                    self.txt.updateReaderMessage(self.p.name + ' died!')
                    died = True
                if time - died_time < 1500:
                    self.frame.draw(self.p, self.sun)
                else:
                    self.sound.stopAll()
                    
                    return 'DIED'
    
    
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
                    full_nome = unicode('[' + str(self.p.name) + ']: ', 'utf8')
                    full_message = full_nome + message
                    self.client.setMessage(full_message)
                 
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
                        #self.p.attack(e.key)
                        self.client.setAttack(e.key)
                    #if e.key == K_LSHIFT:
                    #    self.p.updateSpeed(True)
        
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
        
