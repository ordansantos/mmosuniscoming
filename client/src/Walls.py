
import pytmx

class Walls:
    
    CONST_MAP_PX = 4
    CONST_MAP_WH = 1800
    
    Matrix = [[None for i in xrange(1810)] for j in xrange(1810)]
    
    def __init__(self):
        pass
    
    @staticmethod
    def getTileByPXMap((x, y)):
        
        if (x % Walls.CONST_MAP_PX):
            x = x / Walls.CONST_MAP_PX + 1
        else:
            x = x / Walls.CONST_MAP_PX
            
        if (y % Walls.CONST_MAP_PX):
            y = y / Walls.CONST_MAP_PX + 1
        else:
            y = y / Walls.CONST_MAP_PX
        
        return (x, y)
    
    @staticmethod
    def pushWalls (tile_map):
        for layer in tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    Walls.putAMagicWall ( Walls.getTileByPXMap( (obj.x, obj.y)), Walls.getTileByPXMap ((obj.width, obj.height)) )
                    
    @staticmethod
    def isThereWall ((x, y)):
        if (Walls.Matrix[x][y] == -1):
            return True
        return False
    
    @staticmethod
    def putAMagicWall ((x, y), (w, h)):
        for i in xrange (int(x), int(x + w) + 1):
            for j in xrange (int(y), int(y + h) + 1):
                Walls.Matrix[i][j] = -1
    # About Magic Wall's Algorithm : https://www.youtube.com/watch?v=nX6FNSU_Ywc
