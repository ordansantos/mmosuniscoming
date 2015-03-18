
import pygame

class Sun:
    
    # 1 minute = 60000
    PERIOD = 60000
    MAX = 256
    MIN = 80

    def __init__(self):
        self.time = 0
        self.gray = Sun.MIN
        self.sum = 16
    
    def getGray(self):
        color = self.gray
        time = pygame.time.get_ticks()
        if (time - self.time) >= Sun.PERIOD:
            color = self.nextGray()
            self.time = time
        if color >= 256:
            color = 255
        return color
    
    def nextGray(self):
        self.gray += self.sum
        if self.gray <= 80 - abs(self.sum):
            self.gray = 80
            self.sum = 16
        if self.gray == 256 + abs(self.sum):
            self.gray = 256
            self.sum = -16
        return self.gray
    
    def getPeriod(self):
        if self.gray < 192:
            return 'a'
        else:
            return 'm'
    