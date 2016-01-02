import os
import pygame


def load_image(filename):
    image = os.path.join("assets", "images", filename)
    if filename.endswith('.jpg'):
        surface = pygame.image.load(image).convert()
    else:
        surface = pygame.image.load(image).convert_alpha()
    return surface


class FILES(object):
    hiscore = os.path.join('data', 'hiscore.txt')


class SCREEN(object):
    width = 1024
    height = 576
    display = pygame.display.set_mode((width, height))
    bg = load_image("bg.png")
    bg = pygame.transform.smoothscale(bg, (width, height))


class GAME(object):
    fps = 60
    time = 5 * 1


class MENU(object):    
    menuScreen = load_image("menuBG.png")
    scoreScreen = load_image("scorescreen.png")
    button = load_image("menu_button.png")
    buttonWidth = 178
    buttonHeight = 40


class STATE(object):
    menu = "menu"
    game = "game"
    nextlevel = "nextlevel"
    paused = "paused"
    countdown = "countdown"
    exit = "exit"
    splashscreen = "splashscreen"
    scorescreen = "scorescreen"
    logo = "logo"


class COLOR(object):
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (31, 31, 31)
    gray7 = (77, 77, 77)
    light_gray = (102, 102, 102)
    half_black = (128, 128, 128)
    green = (0, 196, 0)
    blue = (0, 109, 135)
    deep_rose = (204, 51, 153)
    regal_red = (204, 51, 102)
    blue_sea = (0, 149, 186)
    deep_blue = (0, 121, 150)
    desert_blue = (51, 102, 153)
    gold = (204, 153, 51)
    burnt_orange = (214, 89, 49)
    deep_yellow = (251, 200, 0)
    petal_green = (128, 190, 31)
    ice_blue = (153, 255, 255)

    colors = [ice_blue]


class FONT(object):
    default = os.path.join("assets", "fonts", "tinyfont.ttf")
    hoog0553 = os.path.join("assets", "fonts", "hoog0553.ttf")
    square = os.path.join("assets", "fonts", "square.ttf")


class TITLE(object):
    width = 604
    height = 60


class WORLD(object):
    gravity = 1


class PLAYER(object):
    one = "p1"
    two = "p2"
    ai = "ai"
    p1_label = load_image("p1_label.png")
    p2_label = load_image("p2_label.png")
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
    image = load_image("datafragment.png")


class ASSET(object):
    pygame_logo = load_image("pygame_logo.png")
    playerSheet = load_image("player1.png")
    playerMap = os.path.join("assets", "images", "playermap.txt")
    player1 = load_image("player1.png")
    player2 = load_image("player2.png")
    player1_glow = load_image("player1_glow.png")
    player2_glow = load_image("player2_glow.png")
    player_hurt = load_image("player_hurt.png")

    platform = load_image("platform.png")

    dataFragment = load_image("datafragment.png")

    bubble = load_image("light_particle.png")

    blockImage = load_image("block.png")
    ioInImage = load_image("io_in.png")
    portal = load_image("portal.png")
    portal_base = load_image("portal_base.png")

    saw1 = load_image("saw_spin1.png")
    saw2 = load_image("saw_spin2.png")
    saw3 = load_image("saw_spin3.png")
    sawFrames = [saw1, saw2, saw3]

    title = load_image("title.png")
    score_bg = load_image("score_bg.png")
    score_bg = pygame.transform.smoothscale(score_bg, (SCREEN.width, 54))

    countdown_overlay = load_image("countdown_bg.png")

    animateBG = load_image("bg_block.png")

    bg = load_image("bg.png")

    scanline = load_image("scan_line.png")
    scanline.set_alpha(20)

    studio_logo = load_image("phrbt_logo.png")
    try:
        overlay = load_image("overlay.jpg")
    except:
        overlay = load_image("overlay.png")


class SPLASHSCREEN(object):
    width = 450
    height = 178


class LOGO(object):
    width = 128
    height = 128


class RESULT(object):
    win = "WINNER"
    lose = "LOSER"
    draw = "DRAW"
