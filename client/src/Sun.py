
import pygame

class Sun:
    
    def __init__(self):
        self.gray = 0
    
    def getColor(self):
        return (self.gray, self.gray, self.gray)
    
    def setGray(self, gray):
        self.gray = gray
