
import pygame
from pygame.locals import *

import Game
import Menu
import Person

pygame.init()

info = pygame.display.Info()

width = [800, info.current_w]
height = [600, info.current_h]

screen = pygame.display.set_mode((width[0], height[0]), HWSURFACE | DOUBLEBUF)

menu = Menu.Menu(screen, width, height)

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

while True:
    
    op = 0
    
    op = menu.selectMenu()
    
    if op == 0:
        menu.loading()
        game = Game.Game(screen, width[0], height[0])
        switch = game.run()
        if switch == 'QUIT':
            pygame.quit()
            break
        Person.Person.reset()
    elif op == 1:
        switch = menu.options()
        if switch == 'QUIT':
            pygame.quit()
            break
    
    elif op == 2:
        print 'Menu unexist'
        
    elif op == 3:
        pygame.quit()
        break
