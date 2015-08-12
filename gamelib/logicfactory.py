import pygame
import sys, os
from pygame import *
from constants import SCREEN, COLOR
from levelfactory import Stage
from camera import Camera

class GameEngine(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.screen = pygame.display.set_mode((SCREEN.width, SCREEN.height))
        self.fpsClock = pygame.time.Clock()

        self.stage = Stage()

        self.camera = Camera(self.complex_camera, self.stage.level.width, self.stage.level.height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            self.stage.level.player.handle_events(event)

    def update(self):
        self.camera.update(self.stage.level.player)
        self.stage.level.update()
        #self.stage.update()

    def draw(self):
        self.screen.fill(COLOR.gray)
        for entity in self.stage.level.entities:
            self.screen.blit(entity.image, self.camera.apply(entity))
        #self.screen.blit(self.bg.image, self.screen.get_rect())

    def run_game(self, fps=30):
        self.fps = fps
        while True:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            pygame.display.set_caption("Cosmic Dust - " + str(int(self.fpsClock.get_fps())) + " fps")
            self.fpsClock.tick(self.fps)

    def complex_camera(self, cameraRect, target_rect):
        x, y, dummy, dummy = target_rect
        dummy, dummy, w, h = cameraRect
        x, y  = int(SCREEN.width/2)-x, int(SCREEN.height/2) - y

        x = min(0, x)
        x = max(-(cameraRect.width-SCREEN.width), x)
        y = max(-(cameraRect.height-SCREEN.height), y)
        y = min(0, y)

        return pygame.Rect(x, y, w, h)