
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
        if (x < 0 or y < 0 or x > Walls.CONST_MAP_WH or y > Walls.CONST_MAP_WH):
            return False
        if (Walls.Matrix[x][y] != None and Walls.Matrix[x][y] == -1):
            return True
        return False
    
    @staticmethod
    def putAMagicWall ((x, y), (w, h)):
        for i in xrange (int(x), int(x + w) + 1):
            for j in xrange (int(y), int(y + h) + 1):
                Walls.Matrix[i][j] = -1
    # About Magic Wall's Algorithm : https://www.youtube.com/watch?v=nX6FNSU_Ywc
    
    @staticmethod
    def pushPerson (x, y, p):
        if (x < 0 or y < 0 or x > Walls.CONST_MAP_WH or y > Walls.CONST_MAP_WH):
            return False
        if (not Walls.isThereWall((x, y)) and not Walls.isTherePerson(x, y)):
            Walls.Matrix[x][y] = p.getId()
            return True
        return False;
    
    @staticmethod
    def doChange(id, (x0, y0), (x, y)):
        Walls.Matrix[x0][y0] = None
        Walls.Matrix[x][y] = id
        
    @staticmethod
    def changePersonLocation (p, x, y):
        
        x0, y0 = final_position = p.getPosition()
        
        k = 1
        # It's done for any k's
        if (y0 == y):
            
            if (x < x0):
                k = -1
            
            while ( x0 != x ):
                x0 += k
                if (Walls.isThereWall((x0, y0)) or Walls.isTherePerson(x0, y0)):
                    return final_position
            
                final_position = (x0, y0)
                
            Walls.doChange(p.getId(), p.getPosition(), (x0, y0))
            
            return final_position
        
        if (x0 == x):
            #print x0, y0, x, y
            if (y < y0):
                k = -1
            
            while ( y0 != y ):
                y0 += k
                if (Walls.isThereWall((x0, y0)) or Walls.isTherePerson(x0, y0)):
                    return final_position
                
                final_position = (x0, y0)
                
            Walls.doChange(p.getId(), p.getPosition(), (x0, y0))
            
            return final_position
        
        j = 1
        if (x < x0):
            k = -1
        if (y < y0):
            j = -1
        
        while ( y0 != y and x0 != x ):
            x0 += k
            y0 += j
            if (Walls.isThereWall((x0, y0)) or Walls.isTherePerson(x0, y0)):
                return final_position
            
            final_position = (x0, y0)
        
        Walls.doChange(p.getId(), p.getPosition(), (x0, y0))
            
        return final_position
    
    @staticmethod
    def isTherePerson (x, y):
        if (Walls.Matrix[x][y] != None and Walls.Matrix[x][y] != -1):
            return True
        return False

    @staticmethod
    def getIdPosition (x, y):
        if (Walls.Matrix[x][y] == None or Walls.Matrix[x][y] == -1):
            return -1
        return Walls.Matrix[x][y]
    
    @staticmethod
    def freeLocation((x, y)):
        Walls.Matrix[x][y] = None
        
    @staticmethod
    def isAValidPosition(z):
        if z < 0 or z > Walls.CONST_MAP_WH:
            return False
        return True
    
    @staticmethod
    def isFree((x, y)):
        return Walls.Matrix[x][y] == None
        