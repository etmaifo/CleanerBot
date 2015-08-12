import os
import pygame
from assets import ObjectAsset

class SCREEN(object):
    width = 800
    height = 600

class COLOR(object):
    white = (255, 255, 255)
    black = (0, 0, 0)

class WORLD(object):
    gravity = 1

class ASSET(object):
    spriteSheet = pygame.image.load(os.path.join("assets", "images", "playerSpriteSheet.png"))
    spriteMap = os.path.join("assets", "images", "playerSpriteMap.txt")
    player = ObjectAsset(spriteSheet, spriteMap)
    platform = pygame.image.load(os.path.join("assets", "images", "platform.png"))
    enemySheet = pygame.image.load(os.path.join("assets", "images", "enemySpriteSheet.png"))
    enemyMap = os.path.join("assets", "images", "enemySpriteMap.txt")
    enemy = ObjectAsset(enemySheet, enemyMap)
