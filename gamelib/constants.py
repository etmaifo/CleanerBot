import os
import pygame
from assets import ObjectAsset

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
    button = pygame.image.load(os.path.join("assets", "images", "menu_button.png"))


class STATE(object):
    menu = "menu"
    game = "game"
    paused = "paused"
    countdown = "countdown"
    exit = "exit"

class COLOR(object):
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (31, 31, 31)
    green = (0, 196, 0)
    blue = (0, 109, 135)
    deep_rose = (204, 51, 153)
    regal_red = (204, 51, 102)
    blue_sea = (0, 149, 186)
    deep_blue = (0, 121, 150)
    desert_blue = (51, 102, 153)
    gold = (204, 153, 51)
    burnt_orange = (214, 89, 49)
    petal_green = (128, 190, 31)

    colors = [deep_rose, regal_red, blue_sea, deep_blue, desert_blue, gold, burnt_orange, petal_green]

class WORLD(object):
    gravity = 1

class PLAYER(object):
    one = "p1"
    two = "p2"
    ai = "ai"
    p1_label = pygame.image.load(os.path.join("assets", "images", "p1_label.png"))
    p2_label = pygame.image.load(os.path.join("assets", "images", "p2_label.png"))
    jump = -18
    speed = 5

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
    ioOutImage = pygame.image.load(os.path.join("assets", "images", "iosprites.png"))

    sawSheet = pygame.image.load(os.path.join("assets", "images", "sawspritesheet.png"))
    sawMap = os.path.join("assets", "images", "sawspritesheet.txt")
    sawFrames = ObjectAsset(sawSheet, sawMap)

    score_bg = pygame.image.load(os.path.join("assets", "images", "score_bg.png"))
    score_bg = pygame.transform.smoothscale(score_bg, (SCREEN.width, 54))

    countdown_overlay = pygame.image.load(os.path.join("assets", "images", "countdown_bg.png"))

    animateBG = pygame.image.load(os.path.join("assets", "images", "bg_block.png"))
    
