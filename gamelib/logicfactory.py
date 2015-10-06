import pygame
import sys, os
from pygame import *
from constants import SCREEN, COLOR, STATE, GAME, COLOR
from levelfactory import Stage
from camera import Camera
from uifactory import Menu

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

        self.font = pygame.font.Font(os.path.join("assets", "fonts", "tinyfont.ttf"), 40)
        self.font.set_bold(False)
        self.text = self.font.render("0 MB", True, (0, 0, 0), (250, 250, 250))
        self.textRect = self.text.get_rect()
        self.textRect.y = 30

        self.totalData = self.font.render("0 MB", True, (0, 0, 0), (250, 250, 250))
        self.dataRect = self.totalData.get_rect()
        self.dataRect.y = 30

        self.state = STATE.menu
        self.stage = Stage()
        self.timer = GAME.time
        self.totalscore = 0

        self.camera = Camera(self.complex_camera, self.stage.level.width, self.stage.level.height)
        self.menu = Menu(SCREEN.width, SCREEN.height)

        self.bg = SCREEN.bg
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
        self.menu = Menu(SCREEN.width, SCREEN.height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = STATE.menu
                if event.key == K_p:
                    pygame.image.save(self.screen, os.path.join("screenshots", "screen01.jpg"))
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
            elif self.state == "exit":
                pygame.quit()
                sys.exit()

    def update(self):
        self.camera.update(self.stage.level.player1)
        self.menu.update()
        if self.timer == 0:
            self.reset()

        if self.stage == STATE.menu:
            self.menu.update()
        elif self.state == STATE.game:
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
            self.text = self.font.render(displayTime, True, COLOR.white)
            self.textRect = self.text.get_rect()
            self.textRect.centerx = self.screen.get_rect().centerx
            self.textRect.y = 10

            self.totalData = self.font.render(str(self.stage.level.storedData) + "MB", True, COLOR.white)
            self.dataRect = self.totalData.get_rect()
            self.dataRect.right = self.screen.get_rect().right - 30
            self.dataRect.y = 10
            self.totalscore = self.stage.level.storedData

    def draw(self):
        self.screen.fill(COLOR.white)
        self.screen.blit(self.bg, (0,0))

        if self.state == STATE.game:
            #self.screen.blit(self.bg, (0,0))
            for entity in self.stage.level.display_group:
                self.screen.blit(entity.image, self.camera.apply(entity))
            for particle in self.stage.level.particles:
                self.screen.blit(particle.image, self.camera.apply(particle))
            self.screen.blit(self.text, self.textRect)
            self.screen.blit(self.totalData, self.dataRect)

        elif self.state == STATE.menu:
            self.screen.blit(self.menu.bg, self.menu.bg.get_rect())
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