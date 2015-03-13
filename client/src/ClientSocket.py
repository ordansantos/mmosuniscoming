

import socket
import json
import Person

class ClientSocket :
    
    def __init__(self):
        
        self.host = 'localhost'
        self.port = 8888
        self.size = 1024
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect ((self.host, self.port))

        data = self.conn.recv(self.size)
        data = json.loads(data)
        
        bots = data['bots']
        self.addBots (bots)
        master = data['master']
        self.createMaster (master)
        
        #eventos
        self.attack_event = False
        self.move_event = None
    
    def resetEvents(self):
        self.attack_event = False
        self.move_event = None
    
    def buildEventPackage(self):
        data = {"move": self.move_event, "attack": self.attack_event}
      
        data = json.dumps(data)
        self.resetEvents()
        return data
    
    def setAttack (self):
        self.attack_event = True
    
    
    def setMovementEvent (self, arrow):
       
        if arrow == [0, -1]:
            self.move_event = 'u'
        elif arrow == [0, 1]:
            self.move_event = 'd'
        elif arrow == [-1, 0]:
            self.move_event = 'l'
        elif arrow == [1, 0]:
            self.move_event = 'r'
        elif arrow == [-1, -1]:
            self.move_event = 'ul'
        elif arrow == [1, -1]:
            self.move_event = 'ur'
        elif arrow == [-1, 1]:
            self.move_event = 'dl'
        elif arrow == [1, 1]:
            self.move_event = 'dr'
    
    def addBots(self, bots):
        
        for bot in bots:
            self.addBot(bot)
    
    def addBot(self, bot):
        Person.Person.getNewBot (bot[1], bot[2], bot[3], bot[0])
    
    def createMaster(self, (id, x, y, image)):
        self.master = Person.Person.getNewPlayer(x, y, image, id)
        Person.Person.setMaster(self.master.getId())
        
    
    def updateGame(self):
        
        self.conn.sendall (self.buildEventPackage())
        
        data = self.conn.recv(self.size)
        data = json.loads(data)
        self.updateEvents (data['events'])
        self.updateBotsPositions(data['moves'])
        
    def updateBotsPositions(self, moves):
        for m in moves:
            id, x, y = m[0], m[1], m[2]
            p = Person.Person.getPersonById(id)
            
            if p.getPosition() == (x, y):
                p.stopped()
            else:
                p.doAMovement((x, y))
            
    def updateEvents (self, events):
        
        for e in events:
            event = e[0]
            
            if (event == 'c'):
                self.addBot(e[1])
    
                
        
        