
import pygame
import os, sys
from pygame.locals import *
from constants import COLOR, MENU, SCREEN, STATE, ASSET, GAME, TITLE
from physicsbody import PhysicsBody
from fontfactory import GameText
import pygame.mixer as mixer


class Menu(object):
    def __init__(self, width, height, color):
        mixer.init()

        self.width = width
        self.height = height
        self.cursor_index = 0
        self.title_font = pygame.font.Font(os.path.join("assets", "fonts", "hoog0553.ttf"), 100)
        self.title_font.set_bold(True)
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "hoog0553.ttf"), 24)
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

        self.nav_sound = mixer.Sound(os.path.join("assets", "sfx", "flashlight off.wav"))
        self.nav_sound.set_volume(0.5)
        self.select_sound = mixer.Sound(os.path.join("assets", "sfx", "comical pop and swirl.wav"))
        self.select_sound.set_volume(0.1)

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
        self.text_play = self.font.render("Play", True, COLOR.half_black)
        self.text_controls = self.font.render("Controls", True, COLOR.half_black)
        self.text_exit = self.font.render("Exit", True, COLOR.half_black)
        
        if self.play_rect.colliderect(self.button.rect):
            self.text_play = self.font.render("Play", True, COLOR.petal_green)
        elif self.controls_rect.colliderect(self.button.rect):
            self.text_controls = self.font.render("Controls", True, COLOR.petal_green)
        elif self.exit_rect.colliderect(self.button.rect):
            self.text_exit = self.font.render("Exit", True, COLOR.petal_green)
    

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
            

class ScanLines(object):
    def __init__(self):
        self.collection = pygame.sprite.Group()
        self.assemble()
        
        
    def assemble(self):
        for i in range(160):
            scanline = PhysicsBody(0, i * 4, SCREEN.width, 1, ASSET.scanline)
            self.collection.add(scanline)
            
            
    def draw(self, screen):
        for scanline in self.collection:
            screen.blit(scanline.image, scanline.rect)
            

class SplashScreen(object):
    def __init__(self, x, y, width, height):
        self.logo = PhysicsBody(0, 0, width, height, ASSET.pygame_logo)
        self.timer = 0
        self.timeout = False
        self.state = STATE.splashscreen
        self.overlay = ASSET.overlay
        self.overlay = self.overlay.convert()

        self.assemble()


    def assemble(self):
        self.logo.rect.center = (SCREEN.width/2, SCREEN.height/2)

    def update(self):
        self.animate()
        self.timer += 1
        if self.timer >= GAME.fps * 5:
            self.timeout = True

        if self.timeout:
            self.state = STATE.menu
            
    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.logo.image, self.logo.rect)
        screen.blit(self.overlay, (0, 0))

    def animate(self):
        if self.timer <= 32:
            self.overlay.set_alpha(255 - self.timer * 4)
        elif self.timer > 170:
            self.overlay.set_alpha(self.timer - 20)


class LogoScreen(SplashScreen):
    def __init__(self, x, y, width, height):
        SplashScreen.__init__(self, x, y, width, height)
        self.logo = PhysicsBody(0, 0, width, height, ASSET.studio_logo)
        self.state = STATE.logo

        self.assemble()

    def update(self):
        self.animate()
        self.timer += 1
        if self.timer >= GAME.fps * 5:
            self.timeout = True

        if self.timeout:
            self.state = STATE.splashscreen


class ScoreScreen(object):
    def __init__(self):
        self.title = GameText("Scoreboard", 94)
        self.title.centerx = SCREEN.width / 2
        self.title.y = 48
        self.title.color = COLOR.half_black

        self.hi_score = GameText("Hi-score: 0", 38)
        self.hi_score.centerx = SCREEN.width / 2
        self.hi_score.y = 172
        self.hi_score.color = COLOR.light_gray

        self.p1 = GameText("P1", 20, True)
        self.p1.x = 92
        self.p1.y = 280
        self.p1.color = COLOR.blue_sea

        self.p2 = GameText("P2", 20, True)
        self.p2.x = 92
        self.p2.y = 340
        self.p2.color = COLOR.petal_green

        self.bg = MENU.scoreScreen
        self.state = STATE.scorescreen

        self.title.create()
        self.hi_score.create()
        self.p1.create()
        self.p2.create()

    def handle_events(self, event):
        pass

    def update(self):
        self.title.update()
        self.hi_score.update()
        self.p1.update()
        self.p2.update()

    def draw(self, screen):
        screen.fill(COLOR.black)
        screen.blit(self.bg, (0, 0))
        self.title.draw_to(screen)
        self.hi_score.draw_to(screen)
        self.p1.draw_to(screen)
        self.p2.draw_to(screen)
