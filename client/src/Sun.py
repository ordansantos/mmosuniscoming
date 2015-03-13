
import pygame

class Sun:
    
    # 2,5 minutes = 150000
    PERIOD = 15000
    MAX = 256
    MIN = 80

    def __init__(self):
        self.color = (Sun.MIN, Sun.MIN, Sun.MIN)
        self.time = 0
        self.gray = Sun.MIN
        self.sum = 16
    
    def getColor(self):
        time = pygame.time.get_ticks()
        if (time - self.time) >= Sun.PERIOD:
            self.color = self.nextColor()
            self.time = time
        return self.color
    
    def nextColor(self):
        self.gray += self.sum
        if self.gray == Sun.MIN - abs(self.sum):
            self.gray = Sun.MIN
            self.sum = 16
        if self.gray == Sun.MAX + abs(self.sum):
            self.gray = Sun.MAX
            self.sum = -16
        if self.gray == Sun.MAX:
            return (255, 255, 255)
        return (self.gray, self.gray, self.gray)
    
    def getPeriod(self):
        if self.gray < 192:
            return 'afternoon'
        else:
            return 'morning'
    