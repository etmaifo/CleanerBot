import pygame
import sys, os
from pygame import *
from random import choice
from levelfactory import Stage
from camera import Camera
from logo import LogoScreen
from menu import Menu
from overlay import CountDownOverlay
from scorescreen import ScoreScreen
from splashscreen import SplashScreen
from vfx import ScanLines
from constants import SCREEN, COLOR, STATE, GAME, ASSET, SPLASHSCREEN, LOGO, FONT
from soundfactory import Music
from fontfactory import GameText
from controlscreen import Controls


class GameEngine(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.screen = SCREEN.display
        self.fpsClock = pygame.time.Clock()
        self.fps = GAME.fps
        self.ticks = 0
        self.firstrun = True

        self.music = Music("mainmenu.ogg", 0.5, -1)
        self.menu_music = False
        self.game_music = False

        self.game_time = GameText("0", 24, True)
        self.game_time.font_file = FONT.default
        self.game_time.centerx = SCREEN.width/2
        self.game_time.y = 18
        self.game_time.color = COLOR.white
        self.game_time.create()
        self.timer_red = False
        self.flash_timer = 0

        self.p1_score = GameText("0", 24, True)
        self.p1_score.font_file = FONT.default
        self.p1_score.left = 30
        self.p1_score.y = 18
        self.p1_score.color = COLOR.blue_sea
        self.p1_score.create()

        self.p2_score = GameText("0", 24, True)
        self.p2_score.font_file = FONT.default
        self.p2_score.right = SCREEN.width - 30
        self.p2_score.y = 18
        self.p2_score.color = COLOR.petal_green
        self.p2_score.create()

        self.state = STATE.logo
        self.stage_number = 1
        self.stage = Stage(self.stage_number)
        self.hi_score = 0
        self.splashscreen = SplashScreen(0, 0, SPLASHSCREEN.width, SPLASHSCREEN.height)
        self.logoscreen = LogoScreen(0, 0, LOGO.width, LOGO.height)
        self.timer = GAME.time
        self.totalscore = 0

        self.p1_scores = {}
        self.p2_scores = {}

        self.camera = Camera(self.complex_camera, self.stage.level.width, self.stage.level.height)        

        self.bg = SCREEN.bg
        self.screen_color = (choice(COLOR.colors))
        self.menu = Menu(SCREEN.width, SCREEN.height, self.screen_color)
        self.score_screen = ScoreScreen()
        self.controls_screen = Controls()

        self.screen_number = 1
        self.capture_video = False

        self.countdownOverlay = CountDownOverlay()
        self.intro = True
        self.intro_countdown = self.fps * 4
        
        self.scanlines = ScanLines()

        try:
            self.player1_joy = pygame.joystick.Joystick(0)
            self.player1_joy.init()
        except:
            pass

    def reset(self):
        self.stage_number += 1
        if self.stage_number > self.stage.number_of_levels:
            self.stage_number = 1
            self.state = STATE.menu
            self.score_screen = ScoreScreen()
            self.controls_screen = Controls()
            self.firstrun = True
        else:
            self.firstrun = False
            self.state = STATE.game

        self.stage = Stage(self.stage_number)
        self.timer = GAME.time
        self.camera = Camera(self.complex_camera, self.stage.level.width, self.stage.level.height)
        self.screen_color = (choice(COLOR.colors))
        self.menu = Menu(SCREEN.width, SCREEN.height, self.screen_color)
        
        self.countdownOverlay = CountDownOverlay()
        self.intro = True
        self.intro_countdown = self.fps * 4        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = STATE.menu
                if event.key == K_p:
                    if not self.capture_video:
                        self.capture_video = True
                    else:
                        self.capture_video = False
                if event.key == K_q:
                    self.stage.level.spawn_data()
            if self.state == STATE.game:                
                if self.stage.level.timer == 0:
                    self.stage.level.timer = pygame.time.get_ticks()/1000.0
                self.stage.level.player1.handle_events(event)
                self.stage.level.player2.handle_events(event)
            elif self.state == STATE.menu:
                self.menu.handle_events(event)
                self.state = self.menu.state
            elif self.state == STATE.controls:
                self.controls_screen.handle_events(event)
                self.state = self.controls_screen.state
            elif self.state == STATE.scorescreen:
                self.score_screen.handle_events(event)
                self.state = self.score_screen.state
            elif self.state == STATE.exit:
                pygame.quit()
                sys.exit()

    def update(self):
        if self.state == STATE.nextlevel:
            self.reset()
            return
        if self.capture_video:
            self.makeVideo()

        if self.timer == 0:
            self.state = STATE.scorescreen

        if self.state == STATE.logo:
            self.logoscreen.update()
            self.state = self.logoscreen.state
        if self.state == STATE.splashscreen:
            self.splashscreen.update()
            self.state = self.splashscreen.state
        elif self.state == STATE.controls:
            self.controls_screen.update()
        elif self.state == STATE.menu:
            self.menu.update()
        elif self.state == STATE.scorescreen:
            self.p1_scores[self.stage_number-1] = self.stage.level.p1_data
            self.p2_scores[self.stage_number-1] = self.stage.level.p2_data

            self.score_screen.p1_scores[self.stage_number-1].text = self.stage.level.p1_data
            self.score_screen.p2_scores[self.stage_number-1].text = self.stage.level.p2_data

            self.score_screen.update(self.stage_number, 1, self.hi_score)
        elif self.state == STATE.game:
            self.camera.update(self.stage.level.player1)
            if self.intro_countdown <= GAME.fps:
                self.intro = False
                self.intro_countdown = 0
            if self.intro:
                self.countdownOverlay.update(self.intro_countdown)
                self.intro_countdown -= 1
            else:
                self.stage.level.update()
                if self.stage.level.intro:
                    self.timer = GAME.time
                if self.ticks > self.fps:
                    self.ticks = 0
                    self.timer -= 1
                else:
                    self.ticks += 1

            display_time = self.format_timer(self.timer)
            self.game_time.text = display_time
            if self.timer_red:
                self.animate_flash()
            else:
                self.game_time.color = COLOR.white
            self.game_time.update()

            self.p1_score.text = str(self.stage.level.p1_data)
            self.p1_score.update()

            self.p2_score.text = str(self.stage.level.p2_data)
            self.p2_score.update()

    def draw(self):
        self.screen.fill(COLOR.black)

        if self.state == STATE.logo:
            self.logoscreen.draw(self.screen)
        elif self.state == STATE.splashscreen:
            self.splashscreen.draw(self.screen)
        elif self.state == STATE.scorescreen:
            self.score_screen.draw(self.screen)
        elif self.state == STATE.controls:
            self.controls_screen.draw(self.screen)
        elif self.state == STATE.game:
            self.screen.blit(SCREEN.bg, (0, 0))
            self.screen.blit(ASSET.score_bg, (0, 0))
            self.stage.draw(self.screen)
            for particle in self.stage.level.particles:
                self.screen.blit(particle.image, self.camera.apply(particle))

            self.game_time.draw_to(self.screen)
            self.p1_score.draw_to(self.screen)
            self.p2_score.draw_to(self.screen)

            if self.intro:
                self.countdownOverlay.draw(self.screen)

        elif self.state == STATE.menu:
            self.menu.draw(self.screen)
            if not self.firstrun:
                pass
            
        self.scanlines.draw(self.screen)

    def run_game(self, fps=30):
        self.fps = fps
        while True:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            pygame.display.set_caption("CleanerBot - " + str(int(self.fpsClock.get_fps())) + " fps")
            self.fpsClock.tick(self.fps)

    def complex_camera(self, camera_rect, target_rect):
        x, y, dummy, dummy = target_rect
        dummy, dummy, w, h = camera_rect
        x, y = int(SCREEN.width/2)-x, int(SCREEN.height/2) - y

        x = min(0, x)
        x = max(-(camera_rect.width-SCREEN.width), x)
        y = max(-(camera_rect.height-SCREEN.height), y)
        y = min(0, y)

        return pygame.Rect(x, y, w, h)

    def format_timer(self, timer):
        self.timer_red = False
        minutes = timer/60
        seconds = timer % 60
        if minutes == 0 and seconds < 10:
            self.timer_red = True
        if seconds < 10:
            seconds = "0" + str(seconds)
        return str(minutes)+":"+str(seconds)

    def makeVideo(self):
        pygame.image.save(self.screen, os.path.join("screenshots", "screenshot%d.jpg" %self.screen_number))
        self.screen_number += 1

    def animate_flash(self):
        self.flash_timer += 1
        if self.flash_timer < GAME.fps/4:
            self.game_time.color = COLOR.white
        elif self.flash_timer < GAME.fps/2:
            self.game_time.color = COLOR.red
        else:
            self.flash_timer = 0
