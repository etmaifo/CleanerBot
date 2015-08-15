import pygame
from physicsbody import PhysicsBody
from constants import BEAM


class Enemy(PhysicsBody):
    def __init__(self, x, y, width, height, image):
        PhysicsBody.__init__(self, x, y, width, height, image)


    def update(self):
        pass


