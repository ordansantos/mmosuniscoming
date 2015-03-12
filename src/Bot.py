
import Person
from collections import deque
import pygame
import threading
import PathFind

import random
import Walls
from Character import Bot

class BotController:
    
    @staticmethod
    def putNewBot ( (x, y), image = '../characters/sprites/black_man.png' ):
        
        person = Person.Person.getNewBot(x, y, image)
        
        person_bot = BotThread(kwargs={'person': person})
        person_bot.setDaemon(True)
        person_bot.start()

class BotThread(threading.Thread):
    
    def run(self):
        self.last_tick = 0
        self.p = self._Thread__kwargs['person']
        self.path_deque = deque()
        self.clock = pygame.time.Clock()
        self.any_path = False
        
        while self.p.life != 0:
            
            self.clock.tick(30)
            
            if (self.p.getEnemy() != None):
                Person.Person.giveMeHelp(self.p)
                
            if (self.any_path and self.p.getEnemy() != None):
                self.path_deque.clear()
                self.any_path = False
                
            if (len(self.path_deque)):
                self.moveBot()
                if (self.path_deque == 0):
                    self.p.stopped()
            else:
                x1, y1 = Person.Person.getMaster().getPosition()
                
                if (self.p.getEnemy() != None):
                    if (not self.getPath((x1, y1))):
                        self.p.attack(pygame.K_SPACE)
                        Person.Person.giveMeHelp(self.p)
                else:
                    if (pygame.time.get_ticks() - self.last_tick > 5000):
                        self.getAnyPath()    
                        self.last_tick = pygame.time.get_ticks()
                        self.any_path = True
                    else:
                        self.p.stopped()
    
    def moveBot(self):
        x1, y1 = self.path_deque.popleft()
        self.p.doAMovement((x1, y1))


    def getPath (self, (x1, y1)):
        x0, y0 = self.p.getPosition()
        dist = PathFind.PathFind.euclidianDistance( (x0, y0), (x1, y1) )
        if (dist <= 100 and dist > 4):
            self.path_deque = PathFind.PathFind.getPath ((x0, y0), (x1, y1))
            return True
        return False
    
    
    def getAnyPath(self):
        x0, y0 = self.p.getPosition()
        
        xi, yi = self.p.getInitialPosition()
        
        mr = self.p.getMovementRange()
        
        x1 = random.randint(xi - mr, xi + mr)
        y1 = random.randint(yi - mr, yi + mr)
        
        if (not Walls.Walls.isAValidPosition(x1)):
            x1 = x0
            
        if (not Walls.Walls.isAValidPosition(y1)):
            y1 = x0
        
        self.path_deque = PathFind.PathFind.getPath ((x0, y0), (x1, y1))
