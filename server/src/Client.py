

import database 

import threading
import json
import Person
import Walls
import pygame

import Master

from pygame.locals import *

class Client:
    
    events = []
    
    @staticmethod
    def addNewClient (conn, sun):
        
        client_thread = ClientThread(kwargs={'conn': conn, 'sun': sun})
        client_thread.setDaemon(True)
        client_thread.start()
    
    @staticmethod
    def  getBots (master):
        
        bot_list = []
        
        bots = Person.Person.getPersons()
        
        for b in bots:
            if b != master and b.life != 0:
                x, y = b.getPosition()
                image = b.getImage()
                
                bot_list.append (( b.getId(), x, y, image, b.name))
            
        return bot_list
    
    @staticmethod
    def getPackage ():
        
        list_positions = []
        
        bots = Person.Person.getPersons()
        
        for b in bots:
            if (b.life == 0): continue
            x, y = b.getPosition()
            id = b.getId()
            life = b.life
            list_positions.append ((id, x, y, life))
        
        return list_positions
    
    @staticmethod
    def getNewPlayer(image, name):
        
        x, y = 733, 896
        
        while not Walls.Walls.isFree((x, y)):
            x += 1
            y += 1
                
        new = Person.Person.getNewPlayer(x, y, image, name)
        x, y = new.getPosition()
        image = new.getImage()
        id = new.getId()
        
        Client.events.append(('c', (id, x, y, image, name)))
        
        return (id, x, y, image, name)

    
        
class ClientThread(threading.Thread):
    
    def checkLogin (self, data):
        print '.'+data['email']+'.', '.'+data['senha']+'.'
        master_banco = Master.Master(email=data['email'], password=data['senha'])
        
        message = database.MasterCRUD.getMasterByLogin(master_banco)
        
        if (isinstance(message, Master.Master)): 
            message = 'SUCESS'
            
        return message
        
    def run(self):

        self.conn = self._Thread__kwargs['conn']
        self.sun = self._Thread__kwargs['sun']
        
        data = self.conn.recv(1024)
        
        data = json.loads(data)

        if (data['check']):
            message = self.checkLogin(data)
            self.conn.sendall (message)
            return
        
        master_banco = Master.Master(email=data['email'], password=data['senha'])
        master_banco = database.MasterCRUD.getMasterByLogin(master_banco)
        if (not isinstance(master_banco, Master.Master)): 
            return
        
        self.last_event = 0
        
        #enviando personagens criados e o id do master
        master_tuple = Client.getNewPlayer(data['image'], data['email'])

        self.master = Person.Person.getPersonById(master_tuple[0])

        self.master.all_killed = int(master_banco.killed)

        try:
        
            data = {"bots": Client.getBots(self.master), "master": master_tuple}
            
            self.last_event = len(Client.events)
            
            data_string = json.dumps(data)
            self.conn.sendall (data_string)
            
            while True:
                
                if (int(master_banco.killed) !=  int(self.master.all_killed) and int(self.master.all_killed) < 4):
                    master_banco.killed = str(self.master.all_killed)
                    database.MasterCRUD.updateMaster(master_banco)
                
                self.master.updateDeath(self.sun.getPeriod())
                
                self.error = False
                #print self.master.life
                data = self.conn.recv(1024)
                
                self.doClientEvents(data)
                
                if (self.master.life == 0):
                    Client.events.append(('d', self.master.getId()))
                
                data = {"moves": Client.getPackage(), "events": self.getServerEvents(), "error": self.error, "sun": self.sun.getGray()}
                
                data_string = json.dumps(data)
                self.conn.sendall(data_string)
                
                """if (self.master.life == 0):
                    data = self.conn.recv(1024)
                    data = {"moves": Client.getPackage(), "events": self.getServerEvents(), "error": self.error}
                    self.conn.sendall(data_string)
                    self.conn.close()
                    self.master.dead()
                    print 'fim da conexao com o cliente'
                    break """
        
        except Exception, e:
            print "Exception wile receiving message: ", e
            self.conn.close()
            self.master.dead()
            Client.events.append(('d', self.master.getId()))
        
    def doClientEvents(self, data):
        data = json.loads(data)
        
        attack_event = data['attack']
        move_event = data['move']
        message = data['message']
        
        self.error = self.doClientMovement (move_event)
        self.doClienAttack (attack_event)
        self.sendMessage (message)
        
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
    
    def sendMessage(self, message):
        if (message == None): return
        Client.events.append(('m', message))
    
