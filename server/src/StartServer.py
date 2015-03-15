
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
#Bot.BotController.putNewBot ((170, 350), '../characters/sprites/black_man.png')
#Bot.BotController.putNewBot ((180, 350), '../characters/sprites/blond_man.png')

server = Server.Server()

server.start()