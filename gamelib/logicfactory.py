import pygame
import sys, os
from pygame import *
from random import choice
from constants import SCREEN, COLOR, STATE, GAME, ASSET
from levelfactory import Stage
from camera import Camera
from uifactory import Menu, CountDownOverlay

class GameEngine(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        joystick_count = pygame.joystick.get_count()
        print "%d connected." %joystick_count

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.screen = pygame.display.set_mode((SCREEN.width, SCREEN.height))
        self.fpsClock = pygame.time.Clock()
        self.fps = GAME.fps
        self.ticks = 0
        self.firstrun = True

        pygame.mixer.music.load(os.path.join("assets", "music", "galactic.ogg"))
        #pygame.mixer.music.play()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "molot.ttf"), 30)
        self.font.set_bold(False)
        self.time_font = pygame.font.Font(os.path.join("assets", "fonts", "hoog0553.ttf"), 20)
        self.time_font.set_bold(True)
        self.gameTime = self.font.render("0", True, (0, 0, 0), (250, 250, 250))
        self.textRect = self.gameTime.get_rect()
        self.textRect.y = 30

        self.p1_score = self.font.render("0", True, (0, 0, 0), (250, 250, 250))
        self.p1_score_rect = self.p1_score.get_rect()
        self.p1_score_rect.y = 30

        self.p2_score = self.font.render("0", True, (0, 0, 0), (250, 250, 250))
        self.p2_score_rect = self.p2_score.get_rect()
        self.p2_score_rect.y = 30

        self.state = STATE.menu
        self.stage = Stage()
        self.timer = GAME.time
        self.totalscore = 0

        self.camera = Camera(self.complex_camera, self.stage.level.width, self.stage.level.height)        

        self.bg = SCREEN.bg
        self.screen_color = (choice(COLOR.colors))
        self.menu = Menu(SCREEN.width, SCREEN.height, self.screen_color)

        self.screen_number = 1
        self.capture_video = False

        self.countdownOverlay = CountDownOverlay()
        self.intro = True
        self.intro_countdown = self.fps * 3

        try:
            self.player1_joy = pygame.joystick.Joystick(0)
            self.player1_joy.init()
        except:
            pass

    def reset(self):
        self.firstrun = False
        self.state = STATE.menu
        self.stage = Stage()
        self.timer = GAME.time
        self.camera = Camera(self.complex_camera, self.stage.level.width, self.stage.level.height)
        self.screen_color = (choice(COLOR.colors))
        self.menu = Menu(SCREEN.width, SCREEN.height, self.screen_color)        
        
        self.countdownOverlay = CountDownOverlay()
        self.intro = True
        self.intro_countdown = self.fps * 3        

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
            elif self.state == STATE.exit:
                pygame.quit()
                sys.exit()

    def update(self):
        print self.state
        if self.capture_video:
            self.makeVideo()

        self.camera.update(self.stage.level.player1)
        self.menu.update()
        if self.timer == 0:
            self.reset()

        if self.stage == STATE.menu:
            self.menu.update()
        elif self.state == STATE.game:
            if self.intro_countdown <= 0:
                self.intro = False
                self.intro_countdown = 0
            if self.intro:
                self.countdownOverlay.update(self.intro_countdown/self.fps)
                self.intro_countdown -= 1
            else:
                self.stage.level.update()
                self.stage.update()
                if self.stage.level.intro:
                    self.timer = 60
                if self.ticks > self.fps:
                    self.ticks = 0
                    self.timer -= 1
                else:
                    self.ticks += 1

            displayTime = self.format_timer(self.timer)
            self.gameTime = self.time_font.render(displayTime, True, COLOR.white)
            self.textRect = self.gameTime.get_rect()
            self.textRect.centerx = self.screen.get_rect().centerx
            self.textRect.y = 18

            self.p1_score = self.font.render(str(self.stage.level.p1_data), True, COLOR.white)
            self.p1_score_rect = self.p1_score.get_rect()
            self.p1_score_rect.left = 30
            self.p1_score_rect.y = 10

            self.p2_score = self.font.render(str(self.stage.level.p2_data), True, COLOR.white)
            self.p2_score_rect = self.p2_score.get_rect()
            self.p2_score_rect.right = self.screen.get_rect().right - 30
            self.p2_score_rect.y = 10
            self.totalscore = self.stage.level.p1_data

    def draw(self):
        self.screen.fill(COLOR.white)
        self.screen.fill(self.screen_color)        

        if self.state == STATE.game:
            self.screen.blit(ASSET.score_bg, (0, 0))
            for entity in self.stage.level.display_group:
                self.screen.blit(entity.image, self.camera.apply(entity))
            for particle in self.stage.level.particles:
                self.screen.blit(particle.image, self.camera.apply(particle))
            self.screen.blit(self.gameTime, self.textRect)
            self.screen.blit(self.p1_score, self.p1_score_rect)
            self.screen.blit(self.p2_score, self.p2_score_rect)

            if self.intro:
                self.countdownOverlay.draw(self.screen)

        elif self.state == STATE.menu:
            #self.screen.blit(self.menu.bg, self.menu.bg.get_rect())
            self.menu.draw(self.screen)
            if not self.firstrun:
                pass

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
        x, y  = int(SCREEN.width/2)-x, int(SCREEN.height/2) - y

        x = min(0, x)
        x = max(-(camera_rect.width-SCREEN.width), x)
        y = max(-(camera_rect.height-SCREEN.height), y)
        y = min(0, y)

        return pygame.Rect(x, y, w, h)

    def format_timer(self, timer):
        minutes = timer/60
        seconds = timer % 60
        if seconds < 10:
            seconds = "0" + str(seconds)
        return str(minutes)+":"+str(seconds)

    def makeVideo(self):
        pygame.image.save(self.screen, os.path.join("screenshots", "screenshot%d.jpg" %self.screen_number))
        self.screen_number += 1        