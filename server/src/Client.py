
import threading
import json
import Person
import Walls
import pygame

from pygame.locals import *

class Client:
    
    events = []
    
    @staticmethod
    def addNewClient (conn):
        
        client_thread = ClientThread(kwargs={'conn': conn})
        client_thread.setDaemon(True)
        client_thread.start()
    
    @staticmethod
    def  getBots (master):
        
        bot_list = []
        
        bots = Person.Person.getPersons()
        
        for b in bots:
            if b != master:
                x, y = b.getPosition()
                image = b.getImage()
                
                bot_list.append (( b.getId(), x, y, image))
            
        return bot_list
    
    @staticmethod
    def getPackage ():
        
        list_positions = []
        
        bots = Person.Person.getPersons()
        
        for b in bots:
            x, y = b.getPosition()
            id = b.getId()
            life = b.life
            list_positions.append ((id, x, y, life))
        
        return list_positions
    
    @staticmethod
    def getNewPlayer():
        
        x, y = 150, 350
        
        while not Walls.Walls.isFree((x, y)):
            x += 1
            y += 1
                
        new = Person.Person.getNewPlayer(x, y, '../characters/sprites/ordan.png')
        x, y = new.getPosition()
        image = new.getImage()
        id = new.getId()
        
        Client.events.append(('c', (id, x, y, image)))
        
        return (id, x, y, image)

    
        
class ClientThread(threading.Thread):
    
    def run(self):
        self.conn = self._Thread__kwargs['conn']
        
        self.last_event = 0
        
        #enviando personagens criados e o id do master
        master_tuple = Client.getNewPlayer()
        self.master = Person.Person.getPersonById(master_tuple[0])
        
        data = {"bots": Client.getBots(self.master), "master": master_tuple}
        
        self.last_event = len(Client.events)
        
        data_string = json.dumps(data)
        self.conn.sendall (data_string)
        
        while True:
            self.error = False
            
            data = self.conn.recv(1024)
            
            self.doClientEvents(data)
            
            data = {"moves": Client.getPackage(), "events": self.getServerEvents(), "error": self.error}
            data_string = json.dumps(data)
            self.conn.sendall(data_string)
            
    def doClientEvents(self, data):
        data = json.loads(data)
        
        attack_event = data['attack']
        move_event = data['move']
        
        self.error = self.doClientMovement (move_event)
        self.doClienAttack (attack_event)
        
    def doClientMovement(self, move_event):
        
            if move_event == 'u':
                return not self.master.up()
              
            elif move_event == 'd':
                return not self.master.down()
                
            elif move_event == 'l':
                return not self.master.left()
             
            elif move_event == 'r':
                return not self.master.right()
                
            elif move_event == 'ul':
                return not self.master.upLeft()
   
            elif move_event == 'ur':
                return not self.master.upRight()
      
            elif move_event == 'dl':
                return not self.master.downLeft()
              
            elif move_event == 'dr':
                return not self.master.downRight()
             
                
            if (move_event != None):
                return True
            return False
    
    def doClienAttack(self, attack_event):
        if attack_event != None:
            self.master.attack(attack_event)
            Client.events.append(('a', self.master.getId(), attack_event))
            
    def getServerEvents(self):
        new_last = len(Client.events)
        events = Client.events[self.last_event:new_last]
        self.last_event = new_last
        return events
    
    