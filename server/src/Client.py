
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
            list_positions.append ((id, x, y))
        
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
        
        self.clock = pygame.time.Clock()
        
        self.last_event = 0
        
        #enviando personagens criados e o id do master
        master_tuple = Client.getNewPlayer()
        self.master = Person.Person.getPersonById(master_tuple[0])
        
        data = {"bots": Client.getBots(self.master), "master": master_tuple}
        
        self.last_event = len(Client.events)
        
        data_string = json.dumps(data)
        self.conn.sendall (data_string)
        
        while True:
            self.clock.tick(30)
            data = self.conn.recv(1024)
            data = json.loads(data)
            self.master.doAMovement(data['movement'])
            data = {"moves": Client.getPackage(), "events": self.getEvents()}
            data_string = json.dumps(data)
            self.conn.sendall(data_string)
            
            
    def getEvents(self):
        new_last = len(Client.events)
        events = Client.events[self.last_event:new_last]
        self.last_event = new_last
        return events
    
        
"""
class Client:
    

    def clientthread(conn):


        conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    
        return
        while True:
    
    #Receiving from client
    
            data = conn.recv(1024)
            data = json.loads(data)
            if data['movement'] != 'none':
                Clients.putMove(data['movement'])
                continue
                #print data['movement']
            #print data['movement']from thread import *
            #if not data: 
            #    break
    
    
            #x = int(raw_input())
            #y = int(raw_input())
            
            data = { "moves": Clients.getMoves(id) }
            print '1:', data
            data_string = json.dumps(data)
            print '2:', data_string
            conn.sendall(data_string)
            
            Clients.clear(id)
            
            #came out of loop
        conn.close()
    
            #now keep talking with the client
            
            """