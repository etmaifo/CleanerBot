import os
import pygame
from assets import ObjectAsset

class COLOR(object):
    white = (255, 255, 255)
    black = (0, 0, 0)

class SCREEN(object):
    width =1024
    height = 576
    bg = pygame.image.load(os.path.join("assets", "images", "bg.png"))
    bg = pygame.transform.smoothscale(bg, (width, height))

class GAME(object):
    fps = 60
    time = 60 * 1 

class MENU(object):
    menuScreen = pygame.image.load(os.path.join("assets", "images", "menuBG.png"))
    scoreScreen = pygame.image.load(os.path.join("assets", "images", "scorescreen.png"))


class STATE(object):
    menu = "menu"
    game = "game"

class COLOR(object):
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (31, 31, 31)
    green = (0, 196, 0)

class WORLD(object):
    gravity = 1

class DIRECTION(object):
    left = "left"
    right = "right"
    up = "up"
    down = "down"
    
class PARTICLE(object):
    width = 8
    height = 8
    image = pygame.image.load(os.path.join("assets", "images", "datafragmentsprite.png"))

class ASSET(object):
    playerSheet = pygame.image.load(os.path.join("assets", "images", "playersprites.png"))
    playerMap = os.path.join("assets", "images", "playermap.txt")
    player = ObjectAsset(playerSheet, playerMap)

    platform = pygame.image.load(os.path.join("assets", "images", "platform.png"))

    dataFragmentSheet = pygame.image.load(os.path.join("assets", "images", "datafragmentsprite.png"))
    dataFragmentMap = os.path.join("assets", "images", "datafragmentmap.txt")
    dataFragmentFrames = ObjectAsset(dataFragmentSheet, dataFragmentMap)

    enemySheet = pygame.image.load(os.path.join("assets", "images", "enemysprites.png"))
    enemyMap = os.path.join("assets", "images", "enemymap.txt")
    enemyFrames = ObjectAsset(enemySheet, enemyMap)

    blockImage = pygame.image.load(os.path.join("assets", "images", "block.png"))
    ioInImage = pygame.image.load(os.path.join("assets", "images", "io_in.png"))
    ioOutImage = pygame.image.load(os.path.join("assets", "images", "io_out.png"))

