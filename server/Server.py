
import socket
import sys
from thread import *
import json

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Socket created'
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

class Clients:
    
    clients = []
    id = -1
    
    @staticmethod
    def putClient():
        Clients.id += 1
        Clients.clients.append([])
        return Clients.id
        
    @staticmethod
    def putMove(movement):
        for i in range (Clients.id +  1):
            Clients.clients[i].append(movement)
            
    @staticmethod
    def getMoves(id):
        return Clients.clients[id]
    
    @staticmethod
    def clear (id):
        Clients.clients[id] = []
            
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    id = Clients.putClient()
#Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

#infinite loop so that function do not terminate and thread do not end.
    while True:

#Receiving from client

        data = conn.recv(1024)
        data = json.loads(data)
        if data['movement'] != 'none':
            Clients.putMove(data['movement'])
            continue
            #print data['movement']
        #print data['movement']
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


while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn, ))

s.close()
