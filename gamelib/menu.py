import pygame
import os, sys
from pygame.locals import *
from gamelib.constants import COLOR, MENU, SCREEN, STATE, ASSET, TITLE, FONT
from gamelib.physicsbody import PhysicsBody
import pygame.mixer as mixer


class Menu(object):
    def __init__(self, width, height, color):
        mixer.init()

        self.width = width
        self.height = height
        self.cursor_index = 0
        self.title_font = pygame.font.Font(FONT.default, 100)
        self.title_font.set_bold(True)
        self.font = pygame.font.Font(FONT.default, 24)
        self.font.set_bold(True)
        self.color = color
        self.title = PhysicsBody(0, 0, TITLE.width, TITLE.height, ASSET.title)
        self.text_play = self.font.render("Play", True, self.color)
        self.text_controls = self.font.render("Controls", True, COLOR.half_black)
        self.text_exit = self.font.render("Exit", True, COLOR.half_black)
        self.bg = MENU.menuScreen
        self.button = PhysicsBody(0, 250, MENU.buttonWidth, MENU.buttonHeight, MENU.button)
        self.button.rect.centerx = SCREEN.width/2
        self.button_pos = 0
        self.state = STATE.menu
        self.timer = 0
        self.overlay = ASSET.overlay.convert()

        self.assemble()

        self.nav_sound = mixer.Sound(os.path.join("assets", "sfx", "nav.wav"))
        self.nav_sound.set_volume(0.5)
        self.select_sound = mixer.Sound(os.path.join("assets", "sfx", "sfx_twoTone.ogg"))
        self.select_sound.set_volume(0.5)

        self.controller = self.get_controller()

    def get_controller(self):
        number_of_joysticks = pygame.joystick.get_count()
        if number_of_joysticks > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            return joystick
        return None

    def handle_events(self, event):
        self.state = STATE.menu
        if event.type == KEYDOWN:
            if (event.key == K_s) and self.button_pos < 2:
                self.button.rect.y += self.button.rect.height
                self.button_pos += 1
                self.nav_sound.play()
            elif (event.key == K_w) and self.button_pos > 0:
                self.button.rect.y -= self.button.rect.height
                self.button_pos -= 1
                self.nav_sound.play()
            elif event.key == K_e or event.key == K_RETURN:
                self.select_sound.play()
                if self.button_pos == 0:
                    self.state = STATE.game
                elif self.button_pos == 1:
                    self.state = STATE.controls
                elif self.button_pos == 2:
                    pygame.quit()
                    sys.exit()

        elif event.type == JOYHATMOTION:
            if (self.controller.get_hat(0)[1] == -1) and self.button_pos < 2:
                self.button.rect.y += self.button.rect.height
                self.button_pos += 1
                self.nav_sound.play()
            elif (self.controller.get_hat(0)[1] == 1) and self.button_pos > 0:
                self.button.rect.y -= self.button.rect.height
                self.button_pos -= 1
                self.nav_sound.play()

        elif event.type == JOYBUTTONDOWN:
            if self.controller.get_button(0):
                self.select_sound.play()
                if self.button_pos == 0:
                    self.state = STATE.game
                elif self.button_pos == 1:
                    self.state = STATE.controls
                elif self.button_pos == 2:
                    pygame.quit()
                    sys.exit()

    def assemble(self):
        self.title.rect.centerx = SCREEN.width / 2
        self.title.rect.y = 50

        self.play_rect = self.text_play.get_rect()
        self.play_rect.centerx = SCREEN.width/2
        self.play_rect.centery = self.button.rect.centery

        self.controls_rect = self.text_controls.get_rect()
        self.controls_rect.centerx = SCREEN.width/2
        self.controls_rect.centery = self.button.rect.centery + self.button.rect.height

        self.exit_rect = self.text_exit.get_rect()
        self.exit_rect.centerx = SCREEN.width/2
        self.exit_rect.centery = self.button.rect.centery + self.button.rect.height * 2

    def update(self):
        self.animate_overlay()
        self.text_play = self.font.render("Play", True, COLOR.gray7)
        self.text_controls = self.font.render("Controls", True, COLOR.gray7)
        self.text_exit = self.font.render("Exit", True, COLOR.gray7)

        if self.play_rect.colliderect(self.button.rect):
            self.text_play = self.font.render("Play", True, COLOR.half_black)
        elif self.controls_rect.colliderect(self.button.rect):
            self.text_controls = self.font.render("Controls", True, COLOR.half_black)
        elif self.exit_rect.colliderect(self.button.rect):
            self.text_exit = self.font.render("Exit", True, COLOR.half_black)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        if self.timer > 32:
            screen.blit(self.title.image, self.title)
            screen.blit(self.button.image, self.button.rect)
            screen.blit(self.text_play, self.play_rect)
            screen.blit(self.text_controls, self.controls_rect)
            screen.blit(self.text_exit, self.exit_rect)
        screen.blit(self.overlay, (0, 0))

    def animate_overlay(self):
        if self.timer < 255:
            self.timer += 1
            self.overlay.set_alpha(255 - self.timer * 2)