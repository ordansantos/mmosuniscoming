# coding: utf-8

import pygame
from pygame.locals import *

import sys
import Game
import Person
import cPickle
import socket
import json

from Menu import Menu, Text

import reader.form as form

class Main:
    
    def __init__(self):
        
        # begin main
        pygame.init()
        
        info = pygame.display.Info()
        
        self.width = (800, info.current_w)
        self.height = (600, info.current_h)
        
        self.screen = pygame.display.set_mode((self.width[0], self.height[0]), HWSURFACE | DOUBLEBUF)
        
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
        
        self.clock = pygame.time.Clock()

    @staticmethod
    def blitGameName():
        height = pygame.display.get_surface().get_height()
        Text.blitAvulseText('Sun is coming', -1, int(height/8), font='../tiles/menu/fonts/Toxia_FRE.ttf', font_size=int(height/5), color=(255, 0, 0))

    def run(self):
        
        def selectMenu():
            
            def _size(mouse_pos):
                if mouse_pos[0] > size_pos[0] and mouse_pos[1] > size_pos[1] and mouse_pos[0] < size_pos[0] + size[0] and mouse_pos[1] < size_pos[1] + size[1]:
                    return True
                return False
            
            width = self.screen.get_width()
            height = self.screen.get_height()
            
            size_pic = pygame.image.load('../tiles/menu/img/full_white.png').convert_alpha()
            
            while True:
                
                self.clock.tick(10)
                
                # background
                background = pygame.image.load("../tiles/menu/img/mountains_moonlight.jpg").convert()
                bg_size = Menu.getSizeByHeight(height, background.get_width(), background.get_height())
                background = pygame.transform.scale(background, bg_size).convert()
                
                # blit background
                self.screen.fill((0, 0, 0))
                self.screen.blit(background, (int(width / 2) - int(bg_size[0] / 2), int(height / 2) - int(bg_size[1] / 2)))
                
                # menus
                menus = [unicode('Jogar', 'utf8'), unicode('Sobre', 'utf8'), unicode('Sair', 'utf8')]
                menu = Text(menus, int(height / 15))
                
                # blit game name
                # Text.blitAvulseText('Sun is coming', -1, int(height/8), font='../tiles/menu/fonts/Toxia_FRE.ttf', font_size=int(height/5), color=(255, 0, 0))
                self.blitGameName()
                
                # blit menu
                menu.show_horizontal((int(width / 15), height - int(height / 15) * 2))
                
                # blit size
                size = int(height / 15), int(height / 15)
                size_pos = width - size[0] * 1.5, height - size[0] * 1.5
                size_pic = pygame.transform.scale(size_pic, size).convert_alpha()
                self.screen.blit(size_pic, size_pos)
                
                # draw
                pygame.display.flip()
                
                # close game
                if pygame.event.peek(pygame.QUIT):
                    return 3
                
                mouse_pos = pygame.mouse.get_pos()
                if _size(mouse_pos):
                    if width != self.width[0]:
                        size_pic = pygame.image.load('../tiles/menu/img/small_red.png').convert_alpha()
                    else:
                        size_pic = pygame.image.load('../tiles/menu/img/full_red.png').convert_alpha()
                else:
                    if width != self.width[0]:
                        size_pic = pygame.image.load('../tiles/menu/img/small_white.png').convert_alpha()
                    else:
                        size_pic = pygame.image.load('../tiles/menu/img/full_white.png').convert_alpha()
                
                for e in pygame.event.get():
                    # button clicked
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        # size
                        if _size(mouse_pos):
                            if width == self.width[0]:
                                self.screen = pygame.display.set_mode((self.width[1], self.height[1]), FULLSCREEN | HWSURFACE | DOUBLEBUF)
                                width = self.width[1]; height = self.height[1]
                            else:
                                self.screen = pygame.display.set_mode((self.width[0], self.height[0]), HWSURFACE | DOUBLEBUF)
                                width = self.width[0]; height = self.height[0]
                        
                        # menus
                        for i in xrange(len(menus)):
                            if menu.isMouseInMenu(i):
                                return i
        
        # begin run
        while True:
            
            self.clock.tick(10)
            
            # close game
            if pygame.event.peek(pygame.QUIT):
                return 'QUIT'
            
            op = 0
            
            op = selectMenu()
            
            width = self.screen.get_width()
            height = self.screen.get_height()
            
            if op == 0:
                Person.Person.reset()
                path_image = Menu.selectCharacter(width, height)
                Menu.loading(width, height)
                game = Game.Game(self.screen, width, height, path_image)
                switch = game.run()
                if switch == 'QUIT':
                    pygame.quit()
                    sys.exit()
            
            elif op == 1:
                switch = Menu.about(width, height)
                if switch[0] == 'QUIT':
                    pygame.quit()
                    sys.exit()
            
            elif op == 2:
                pygame.quit()
                sys.exit()

