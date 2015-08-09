import os
import pygame
from assets import PlayerAsset

class SCREEN(object):
    width = 800
    height = 600

class COLOR(object):
    white = (255, 255, 255)
    black = (0, 0, 0)

class WORLD(object):
    gravity = 10

class ASSET(object):
    spriteSheet = pygame.image.load(os.path.join("assets", "images", "playerSpriteSheet.png"))
    spriteMap = os.path.join("assets", "images", "playerSpriteMap.txt")
    player = PlayerAsset(spriteSheet, spriteMap)