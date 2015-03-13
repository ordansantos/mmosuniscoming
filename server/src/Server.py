#coding: utf-8

import socket
import sys
from thread import *
import json
import Client


class Server:
    
    def __init__(self):
        print 'Iniciando servidor: '
        self.HOST = ''
        self.PORT = 8888
    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ' - Socket criado'
        
        try:
            self.socket.bind((self.HOST, self.PORT))
        except socket.error as msg:
            print ' - Falha ao definir a porta e o host. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        print ' - Porta e host setados'
    
        self.socket.listen(10)
        
        print 'Servidor iniciado com sucesso!'
    
    def start(self):
        
        print 'Socket esperando conexões'
        
        while True:
            conn, addr = self.socket.accept()
            print 'Conectado com:  ' + addr[0] + ':' + str(addr[1])
            Client.Client.addNewClient(conn)

        self.socket.close()
