import pygame
import sys, os
from pygame import *
from constants import SCREEN, COLOR
from player import Player
from constants import ASSET

class GameEngine(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.screen = pygame.display.set_mode((SCREEN.width, SCREEN.height))
        self.fpsClock = pygame.time.Clock()

        self.player = Player(SCREEN.width/2, SCREEN.width/2, 40, 50, ASSET.player)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            self.player.handle_events(event)

    def update(self):
        self.player.update()

    def draw(self):
        self.screen.fill(COLOR.white)
        self.player.draw(self.screen)
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
