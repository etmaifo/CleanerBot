import pygame, os, sys
from pygame.locals import *
from constants import COLOR, MENU, SCREEN, STATE, ASSET
from physicsbody import PhysicsBody
import pygame.mixer as mixer


class Menu(object):
    def __init__(self, width, height, color):
        mixer.init()

        self.width = width
        self.height = height
        self.cursor_index = 0
        self.title_font = pygame.font.Font(os.path.join("assets", "fonts", "molot.ttf"), 100)
        self.title_font.set_bold(True)
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "molot.ttf"), 30)
        self.font.set_bold(True)
        self.color = color
        self.title = self.title_font.render("CleanerBot", True, COLOR.white)
        self.text_play = self.font.render("Play", True, self.color)
        self.text_controls = self.font.render("Controls", True, COLOR.white)
        self.text_exit = self.font.render("Exit", True, COLOR.white)
        self.bg = MENU.menuScreen
        self.button = PhysicsBody(0, 250, SCREEN.width, 58, MENU.button)
        self.button_pos = 0
        self.state = STATE.menu
        self.assemble()

        self.nav_sound = mixer.Sound(os.path.join("assets", "sfx", "menu_nav.wav"))
        self.nav_sound.set_volume(0.5)



    def handle_events(self, event):
        self.state = STATE.menu
        if event.type == KEYDOWN:
            if (event.key == K_DOWN or event.key == K_s) and self.button_pos < 2:
                self.button.rect.y += self.button.rect.height
                self.button_pos += 1
                self.nav_sound.play()
            elif (event.key == K_UP or event.key == K_w) and self.button_pos > 0:
                self.button.rect.y -= self.button.rect.height
                self.button_pos -= 1
                self.nav_sound.play()
            elif event.key == K_RETURN:
                if self.button_pos == 0:
                    self.state = STATE.game
                elif self.button_pos == 2:
                    pygame.quit()
                    sys.exit()

    def assemble(self):
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = SCREEN.width / 2
        self.title_rect.y = 50

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
        self.text_play = self.font.render("Play", True, COLOR.white)
        self.text_controls = self.font.render("Controls", True, COLOR.white)
        self.text_exit = self.font.render("Exit", True, COLOR.white)

        if self.play_rect.colliderect(self.button.rect):
            self.text_play = self.font.render("Play", True, self.color)
        elif self.controls_rect.colliderect(self.button.rect):
            self.text_controls = self.font.render("Controls", True, self.color)
        elif self.exit_rect.colliderect(self.button.rect):
            self.text_exit = self.font.render("Exit", True, self.color)

    def draw(self, screen):
        screen.blit(self.title, self.title_rect)
        screen.blit(self.button.image, self.button.rect)
        screen.blit(self.text_play, self.play_rect)
        screen.blit(self.text_controls, self.controls_rect)
        screen.blit(self.text_exit, self.exit_rect)


class CountDownOverlay(object):
    def __init__(self):
        self.overlay = PhysicsBody(0, SCREEN.height/3, SCREEN.width, 54, ASSET.countdown_overlay)
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "hoog0553.ttf"), 20)
        self.font.set_bold(True)
        self.text = self.font.render("3", True, COLOR.white)

        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.overlay.rect.center

    def update(self, remainingSeconds):
        seconds = str(remainingSeconds + 1)
        self.text = self.font.render(seconds, True, COLOR.white)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.overlay.rect.center

    def draw(self, screen):
        screen.blit(self.overlay.image, self.overlay.rect)
        screen.blit(self.text, self.text_rect)