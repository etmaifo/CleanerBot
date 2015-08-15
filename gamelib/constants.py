import os
import pygame
from assets import ObjectAsset, BeamAsset

class SCREEN(object):
    width = 800
    height = 600

class COLOR(object):
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (31, 31, 31)

class WORLD(object):
    gravity = 1

class BEAM(object):
    raywidth = 96
    rayheight = 160
    basewidth = 96
    baseheight = 32
    baseImage = pygame.image.load(os.path.join("assets", "images", "beambase.png"))

class ASSET(object):
    playerSheet = pygame.image.load(os.path.join("assets", "images", "playersprites.png"))
    playerMap = os.path.join("assets", "images", "playermap.txt")
    player = ObjectAsset(playerSheet, playerMap)

    platform = pygame.image.load(os.path.join("assets", "images", "platform.png"))

    dataFragmentSheet = pygame.image.load(os.path.join("assets", "images", "datafragmentsprite.png"))
    dataFragmentMap = os.path.join("assets", "images", "datafragmentmap.txt")
    dataFragment = ObjectAsset(dataFragmentSheet, dataFragmentMap)

    enemySheet = pygame.image.load(os.path.join("assets", "images", "enemysprites.png"))
    enemyMap = os.path.join("assets", "images", "enemymap.txt")
    enemy = ObjectAsset(enemySheet, enemyMap)

    blockImage = pygame.image.load(os.path.join("assets", "images", "block.png"))

    beamSheet = pygame.image.load(os.path.join("assets", "images", "beamsprites.png"))
    beamMap = os.path.join("assets", "images", "beammap.txt")
    beam = BeamAsset(beamSheet, beamMap)
