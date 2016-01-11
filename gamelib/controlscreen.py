import os
from pygame.locals import *
from scorescreen import ScoreScreen
from fontfactory import GameText
from constants import SCREEN, COLOR, ASSET, STATE
import pygame.mixer as mixer


class Controls(ScoreScreen):
    def __init__(self):
        ScoreScreen.__init__(self)
        mixer.init()
        self.title = GameText("Controls", 94)
        self.title.centerx = SCREEN.width / 2
        self.title.y = 48
        self.title.color = COLOR.half_black
        self.title.create()

        self.bg = ASSET.controls
        self.state = STATE.controls

        self.select_sound = mixer.Sound(os.path.join("assets", "sfx", "sfx_twoTone.ogg"))
        self.select_sound.set_volume(0.5)

    def handle_events(self, event):
        self.state = STATE.controls
        if event.type == KEYDOWN:
            if event.key == K_e or event.key == K_RETURN:
                self.state = STATE.menu
                self.select_sound.play()

        elif event.type == JOYBUTTONDOWN:
            if self.controller.get_button(0):
                self.state = STATE.menu
                self.select_sound.play()

    def update(self):
        self.title.update()

    def draw(self, screen):
        screen.fill(COLOR.black)
        screen.blit(self.bg, (0, 0))
        self.title.draw_to(screen)