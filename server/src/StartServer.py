
import sys
sys.path.append("../")
import Server
import pytmx
import Walls
import Bot

from pytmx.util_pygame import load_pygame

#Iniciando os tiles do jogo
tile_map = load_pygame('tile_map.tmx')
Walls.Walls.pushWalls(tile_map) 

#Criando bots

Bot.BotController.putNewBot ((160, 350), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((170, 350), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((180, 350), '../characters/sprites/blond_man.png')
Bot.BotController.putNewBot ((200, 350), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((160, 350), '../characters/sprites/blond_man.png')
Bot.BotController.putNewBot ((250, 240), '../characters/sprites/pink_woman.png')
Bot.BotController.putNewBot ((130, 240), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((130, 240), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((364, 100), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((209, 538), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((209, 538), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((52, 536), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((230, 802), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((230, 802), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((456, 1420), '../characters/sprites/black_man.png')
Bot.BotController.putNewBot ((410, 1305), '../characters/sprites/black_man.png')

'''
'../characters/sprites/black_man.png'
'../characters/sprites/blond_man.png'
'../characters/sprites/blond_woman.png'
'../characters/sprites/brunette_woman.png'
'../characters/sprites/daenerys.png'
'../characters/sprites/dumb_blond.png'
'../characters/sprites/mohican_man_brunette.png'
'../characters/sprites/mohican_man_brunette.png'
'../characters/sprites/mohican_man.png'
'../characters/sprites/pink_woman.png'
'''

server = Server.Server()

server.start()