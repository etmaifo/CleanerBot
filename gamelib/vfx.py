import pygame
from gamelib.physicsbody import PhysicsBody
from gamelib.constants import SCREEN, ASSET


class ScanLines(object):
    def __init__(self):
        self.collection = pygame.sprite.Group()
        self.assemble()

    def assemble(self):
        for i in range(200):
            scanline = PhysicsBody(0, i * 3, SCREEN.width, 1, ASSET.scanline)
            self.collection.add(scanline)

    def draw(self, screen):
        for scanline in self.collection:
            if scanline.rect.x < SCREEN.height:
                screen.blit(scanline.image, scanline.rect)