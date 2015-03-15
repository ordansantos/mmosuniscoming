
# coding: utf-8

import sys
sys.path.append("../")

import sys, os, traceback
if sys.platform in ["win32", "win64"]: os.environ["SDL_VIDEO_CENTERED"] = "1"

import pygame
from pygame.locals import *

import reader.reader as reader

class Menu:
    
    def __init__(self, screen, width, height):
        # frame
        self.frame = screen
        self.width = width
        self.height = height
        pygame.font.init()
        if not pygame.font.get_init():
            pygame.quit()
            print 'Pygame fonts module broken.!'
            sys.exit()
    
    def getSizeByHeight(self, reference, width, height):
        gap = reference - height
        perc = 0
        size = 0
        if gap < 0:
            gap = -gap
            perc = gap * 100 / height
            size = width - int(width * perc / 100), height - gap
        else:
            perc = gap * 100 / height
            size = width + int(width * perc / 100), height + gap
        return size
    
    def getSizeByWidth(self, reference, width, height):
        gap = reference - width
        perc = 0
        size = 0
        if gap < 0:
            gap = -gap
            perc = gap * 100 / width
            size = width - gap, height - int(height * perc / 100) 
        else:
            perc = gap * 100 / width
            size = width + gap, height + int(height * perc / 100)
        return size
    
    def selectMenu(self):
        
        menus = [unicode('Jogar', 'utf8'), unicode('Opções', 'utf8'), unicode('Sobre', 'utf8'), unicode('Sair', 'utf8')]
        menu = Choose(menus)
        
        while True:
            
            # background
            self.background = pygame.image.load("../tiles/menu/background.png").convert()
            self.bg_size = self.getSizeByHeight(self.height[0], self.background.get_width(), self.background.get_height())
            self.bg_size = self.bg_size[0], self.bg_size[1]
            self.background = pygame.transform.scale(self.background, self.bg_size).convert()
            
            # blit background
            self.frame.fill((0, 0, 0))
            self.frame.blit(self.background, (int(self.width[0] / 2) - int(self.bg_size[0] / 2), 0))
            
            # blit menu
            menu.show_horizontal((int(self.width[0] / 15), self.height[0] - int(self.height[0] / 15) * 2))
            
            # draw
            pygame.display.flip()
            
            # close game
            if pygame.event.peek(pygame.QUIT):
                return 4
            
            for e in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                # button clicked
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    for i in xrange(len(menus)):
                        if menu.isMouseInMenu(i):
                            return i
    
    def loading(self):
        # loading
        self.frame.fill((0, 0, 0))
        loading = pygame.image.load("../tiles/menu/loading.jpeg").convert()
        loading = pygame.transform.scale(loading, (self.width[0], self.height[0]))
        self.frame.blit(loading, (0, 0))
        
        # draw
        pygame.display.flip()
    
    def options(self):
        
        # functions
        def _back(mouse_pos):
            if (mouse_pos[0] > (back_pos[0])) and (mouse_pos[1] > (back_pos[1])) and (mouse_pos[0] < (back_pos[0] + back.get_width()) and (mouse_pos[1]) < (back_pos[1] + back.get_height())):
                return True
            return False
        
        def _small(mouse_pos):
            if (mouse_pos[0] > (small_pos[0])) and (mouse_pos[1] > (small_pos[1])) and (mouse_pos[0] < (small_pos[0] + small_screen.get_width()) and (mouse_pos[1]) < (small_pos[1] + small_screen.get_height())):
                return True
            return False
        
        def _full(mouse_pos):
            if (mouse_pos[0] > (full_pos[0])) and (mouse_pos[1] > (full_pos[1])) and (mouse_pos[0] < (full_pos[0] + full_screen.get_width()) and (mouse_pos[1]) < (full_pos[1] + full_screen.get_height())):
                return True
            return False
        
        color_in = (255, 0, 0)
        color_out = (255, 255, 255)
        
        small_color = color_out
        full_color = color_out
        
        back = pygame.image.load('../tiles/menu/back.png').convert()
        
        while True:
            
            # options init
            options_background = pygame.image.load('../tiles/menu/options/background.png').convert()
            op_size = self.getSizeByHeight(self.height[0], options_background.get_width(), options_background.get_height())
            options_background = pygame.transform.scale(options_background, op_size).convert()
            
            # blit options
            self.frame.fill((0, 0, 0))
            self.frame.blit(options_background, (int(self.width[0] / 2) - int(op_size[0] / 2), 0))
            
            # buttons
    
            # back
            back_size = self.getSizeByHeight(int(self.width[0] / 15), back.get_width(), back.get_height())
            back = pygame.transform.scale(back, back_size).convert()
            back_pos = back.get_width() * 0.5, self.height[0] - back.get_height() * 1.5
            
            # _text
            font_size = int(self.height[0] / 20)
            _text = pygame.font.Font('../tiles/menu/Purisa-Bold.ttf', font_size)
            
            # _text screen
            screen = _text.render("Tela", 1, color_out)
            screen_pos = screen.get_width() * 0.2, screen.get_height() * 0.5
            small_screen = _text.render("Pequena", 1, small_color)
            small_pos = screen_pos[0], screen_pos[1] + screen.get_height()
            full_screen = _text.render("Grande", 1, full_color)
            full_pos = small_pos[0] + small_screen.get_width(), small_pos[1]
            
            # highlighted
            stain_screen = pygame.image.load('../tiles/menu/options/stain.png').convert()
            if self.width[0] == 800:
                stain_size = self.getSizeByWidth(int(small_screen.get_width() * 0.5), stain_screen.get_width(), stain_screen.get_height())
                stain_pos = int(small_pos[0] * 1.6), small_pos[1] + int(small_screen.get_height() * 0.8)
            else:
                stain_size = self.getSizeByWidth(int(full_screen.get_width() * 0.5), stain_screen.get_width(), stain_screen.get_height())
                stain_pos = int(full_pos[0] * 1.15), full_pos[1] + int(full_screen.get_height() * 0.8)
            stain_screen = pygame.transform.scale(stain_screen, stain_size).convert()
            
            # blit buttons screen
            self.frame.blit(back, back_pos)
            self.frame.blit(screen, screen_pos)
            self.frame.blit(small_screen, small_pos)
            self.frame.blit(full_screen, full_pos)
            self.frame.blit(stain_screen, stain_pos)
            
            # draw
            pygame.display.flip()
            
            # choose
            
            # close game
            if pygame.event.peek(pygame.QUIT):
                return 'QUIT'
            
            for e in pygame.event.get():
                
                mouse_pos = pygame.mouse.get_pos()
                
                if _back(mouse_pos):
                    back = pygame.image.load('../tiles/menu/back_red.png').convert()
                else:
                    back = pygame.image.load('../tiles/menu/back.png').convert()
                if _small(mouse_pos):
                    small_color = color_in
                else:
                    small_color = color_out
                if _full(mouse_pos):
                    full_color = color_in
                else:
                    full_color = color_out
                
                # button clicked
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if _back(mouse_pos):
                        return 'NEXT'
                    elif _small(mouse_pos):
                        if self.width[0] > self.width[1]:
                            self.width[0], self.width[1] = [self.width[1], self.width[0]]
                            self.height[0], self.height[1] = [self.height[1], self.height[0]]
                            self.frame = pygame.display.set_mode((self.width[0], self.height[0]), HWSURFACE | DOUBLEBUF)
                    elif _full(mouse_pos):
                        if self.width[0] < self.width[1]:
                            self.width[0], self.width[1] = [self.width[1], self.width[0]]
                            self.height[0], self.height[1] = [self.height[1], self.height[0]]
                            self.frame = pygame.display.set_mode((self.width[0], self.height[0]), FULLSCREEN | HWSURFACE | DOUBLEBUF)
    
    def instructions(self):
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

        txt = reader.Reader(unicode(text, 'utf8'), (int(self.edges / 2), int(self.edges / 2)), self.width[0] - self.edges, 15, self.height[0] - self.edges, font=os.path.join('../reader', 'MonospaceTypewriter.ttf'), fgcolor=(255, 255, 255), hlcolor=(250, 190, 150, 50), split=True)
        txt.show()
        pygame.display.flip()
        
        while True:
            # close game
            if pygame.event.peek(pygame.QUIT):
                return 'QUIT'
            
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    return 'NEXT'
    
