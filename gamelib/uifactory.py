import pygame, os
from pygame.locals import *
from constants import COLOR, MENU, SCREEN
from physicsbody import PhysicsBody


class Menu(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cursor_index = 0
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "hoog0553.ttf"), 26)
        self.font.set_bold(True)
        self.text_human = self.font.render("VS Human", True, COLOR.blue)
        self.text_ai = self.font.render("VS A.I.", True, COLOR.white)
        self.text_controls = self.font.render("Controls", True, COLOR.white)
        self.text_exit = self.font.render("Exit", True, COLOR.white)
        self.bg = MENU.menuScreen
        self.button = PhysicsBody(0, 200, SCREEN.width, 58, MENU.button)
        self.button_pos = 0

        self.assemble()

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if (event.key == K_DOWN or event.key == K_s) and self.button_pos < 3:
                self.button.rect.y += self.button.rect.height
                self.button_pos += 1
            elif (event.key == K_UP or event.key == K_w) and self.button_pos > 0:
                self.button.rect.y -= self.button.rect.height
                self.button_pos -= 1
            elif event.key == K_RETURN:
                if self.button_pos == 0:
                    self.state

    def assemble(self):
        self.human_rect = self.text_human.get_rect()
        self.human_rect.centerx = SCREEN.width/2
        self.human_rect.centery = self.button.rect.centery

        self.ai_rect = self.text_ai.get_rect()
        self.ai_rect.centerx = SCREEN.width/2
        self.ai_rect.centery = self.button.rect.centery + self.button.rect.height

        self.controls_rect = self.text_controls.get_rect()
        self.controls_rect.centerx = SCREEN.width/2
        self.controls_rect.centery = self.button.rect.centery + self.button.rect.height * 2

        self.exit_rect = self.text_exit.get_rect()
        self.exit_rect.centerx = SCREEN.width/2
        self.exit_rect.centery = self.button.rect.centery + self.button.rect.height * 3

    def update(self):
        self.text_human = self.font.render("VS Human", True, COLOR.white)
        self.text_ai = self.font.render("VS A.I.", True, COLOR.white)
        self.text_controls = self.font.render("Controls", True, COLOR.white)
        self.text_exit = self.font.render("Exit", True, COLOR.white)

        if self.human_rect.colliderect(self.button.rect):
            self.text_human = self.font.render("VS Human", True, COLOR.blue)
        elif self.ai_rect.colliderect(self.button.rect):
            self.text_ai = self.font.render("VS A.I.", True, COLOR.blue)
        elif self.controls_rect.colliderect(self.button.rect):
            self.text_controls = self.font.render("Controls", True, COLOR.blue)
        elif self.exit_rect.colliderect(self.button.rect):
            self.text_exit = self.font.render("Exit", True, COLOR.blue)

    def draw(self, screen):
        screen.blit(self.button.image, self.button.rect)
        screen.blit(self.text_human, self.human_rect)
        screen.blit(self.text_ai, self.ai_rect)
        screen.blit(self.text_controls, self.controls_rect)
        screen.blit(self.text_exit, self.exit_rect)