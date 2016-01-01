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
        self.x = None
        self.y = None
        self.centerx = None
        self.centery = None
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        
    def create(self):
        self.font = pygame.font.Font(self.fontFile, self.size)
        self.render = self.font.render(self.text, self.isBold, self.color)
        self.rect = self.render.get_rect()
        
    def update(self):
        self.render = self.font.render(str(self.text), self.isBold, self.color)
        if self.x is not None:
            self.rect.x = self.x
        if self.y is not None:
            self.rect.y = self.y
        if self.centerx is not None:
            self.rect.centerx = self.centerx
        if self.centery is not None:
            self.rect.centery = self.centery
        if self.left is not None:
            self.rect.left = self.left
        if self.right is not None:
            self.rect.right = self.right
        if self.top is not None:
            self.rect.top = self.top
        if self.bottom is not None:
            self.rect.bottom = self.bottom
    
        
    def draw_to(self, screen):
        screen.blit(self.render, self.rect)
    
        
