

import socket
import json
import Person
import Character
import threading
import pygame
import Queue
import Main
class ClientSocket:
    
    def __init__(self, txt):
        
        self.host = 'http://suniscoming.ddns.net'
        self.port = 8888
        self.size = 1024
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect ((self.host, self.port))
        self.txt = txt
        data = {"check": False, "email": Person.Person.email, "senha": Person.Person.senha, "image": Person.Person.image}
      
        data = json.dumps(data)
        
        self.conn.sendall (data)
        
        
        data = self.conn.recv(self.size)
        data = json.loads(data)
        
        bots = data['bots']
        self.addBots (bots)
        master = data['master']
        self.createMaster (master)
        
        self.last_x = self.master.x
        self.last_y = self.master.y
        
        
        self.attack_event = None
        self.message = None
        
        self.q_moves = Queue.Queue()
        
        self.close = False
        
    def resetEvents(self):
        self.attack_event = None
        self.message = None
        
        
        
    def buildEventPackage(self):
        move = None
        
        if (not self.q_moves.empty()):
            move = self.q_moves.get()
            
        data = {"move": move, "attack": self.attack_event, "message": self.message}
      
        data = json.dumps(data)
        self.resetEvents()
        return data
    
    def setMessage(self, message):
        self.message = message

    def setAttack (self, key):
        if self.master.attack_key == Character.Character.NO_ATTACK:
            self.attack_event = key
            self.master.attack(key)
    
    def setMovementEvent (self, arrow):
        if self.master.attack_key == Character.Character.NO_ATTACK and self.master.life != 0:
            if arrow == [0, -1]:
                if (self.master.up()):
                    self.q_moves.put ('u')
                
            elif arrow == [0, 1]:
                if self.master.down():
                    self.q_moves.put ('d')
            elif arrow == [-1, 0]:
                if self.master.left():
                    self.q_moves.put ('l')
            elif arrow == [1, 0]:
                if self.master.right():
                    self.q_moves.put ('r')
            elif arrow == [-1, -1]:
                if self.master.upLeft():
                    self.q_moves.put ('ul')
            elif arrow == [1, -1]:
                if self.master.upRight():
                    self.q_moves.put ('ur')
            elif arrow == [-1, 1]:
                if self.master.downLeft():
                    self.q_moves.put ('dl')
            elif arrow == [1, 1]:
                if self.master.downRight():
                    self.q_moves.put ('dr')
    
    def addBots(self, bots):
        
        for bot in bots:
            self.addBot(bot)
    
    def addBot(self, bot):
        Person.Person.getNewBot (bot[1], bot[2], bot[3], bot[0], name=bot[4])
        
    def createMaster(self, (id, x, y, image, name)):
        self.master = Person.Person.getNewPlayer(x, y, image, id, name=name)
        Person.Person.setMaster(self.master.getId())
        print 'mestre: ', self.master.name
    
    def updateGame(self):

        self.conn.sendall (self.buildEventPackage())
        
        data = self.conn.recv(self.size)
        data = json.loads(data)
        self.updateEvents (data['events'])
        self.updateBotsPositions(data['moves'])
        error = data['error']
   
        if (error):
            self.repairError()
            print 'client error'
            
    def repairError(self):
        q = Queue.Queue()
        self.master.x = self.last_x
        self.master.y = self.last_y
    
    def updateBotsPositions(self, moves):
        for m in moves:
            id, x, y, life = m[0], m[1], m[2], m[3]
            p = Person.Person.getPersonById(id)
            if p == None: continue
            p.life = life
            
 
            #if life == 0:
            #    p.dying()
            if p.getPosition() == (x, y):
                p.stopTime()
            else:
                if (p != self.master):
                    p.putMove((x, y))
                    #print p.getPosition(), x, y
                else:
                    self.last_x = x;
                    self.last_y = y
                    
    def updateEvents (self, events):
        
        for e in events:
            event = e[0]
            
            if (event == 'c'):
                self.addBot(e[1])
            if (event == 'a'):
                p = Person.Person.getPersonById(e[1])
                if (p != self.master):
                    p.attack(e[2])
            if (event == 'd'):
                p = Person.Person.getPersonById(e[1])
                if (p == Person.Person.getMaster()):
                    self.close = True
                p.life = 0
                p.dying()
                
            if (event == 'm'):
                message = e[1]
                self.txt.updateReaderMessage(message)
                
class ClientConnection(threading.Thread):
    
    def run(self):

        self.client = self._Thread__kwargs['client']
        while (True):

            self.client.updateGame()
            if self.client.close:
                self.client.conn.close()
                break
    
    