class Login:
    
    def __init__(self):
        self._src = pygame.display.get_surface()
        self.width = self._src.get_width()
        self.height = self._src.get_height()
        
        self.email = None
        self.password = None
        
        self.gap = self.width / 8
        lenfont = 20
        
        # emailbox
        self.emailbox_width, self.emailbox_height = int(self.width - self.gap * 3), int(self.height / 25)
        self.emailbox_pos = (self.width / 2 - self.emailbox_width / 2.5, self.height / 2 + self.gap)
        self.writer_email = form.Form(self.emailbox_pos, self.emailbox_width, lenfont, self.emailbox_height, bg=(255,255,255), fgcolor=(0,0,0), hlcolor=(250,190,150,50), curscolor=(0,255,0))
        self.writer_email_now = False
        
        # passbox
        self.passbox_width, self.passbox_height = self.emailbox_width, self.emailbox_height
        self.passbox_pos = self.emailbox_pos[0], self.emailbox_pos[1] + self.gap / 3
        self.writer_pass = form.Form(self.passbox_pos, self.passbox_width, lenfont, self.passbox_height, bg=(255,255,255), fgcolor=(0,0,0), hlcolor=(250,190,150,50), curscolor=(0,255,0))
        self.writer_pass_now = False
        self.false_pass = form.Form(self.passbox_pos, self.passbox_width, lenfont, self.passbox_height, bg=(255,255,255), fgcolor=(0,0,0), hlcolor=(250,190,150,50), curscolor=(0,255,0))
        
        # reset writerboxes
        self.writer_email.setBlanckMessage()
        self.writer_pass.setBlanckMessage()
        self.false_pass.setBlanckMessage()
        
        # button
        self.button_white = Text.blitAvulseText('ENTRAR', -1, self.passbox_height + self.gap, font='../tiles/menu/fonts/Purisa-Bold.ttf', font_size=int(self.height/20), color=(255, 255, 255))
        self.button_red = Text.blitAvulseText('ENTRAR', -1, self.passbox_height + self.gap, font='../tiles/menu/fonts/Purisa-Bold.ttf', font_size=int(self.height/20), color=(255, 0, 0))
        self.button = self.button_white
        self.button_pos = self.width / 2 - self.button.get_width() / 2, self.passbox_pos[1] + self.passbox_height + self.gap / 4
        
        self.clock = pygame.time.Clock()
    
    def onWriterEmail(self, mouse_pos):
        if mouse_pos[0] >= self.emailbox_pos[0] and mouse_pos[1] >= self.emailbox_pos[1] and mouse_pos[0] < self.emailbox_pos[0] + self.emailbox_width and mouse_pos[1] < self.emailbox_pos[1] + self.emailbox_height:
            return True
        return False
    
    def onWriterPass(self, mouse_pos):
        if mouse_pos[0] >= self.passbox_pos[0] and mouse_pos[1] >= self.passbox_pos[1] and mouse_pos[0] < self.passbox_pos[0] + self.passbox_width and mouse_pos[1] < self.passbox_pos[1] + self.passbox_height:
            return True
        return False
    
    def onButton(self, mouse_pos):
        if mouse_pos[0] >= self.button_pos[0] and mouse_pos[1] >= self.button_pos[1] and mouse_pos[0] < self.button_pos[0] + self.button.get_width() and mouse_pos[1] < self.button_pos[1] + self.button.get_height():
            return True
        return False
    
    def handleWriterEmail(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    self.email = self.writer_email.OUTPUT
                    self.writer_email_now = False
                    self.writer_pass_now = True
                    return
                elif e.key != pygame.K_RETURN and e.key != pygame.K_KP_ENTER and e.key != pygame.K_SPACE:
                    self.writer_email.update(e)
                    pygame.time.delay(50)
    
    def handleWriterPass(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_TAB:
                    self.email = self.writer_pass.OUTPUT
                    self.writer_pass_now = False
                    self.button = self.button_red
                    return
                elif e.key != pygame.K_RETURN and e.key != pygame.K_KP_ENTER and e.key != pygame.K_SPACE:
                    self.writer_pass.update(e)
                    # this is where the magic happens
                    s = ''
                    for i in xrange(len(self.writer_pass.OUTPUT)):
                        s += '*'
                    self.false_pass._splitted = [s]
                    pygame.time.delay(50)
    
    def blitBackgroundLogin(self):
        # background
        background = pygame.image.load("../tiles/menu/img/moonlight.jpg").convert()
        bg_size = Menu.getSizeByWidth(self.width, background.get_width(), background.get_height())
        background = pygame.transform.scale(background, bg_size).convert()
        
        # blit background
        self._src.fill((0, 0, 0))
        self._src.blit(background, (int(self.width / 2) - int(bg_size[0] / 2), int(self.height / 2) - int(bg_size[1] / 2)))
        
        # blit game name
        Main.blitGameName()
        # Text.blitAvulseText('Sun is coming', -1, int(self.height/8), font='../tiles/menu/fonts/Toxia_FRE.ttf', font_size=int(self.height/5), color=(255, 0, 0))
    
    def run(self):
        
        self.blitBackgroundLogin()
                
        x = self.width / 2 - (self.width - self.gap * 2) / 2
        y = self.height / 2 + self.gap - 5
        Text.blitAvulseText('Nome: ', x, y, font='../tiles/menu/fonts/Purisa-Bold.ttf', font_size=20, color=(255, 255, 255))
        Text.blitAvulseText('Senha: ', x, y + self.gap / 3, font='../tiles/menu/fonts/Purisa-Bold.ttf', font_size=20, color=(255, 255, 255))
        
        # draw
        pygame.display.flip()
        
        while True:
            
            self.clock.tick(30)
            
            # close game
            if pygame.event.peek(pygame.QUIT):
                return 'QUIT'
            
            events = pygame.event.get()
            
            for e in events:
                
                mouse_pos = pygame.mouse.get_pos()
                
                # pressed
                if e.type == pygame.KEYDOWN and (e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER):
                    self.go = True
                    break
                
                # mousemotion
                if self.onButton(mouse_pos):
                    self.button = self.button_red
                else:
                    self.button = self.button_white
                
                # clicked
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if self.onWriterEmail(mouse_pos):
                        self.writer_email.setBlanckMessage()
                        self.writer_email_now = True
                        self.writer_pass_now = False
                    elif self.onWriterPass(mouse_pos):
                        self.writer_pass.setBlanckMessage()
                        self.false_pass.setBlanckMessage()
                        self.writer_pass_now = True
                        self.writer_email_now = False
                    elif self.onButton(mouse_pos):
                        self.email = self.writer_email.OUTPUT
                        self.password = self.writer_pass.OUTPUT
                        return self.email, self.password
                    else: # if clicked out...
                        self.email = self.writer_email.OUTPUT
                        self.password = self.writer_pass.OUTPUT
                        self.writer_email_now = False
                        self.writer_pass_now = False
                        self.button = self.button_white
                
                # writer
                if self.writer_email_now:
                    self.handleWriterEmail(events)
                elif self.writer_pass_now:
                    self.handleWriterPass(events)
            
            # blit
            self.writer_email.show()
            self.false_pass.show()
            self._src.blit(self.button, self.button_pos)
            Text.blitAvulseText('Cadastre-se em http://suniscoming.ddns.net/', -1, y + self.gap * 1.5, font='../reader/MonospaceTypewriter.ttf', font_size=20, color=(255, 0, 0))
            
            # draw
            pygame.display.update()
    
    def showError(self, message):
            
        self.blitBackgroundLogin()
        pygame.display.flip()
        
        while True:
            
            y = self.height / 2 + self.gap - 5
            # blit text
            Text.blitAvulseText(message, -1, y, font='../tiles/menu/fonts/Purisa-Bold.ttf', font_size=50, color=(255, 0, 0))
            Text.blitAvulseText('Clique para continuar...', -1, y + self.gap / 1.5, font='../tiles/menu/fonts/Purisa-Bold.ttf', font_size=20, color=(255, 0, 0))
            
            # draw
            pygame.display.update()
            
            # close game
            if pygame.event.peek(pygame.QUIT):
                pygame.quit()
                sys.exit()
        
            for e in pygame.event.get():
                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    return 'NEXT'
        
        
def checkLogin(email, senha):
    
    try:
        
        host = 'suniscoming.ddns.net'
        port = 8888
        size = 1024
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect ((host, port))
        senha = str(senha)
        data = {"check": True, "email": email, "senha": senha}
      
        data = json.dumps(data)
        
        conn.sendall (data)
        
        data = conn.recv(size)
        
        return data
    
    except Exception, e:
        print e
        return 'Servidor inativo'
    
    con.close()
    
        
if __name__ == '__main__':
    
    main = Main()
    login = Login()
    
    # update title based in Ana and Sthefano
    pygame.display.set_caption('Sun is coming Client. Mantido por Ordan Santos e Eri Jonhson')
    
    while True:
        
        master_informations = login.run()
        
        if master_informations == 'QUIT':
            pygame.quit()
            sys.exit()
        
        print master_informations[0]
        print master_informations[1]
        
        response = checkLogin(master_informations[0], master_informations[1])
        print response
        
        if not response == 'SUCESS':
            login.showError(response)
        else:
            Person.Person.email = master_informations[0]
            Person.Person.senha = master_informations[1]
            break
        
    # make tests
    main.run()


    
