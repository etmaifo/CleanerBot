import pygame, os, sys
from pygame.locals import *
from constants import COLOR, MENU, SCREEN, STATE, ASSET, GAME
from physicsbody import PhysicsBody
import pygame.mixer as mixer


class Menu(object):
    def __init__(self, width, height, color):
        mixer.init()

        self.width = width
        self.height = height
        self.cursor_index = 0
        self.title_font = pygame.font.Font(os.path.join("assets", "fonts", "tinyfont.ttf"), 100)
        self.title_font.set_bold(True)
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "showg.ttf"), 24)
        self.font.set_bold(True)
        self.color = color
        self.title = self.title_font.render("CleanerBot", True, COLOR.white)
        self.text_play = self.font.render("Play", True, self.color)
        self.text_controls = self.font.render("Controls", True, COLOR.white)
        self.text_exit = self.font.render("Exit", True, COLOR.white)
        self.bg = MENU.menuScreen
        self.button = PhysicsBody(0, 250, SCREEN.width, 48, MENU.button)
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
        self.overlay = PhysicsBody(0, SCREEN.height/5, SCREEN.width * 3/4, 37, ASSET.countdown_overlay)
        self.overlay.rect.centerx = SCREEN.width/2
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "hoog0553.ttf"), 20)
        self.font.set_bold(True)
        self.text = self.font.render("3", True, COLOR.white)

        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.overlay.rect.center

        self.blink = 0

    def update(self, remainingSeconds):
        self.blink += 1
        if self.blink > GAME.fps:
            self.blink = 0
        seconds = str(remainingSeconds/GAME.fps)
        if seconds == "0":
            seconds = "Start!"
        self.text = self.font.render(seconds, True, COLOR.white)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.overlay.rect.center

    def draw(self, screen):
        if self.blink < GAME.fps/2:
            screen.blit(self.overlay.image, self.overlay.rect)
            screen.blit(self.text, self.text_rect)