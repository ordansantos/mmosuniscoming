
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

Bot.BotController.putNewBot ((912, 482), '../characters/sprites/black_man.png')

Bot.BotController.putNewBot ((739, 498), '../characters/sprites/blond_man.png')
Bot.BotController.putNewBot ((935, 602),  '../characters/sprites/dumb_woman.png')
Bot.BotController.putNewBot ((981, 633), '../characters/sprites/blond_man.png')
Bot.BotController.putNewBot ((975, 597), '../characters/sprites/blond_woman.png')
Bot.BotController.putNewBot ((1029, 622), '../characters/sprites/brunette_woman.png')




server = Server.Server()

server.start()