import pygame
from constants import COLOR, FONT


class GameText(object):
    ''' This class will handle all text initialization and rendering'''
    def __init__(self, text, size=12, isBold=False):
        self.text = text
        self.size = size
        self.isBold = isBold
        self.fontFile = FONT.default
        self.color = COLOR.white
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.x = 0
        self.y = 0
        
    def create(self):
        self.font = pygame.font.Font(self.fontFile, self.size)
        self.render = self.font.render(self.text, self.isBold, self.color)
        self.rect = self.render.get_rect()
        
    def update(self):
        self.font = pygame.font.render(self.text, self.isBold, self.color)
        self.rect.x = x
        self.rect.y = y
    
        
    def draw(self, screen):
        screen.blit(self.font, self.rect)
    
        
