import sys
sys.path.append("../")

import sys, os, traceback
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"

import pygame
import Game

import reader.reader as reader
import reader.form as form

class GameTextBox:
    
    def __init__(self, width, height):
        
        self.text = 'Sun is Coming Client Start'
        
        # text editor
        self.edges = width / 160
        self.lenfont = 13
        
        self.writerbox_height = int(height / 24)
        self.readerbox_height = int(height / 9)
        self.readerbox_width = width - (self.edges * 2)
        self.reader_pos = (self.edges, self.readerbox_height * 8 - self.writerbox_height)
        self.writer_pos = (self.reader_pos[0], self.reader_pos[1] + self.readerbox_height + int(height / 85.7))
        
        self.reader = reader.Reader(unicode(self.text,'utf8'), self.reader_pos, self.readerbox_width, self.lenfont, self.readerbox_height + int(height / 100), font=os.path.join('../reader','MonospaceTypewriter.ttf'), fgcolor=(255,255,255), hlcolor=(250,190,150,50), split=True)
        self.writer = form.Form(self.writer_pos, self.readerbox_width, self.lenfont, self.writerbox_height - int(height / 100), bg=(0,0,0), fgcolor=(0,255,0), hlcolor=(250,190,150,50), curscolor=(0,255,0))
        
        self.writing_now = False
    
    def handleWriterBox(self, events):
        for e in events:
            if self.writing_now:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                        message = self.writer.OUTPUT
                        message = message[2:len(message)]
                        self.writer.setInitialGameTextBox()
                        self.writing_now = False
                        return message
                    else:
                        if ((e.key == pygame.K_BACKSPACE or e.key == pygame.K_LEFT) and self.writer._index <= 2):
                            continue
                        self.writer._cursor = True
                        self.writer.update(e)
            self.handleReaderBox(e)
        return None
    
    def handleReaderBox(self, event):
        if self.onTextBox(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.reader.update(event)
    
    def updateWriting(self):
        if self.onWriterBox(pygame.mouse.get_pos()):
            self.writing_now = True
        else:
            self.writing_now = False
    
    def onTextBox(self, (x, y)):
        if x >= self.reader_pos[0] and y >= self.reader_pos[1]:
            return True
        return False
    
    def onWriterBox(self, (x, y)):
        if x >= self.writer_pos[0] and y >= self.writer_pos[1]:
            return True
        return False
    
    def updateReaderMessage(self, message):
        self.reader.updateText(message)
    
    def drawTextBox(self):
        self.reader.show()
        self.writer.show()
    