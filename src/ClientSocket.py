

import socket
import json

class ClientSocket :
    
    def __init__(self):
        
        self.host = '150.165.74.119'
        self.port = 8888
        self.size = 1024
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect ((self.host, self.port))
        data = self.conn.recv(self.size)
        print data
        
    def get(self):
       
        self.sendMovement ("none")
        data = self.conn.recv(self.size)
        print '->', data
        data = json.loads(data)
        return data
    
    def sendMovement(self, movement):
        
        data = {"movement" : movement}
        data = json.dumps(data)
        self.conn.send (data)
        
        
        
        
        
        