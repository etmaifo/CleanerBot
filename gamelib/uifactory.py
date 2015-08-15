import pygame, os
from pygame.locals import *
from constants import COLOR

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, text, state, image):
        pygame.sprite.Sprite.__init__(self)
        self.active = False
        self.selected = False
        self.state = state
        self.image = pygame.Surface((150, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hover_image = self.get_surface(os.path.join("assets", "images", "button_hover.png"), 150, 40)
        self.inactive_image = self.get_surface(os.path.join("assets", "images", "button_inactive.png"), 150, 40)
        self.text = text

    def handle_events(self, event):
        if event.type == MOUSEMOTION:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.hover_image
                self.active = True
            else:
                self.image = self.inactive_image
                self.active = False

    def get_surface(self, img, width, height):
        image = pygame.image.load(img)
        image = pygame.transform.smoothscale(image, (width, height))
        self.rect.width = image.get_rect().width
        self.rect.height = image.get_rect().height

        return image

    def center(self, text):
        textRect = text.get_rect()
        textRect.centerx = self.rect.centerx
        textRect.centery = self.rect.centery

        return textRect

    def make_active(self, text):
        """ Makes the button active """
        self.text = self.font.render(text, True, COLOR.green)
        self.active = True

class Menu(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cursor_index = 0

        self.font = pygame.font.Font(os.path.join("assets", "fonts", "tinyfont.ttf"), 30)
        self.text_resume = self.font.render("Resume", True, COLOR.white)
        self.text_play = self.font.render("Play", True, COLOR.white)
        #self.text_settings = self.font.render("Settings", True, COLOR.white)
        #self.text_credits = self.font.render("Credits", True, COLOR.white)
        self.text_exit = self.font.render("Exit", True, COLOR.white)

        self.bg = pygame.image.load(os.path.join("assets", "images", "menuBG.png"))

        self.buttons_group = pygame.sprite.Group()

        self.assemble()

    def handle_events(self, event):
        for button in self.buttons_group:
            button.handle_events(event)

        if event.type == KEYDOWN:
            if event.key == K_s:
                self.cursor_index += 1
            elif event.key == K_w:
                self.cursor_index -= 1

        if self.cursor_index < 0:
            self.cursor_index = 0
        elif self.cursor_index > 3:
            self.cursor_index = 3

    def assemble(self):
        button = None
        for i in range(4): # 4 buttons
            x = self.width/2 - 150/2
            y = 280 + i*60 #(i*40) + (i*20)
            if i == 0:
                button = MenuButton(x, y, self.text_play, "game", "img")
                '''
            elif i == 1:
                button = MenuButton(x, y, self.text_settings, "settings", "img")
            elif i == 2:
                button = MenuButton(x, y, self.text_credits, "credits", "img")
                '''
            elif i == 1:
                button = MenuButton(x, y, self.text_exit, "exit", "img")
            self.buttons_group.add(button)

    def get_active_state(self):
        for button in self.buttons_group:
            if button.active:
                return button.state
        return "menu"

    def add_resume_button(self):
        for button in self.buttons_group:
            if button.state == "game":
                button.text = self.text_resume

    def update(self):
        pass


class ScoreScreen(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.Font(os.path.join("assets", "fonts", "tinyfont.ttf"), 30)
        self.text_next = self.font.render("Resume", True, COLOR.white)
        self.text_exit = self.font.render("Exit", True, COLOR.white)

        self.bg = pygame.image.load(os.path.join("assets", "images", "menuBG.png"))
        self.buttons_group = pygame.sprite.Group()

        self.assemble()

    def handle_events(self, event):
        for button in self.buttons_group:
            button.handle_events(event)

        if event.type == KEYDOWN:
            if event.key == K_s:
                self.cursor_index += 1
            elif event.key == K_w:
                self.cursor_index -= 1

        if self.cursor_index < 0:
            self.cursor_index = 0
        elif self.cursor_index > 3:
            self.cursor_index = 3

    def assemble(self):
        button = None
        for i in range(4): # 4 buttons
            x = self.width/2 - 150/2
            y = 280 + i*60 #(i*40) + (i*20)
            if i == 0:
                button = MenuButton(x, y, self.text_next, "game", "img")
            elif i == 1:
                button = MenuButton(x, y, self.text_exit, "exit", "img")
            self.buttons_group.add(button)

    def get_active_state(self):
        for button in self.buttons_group:
            if button.active:
                return button.state
        return "menu"

    def add_resume_button(self):
        for button in self.buttons_group:
            if button.state == "game":
                button.text = self.text_resume

    def update(self):
        pass
