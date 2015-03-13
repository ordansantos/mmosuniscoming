
import sys
sys.path.append("../")

import pygame

class Sound:
    
    def __init__(self, background='../sounds/background.ogg', volume=0.3):
        self.transformed = pygame.mixer.Sound('../sounds/transformed.wav')
        self.normal_background = pygame.mixer.Sound(background)
        self.normal_background.set_volume(volume)
        self.bg_vol = volume
        self.swapped = False
    
    # background
    def updateBackground(self, master_transformed):
        if master_transformed == 'S':
            self.normal_background.stop()
            self.transformed.play()
            self.swapped = True
        elif master_transformed == 'N':
            if self.swapped:
                self.normal_background.play(-1)
                self.swapped = False
    
    def backgroundPlay(self):
        self.normal_background.play(-1)
    
    def backgroundStop(self):
        self.normal_background.stop()
    
    def backgroundGetVolume(self):
        return self.normal_background.get_volume()
    
    def backgroundSetVolume(self, volume):
        self.normal_background.set_volume(volume)
    
    # attack
    @staticmethod
    def attackPlay(sound='../sounds/attack.wav', volume=0.5):
        attack = pygame.mixer.Sound(sound)
        attack.set_volume(volume)
        attack.play()
    
    # death
    @staticmethod
    def deathPlay(sound='../sounds/died.wav', volume=1.0):
        death = pygame.mixer.Sound(sound)
        death.set_volume(volume)
        death.play()
    
    # all
    def stopAll(self):
        self.transformed.stop()
        self.normal_background.stop()
    
