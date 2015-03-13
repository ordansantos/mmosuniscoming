# coding: utf-8

import sys
sys.path.append("../")

import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import pygame
import reader.reader as reader

class Menu:
    
    def __init__(self, screen, width, height):
        # frame
        self.frame = screen
        self.width = width
        self.height = height
        self.edges = int(self.height / 5)
        
        # background
        self.background = pygame.image.load("../tiles/bg_menu.png").convert()
        gap = self.height - self.background.get_height()
        if gap < 0:
            gap = -gap + self.edges
            self.bg_size = self.background.get_width() - gap, self.height - self.edges
        else:
            self.bg_size = self.background.get_width() + gap, self.height - self.edges
        
        self.background = pygame.transform.scale(self.background, self.bg_size).convert()
        
        # menu
        self.menu = pygame.image.load("../tiles/menu.png").convert()
        self.menu_pos = int(self.edges / 2) , self.height - self.menu.get_height() - int(self.edges / 2)
    
    def showMenu(self):

        # background
        self.frame.fill((0, 0, 0))
        self.frame.blit(self.background, (int(self.width / 2) - int(self.bg_size[0] / 2), int(self.edges / 2)))
        
        # menu
        self.frame.blit(self.menu, (self.menu_pos))
        
        #draw
        pygame.display.flip()
    
    def selectMenu(self, event):
        
        # functions
        def play(mouse_pos):
            if (mouse_pos[0] > (self.menu_pos[0])) and (mouse_pos[1] > (self.menu_pos[1] + 7)) and (mouse_pos[0] < (self.menu_pos[0] + 68) and (mouse_pos[1]) < (self.menu_pos[1] + 65)):
                return True
            return False
        
        def options(mouse_pos):
            if (mouse_pos[0] > (self.menu_pos[0] + 69)) and (mouse_pos[1] > (self.menu_pos[1] + 7)) and (mouse_pos[0] < (self.menu_pos[0] + 125) and (mouse_pos[1]) < (self.menu_pos[1] + 65)):
                return True
            return False
        
        def _exit(mouse_pos):
            if (mouse_pos[0] > (self.menu_pos[0] + 136)) and (mouse_pos[1] > (self.menu_pos[1] + 7)) and (mouse_pos[0] < (self.menu_pos[0] + 200) and (mouse_pos[1]) < (self.menu_pos[1] + 65)):
                return True
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if play(mouse_pos):
                return 1
            if options(mouse_pos):
                return 2
            if _exit(mouse_pos):
                return 3
    
    def loading(self):
        # loading
        self.frame.fill((0, 0, 0))
        loading = pygame.image.load("../tiles/loading.jpeg").convert()
        loading = pygame.transform.scale(loading, (self.width, self.height))
        self.frame.blit(loading, (0,0))
        
        #draw
        pygame.display.flip()
    
    def options(self):
        self.frame.fill((0, 0, 0))
        text = """-- ENREDO --

Este é um jogo de mundo aberto.
O personagem principal é um vampiro que luta para sobreviver na era medieval.
A tarefa do jogador é não deixar seu personagem morrer (acabar seu sangue). 
Para tanto é necessário se alimentar dos habitantes da vila. 

Misturando o gênero de ação furtiva, o jogador deve tomar cuidado para não ser pego se alimentando nem muito menos transformado.
O sol é um dos principais inimigos.

-- INSTRUÇÕES --

Você pode mover o personagem nas setas ou clicando no botão direito do mouse.
Quando estiver em modo supremo, você será capaz de matar os bots com apenas um golpe.
Para sair do jogo, pressione ESC a qualquer momento ;)

Divirta-se!

Clique para voltar"""

        txt = reader.Reader(unicode(text,'utf8'),(int(self.edges / 2), int(self.edges / 2)),self.width - self.edges,15,self.height - self.edges,font=os.path.join('../reader','MonospaceTypewriter.ttf'),fgcolor=(255,255,255),hlcolor=(250,190,150,50),split=True)
        txt.show()
        pygame.display.flip()
        
        while True:
            # close window
            if pygame.event.peek(pygame.QUIT):
                self.running = False
                pygame.quit()
                return 'QUIT'
            
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    return 'NEXT'
    
if __name__ == '__main__':
    width = 1280
    height = 780
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    menu = Menu(screen, width, height)
    menu.showMenu()
    while True:
        for e in pygame.event.get():
            op = menu.selectMenu(e)
        
        if type(op) == type(0):
            print op
    