class Choose:
    
    def __init__(self, menus):
        pygame.font.init()
        if not pygame.font.get_init():
            pygame.quit()
            print 'Pygame fonts module broken.!'
            sys.exit()
        
        # characteristics
        self.color_in = (255, 0, 0)
        self.color_out = (255, 255, 255)
        height = pygame.display.get_surface().get_height()
        self.gap = int(height / 20)
        font_size = int(height / 20)
        self._text = pygame.font.Font('../tiles/menu/Purisa-Bold.ttf', font_size)
        
        # name, position
        self.menus = [[None for j in xrange(3)] for i in xrange(len(menus))]
        for i in xrange(len(menus)):
            self.menus[i][0] = self.getMenuSelectedPicture(menus[i])
            self.menus[i][1] = self.getMenuUnselectedPicture(menus[i])
            self.menus[i][2] = [-1, -1]
    
    def show_horizontal(self, initial_position):
        
        position = [initial_position[0], initial_position[1]]
        
        self.menus[0][2] = position
        height = position[1]
        
        for i in xrange(1, len(self.menus)):
            x = self.menus[i-1][2][0] + self.menus[i-1][0].get_width() + self.gap
            self.menus[i][2] = [x, height]
        
        self.blitMenus()

    def getMenuSelectedPicture(self, menu):
        return self._text.render(menu, 1, self.color_in)
    
    def getMenuUnselectedPicture(self, menu):
        return self._text.render(menu, 1, self.color_out)
    
    def blitMenus(self):
        src = pygame.display.get_surface()
        for i in xrange(len(self.menus)):
            if self.isMouseInMenu(i):
                src.blit(self.menus[i][0], self.menus[i][2])
            else:
                src.blit(self.menus[i][1], self.menus[i][2])
    
    def isMouseInMenu(self, menu_number):
        mouse_pos = pygame.mouse.get_pos()
        menu_pos = self.menus[menu_number][2]
        menu_size = self.menus[menu_number][0].get_width(), self.menus[menu_number][0].get_height()
        if (mouse_pos[0] > (menu_pos[0])) and (mouse_pos[1] > (menu_pos[1])) and (mouse_pos[0] < (menu_pos[0] + menu_size[0]) and (mouse_pos[1]) < (menu_pos[1] + menu_size[1])):
            return True
        return False
