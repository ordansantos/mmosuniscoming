
import Queue
import Walls
import math
import pygame
from collections import deque

class PathFind():

    CONST_BOT_MIN_DISTANCE = 4
    CONST_ERROR_NO_PATH = 110000
    
    @staticmethod
    def neighbors((x, y)):
        
        l  = []
        
        if Walls.Walls.isFree((x - 1, y)):
            l.append((x - 1, y))   
        if Walls.Walls.isFree((x + 1, y)):
            l.append((x + 1, y))
        if Walls.Walls.isFree((x, y - 1)):
            l.append ((x, y - 1))
        if Walls.Walls.isFree((x, y + 1)):
            l.append ((x, y + 1))
        if Walls.Walls.isFree((x + 1, y - 1)):
            l.append ((x + 1, y - 1))
        if Walls.Walls.isFree((x + 1, y + 1)):
            l.append ((x + 1, y + 1))
        if Walls.Walls.isFree((x - 1, y + 1)):
            l.append ((x - 1, y + 1))
        if Walls.Walls.isFree((x - 1, y - 1)):
            l.append ((x - 1, y - 1))

        return l
    
    @staticmethod
    def manhattanDistance ((x0, y0), (x1, y1)):
        return math.fabs (x0 - x1) + math.fabs (y0 - y1)
	
    @staticmethod
    def euclidianDistance ((x0, y0), (x1, y1)):
        return math.sqrt ((x0 - x1) ** 2 + (y0 - y1) ** 2)
    
    #A* eh velocidade mediana e inteligente, bfs muito lento eh inteligente, best first search rapido eh relativamente burro
    @staticmethod
    def bestFirstSearch((x0, y0), (x1, y1), precise):
        loops = 0
        x_final, y_final = x_inicial, y_inicial = x0, y0
        discovered = set()
        
        parent_map = {}
        #cost = {}
        #cost[(x0, y0)] = 0
        parent_map[(x0, y0)] = (x0, y0)
        
        if Walls.Walls.isThereWall((x1, y1)):
            return (x0, y0, parent_map)
        
        q = Queue.PriorityQueue()

        q.put ( (0, (x0, y0) ) )
        discovered.add((x0, y0))
        
        while (not q.empty()):

            loops +=1 
            #print loops
            x0, y0 = q.get()[1]
            
            if (not precise):
                if (PathFind.euclidianDistance( (x0, y0), (x1, y1) ) <= PathFind.CONST_BOT_MIN_DISTANCE):
                    x_final, y_final = x0, y0
                    break;
            else:
                if ((x0, y0) == (x1, y1)):
                    x_final, y_final = x0, y0
                    break
                else:
                    if (PathFind.euclidianDistance( (x0, y0), (x1, y1) ) > PathFind.CONST_ERROR_NO_PATH or loops > 80000):
                        x_final, y_final = x_inicial, y_inicial
                        break
                    
            neighbors = PathFind.neighbors((x0, y0))
           
            #parent_cost = cost[(x0, y0)]
            
            for x, y in neighbors:
              
                """"a, b = PathFind.getObjectPosition((x, y), (x_inicial, y_inicial))
                print a, b
                pygame.draw.rect(pygame.display.get_surface(), (140,240,0), (a, b, 4, 4))
                pygame.display.flip()"""
                
                #if ( parent_map.get((x, y)) == None or cost[(x, y)] > parent_cost + 1 ):
                if ( (x, y) not in discovered):
                    parent_map[(x, y)] = (x0, y0)
                    #priority =  parent_cost + 1 + PathFind.manhattanDistance((x1, y1), (x, y))
                    priority =  PathFind.manhattanDistance((x1, y1), (x, y))
                    #cost[(x, y)] = parent_cost + 0.5
                    q.put( (priority, (x, y)) )
                    discovered.add((x, y))
        
        return (x_final, y_final, parent_map)

    # There is no memory for recursive solution
    @staticmethod    
    def buildPath (deque_path, parent_map, xy):

        while (parent_map[xy] != xy):
            deque_path.appendleft(xy)
            xy = parent_map[xy]
            
    @staticmethod
    def getPath ((x0, y0), (x1, y1),  precise = False):
        
        x_final, y_final, parent_map = PathFind.bestFirstSearch((x0, y0), (x1, y1), precise)
        
        path_deque = deque()
        
        PathFind.buildPath (path_deque, parent_map, (x_final, y_final))
        
        return path_deque
    
    @staticmethod   
    def getObjectPosition((objx, objy), (mx, my)):
        x = -mx * 4 + objx * 4 + (800 / 2)
        y = -my * 4 + objy * 4 + (600 / 2)
        return (x, y)
        
