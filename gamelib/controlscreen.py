import pygame
from pygame.locals import *
from scorescreen import ScoreScreen
from fontfactory import GameText
from constants import SCREEN, COLOR, ASSET, STATE


class Controls(ScoreScreen):
    def __init__(self):
        ScoreScreen.__init__(self)
        self.title = GameText("Controls", 94)
        self.title.centerx = SCREEN.width / 2
        self.title.y = 48
        self.title.color = COLOR.half_black
        self.title.create()

        self.bg = ASSET.controls
        self.state = STATE.controls

    def handle_events(self, event):
        self.state = STATE.controls
        if event.type == KEYDOWN:
            if event.key == K_e or event.key == K_RETURN:
                self.state = STATE.menu

        elif event.type == JOYBUTTONDOWN:
            if self.controller.get_button(0):
                self.state = STATE.menu

    def update(self):
        self.title.update()

    def draw(self, screen):
        screen.fill(COLOR.black)
        screen.blit(self.bg, (0, 0))
        self.title.draw_to(screen)