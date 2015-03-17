
# coding: utf-8

import sys
from abc import abstractmethod
sys.path.append("../")

import sys, os, traceback
if sys.platform in ["win32", "win64"]: os.environ["SDL_VIDEO_CENTERED"] = "1"

import pygame
from pygame.locals import *

import reader.reader as reader

class Menu:
    
    @staticmethod
    def getSizeByHeight(reference, width, height):
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
    
    @staticmethod
    def getSizeByWidth(reference, width, height):
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
    
    @staticmethod
    def loading(width, height):
        # loading
        frame = pygame.display.get_surface()
        frame.fill((0, 0, 0))
        loading = pygame.image.load("../tiles/menu/img/loading.jpeg").convert()
        loading = pygame.transform.scale(loading, (width, height))
        frame.blit(loading, (0, 0))
        
        # draw
        pygame.display.flip()
    
    @staticmethod
    def options(width, height):
        
        frame = pygame.display.get_surface()
        
        # functions
        def _back(mouse_pos):
            if (mouse_pos[0] > (back_pos[0])) and (mouse_pos[1] > (back_pos[1])) and (mouse_pos[0] < (back_pos[0] + back.get_width()) and (mouse_pos[1]) < (back_pos[1] + back.get_height())):
                return True
            return False
        
        def _right_arrow(mouse_pos):
            if (mouse_pos[0] > (right_arrow_pos[0])) and (mouse_pos[1] > (right_arrow_pos[1])) and (mouse_pos[0] < (right_arrow_pos[0] + right_arrow.get_width()) and (mouse_pos[1]) < (right_arrow_pos[1] + right_arrow.get_height())):
                return True
            return False
        
        def _left_arrow(mouse_pos):
            if (mouse_pos[0] > (left_arrow_pos[0])) and (mouse_pos[1] > (left_arrow_pos[1])) and (mouse_pos[0] < (left_arrow_pos[0] + left_arrow.get_width()) and (mouse_pos[1]) < (left_arrow_pos[1] + left_arrow.get_height())):
                return True
            return False
        
        back = pygame.image.load('../tiles/menu/img/back.png').convert()
        right_arrow = pygame.image.load('../tiles/menu/img/arrow_white.png').convert_alpha()
        right_arrow = pygame.transform.rotate(right_arrow, 180.0).convert_alpha()
        left_arrow = pygame.image.load('../tiles/menu/img/arrow_white.png').convert_alpha()
        
        # character
        sprites = [[None for j in xrange(2)] for i in xrange(4)]
        
        sprites[0][0] = ('../characters/sprites/ordan.png')
        sprites[1][0] = ('../characters/sprites/pink_woman.png')
        sprites[2][0] = ('../characters/sprites/black_man.png')
        sprites[3][0] = ('../characters/sprites/blond_woman.png')
        
        size_sprite = int(height / 4), int(height / 4)
        for i in xrange(len(sprites)):
            pic = pygame.image.load(file(sprites[i][0])).convert_alpha()
            sprites[i][1] = pic.subsurface((0, 2 * 64, 64, 64)).convert_alpha()
            sprites[i][1] = pygame.transform.scale(sprites[i][j], size_sprite)
        
        master = 0
        
        while True:
            
            # options init
            options_background = pygame.image.load('../tiles/menu/img/mountains_moonlight.jpg').convert_alpha()
            op_size = Menu.getSizeByHeight(height, options_background.get_width(), options_background.get_height())
            #op_size = Menu.getSizeByWidth(width, options_background.get_width(), options_background.get_height())
            options_background = pygame.transform.scale(options_background, op_size).convert_alpha()
            
            # blit options
            frame.fill((0, 0, 0))
            frame.blit(options_background, (int(width / 2) - int(op_size[0] / 2), int(height / 2) - int(op_size[1] / 2)))
            
            # buttons
    
            # back
            back_size = Menu.getSizeByHeight(int(width / 15), back.get_width(), back.get_height())
            back = pygame.transform.scale(back, back_size).convert_alpha()
            back_pos = back.get_width() * 0.5, height - back.get_height() * 1.5
            
            # blit buttons screen
            frame.blit(back, back_pos)
            
            # character
            character_pos = int(width / 10), int(height / 2)
            frame.blit(sprites[master][1], character_pos)
            
            left_arrow_pos = character_pos[0] - int(width / 20), character_pos[1] + int(character_pos[1] / 4)
            right_arrow_pos = character_pos[0] + size_sprite[0], character_pos[1] + int(character_pos[1] / 4)
            size_arrow = size_sprite[0] / 5, size_sprite[1] / 5
            right_arrow = pygame.transform.scale(right_arrow, size_arrow).convert_alpha()
            left_arrow = pygame.transform.scale(left_arrow, size_arrow).convert_alpha()
            
            frame.blit(right_arrow, right_arrow_pos)
            frame.blit(left_arrow, left_arrow_pos)
            
            # draw
            pygame.display.flip()
            
            # choose
            
            # close game
            if pygame.event.peek(pygame.QUIT):
                return ['QUIT']
            
            for e in pygame.event.get():
                
                mouse_pos = pygame.mouse.get_pos()
                
                if _back(mouse_pos):
                    back = pygame.image.load('../tiles/menu/img/back_red.png').convert_alpha()
                else:
                    back = pygame.image.load('../tiles/menu/img/back.png').convert_alpha()
                
                if _right_arrow(mouse_pos):
                    right_arrow = pygame.image.load('../tiles/menu/img/arrow_red.png').convert_alpha()
                    right_arrow = pygame.transform.rotate(right_arrow, 180.0).convert_alpha()
                else:
                    right_arrow = pygame.image.load('../tiles/menu/img/arrow_white.png').convert_alpha()
                    right_arrow = pygame.transform.rotate(right_arrow, 180.0).convert_alpha()
                
                if _left_arrow(mouse_pos):
                    left_arrow = pygame.image.load('../tiles/menu/img/arrow_red.png').convert_alpha()
                else:
                    left_arrow = pygame.image.load('../tiles/menu/img/arrow_white.png').convert_alpha()
                
                # button clicked
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if _back(mouse_pos):
                        return ['MASTER', sprites[master][0]]
                    # character
                    if _right_arrow(mouse_pos):
                        master += 1
                        if master > 3:
                            master = 0
                    elif _left_arrow(mouse_pos):
                        master -= 1
                        if master < 0:
                            master = 3
                    
    @staticmethod
    def about(width, height):
        
        frame = pygame.display.get_surface()
        frame.fill((0, 0, 0))
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

        txt = reader.Reader(unicode(text, 'utf8'), (int(width / 30), int(width / 30)), width - int(width / 30), 15, height - int(width / 30), font=os.path.join('../reader', 'MonospaceTypewriter.ttf'), fgcolor=(255, 255, 255), hlcolor=(250, 190, 150, 50), split=True)
        txt.show()
        pygame.display.flip()
        
        while True:
            # close game
            if pygame.event.peek(pygame.QUIT):
                return 'QUIT'
            
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    return 'NEXT'

class Text:
    
    def __init__(self, menus, font_size):
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
        self._text = pygame.font.Font('../tiles/menu/fonts/Purisa-Bold.ttf', font_size)
        
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
            x = self.menus[i - 1][2][0] + self.menus[i - 1][0].get_width() + self.gap
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
    
    def getPosMenu(self, menu_number):
        return self.menus[menu_number][2][0], self.menus[menu_number][2][1]
    
    def getSizeMenu(self, menu_number):
        return self.menus[menu_number][0].get_width(), self.menus[menu_number][0].get_height()
    
    @staticmethod
    def blitAvulseText(text, x=-1, y=-1, font='../tiles/menu/fonts/Purisa-Bold.ttf', font_size=20, color=(255, 255, 255)):
        _text = pygame.font.Font(font, font_size)
        show = _text.render(text, 1, color)
        if x == -1:
            _src = pygame.display.get_surface()
            x = (_src.get_width() / 2) - (show.get_width() / 2)
        if y == -1:
            _src = pygame.display.get_surface()
            y = (_src.get_height() / 2) - (show.get_height() / 2)
        pygame.display.get_surface().blit(show, (x, y))
        return show
