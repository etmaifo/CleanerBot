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
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "tinyfont.ttf"), 24)
        self.font.set_bold(True)
        self.color = color
        self.title = self.title_font.render("CleanerBot", True, COLOR.half_black)
        self.text_play = self.font.render("Play", True, self.color)
        self.text_controls = self.font.render("Controls", True, COLOR.half_black)
        self.text_exit = self.font.render("Exit", True, COLOR.half_black)
        self.bg = MENU.menuScreen
        self.button = PhysicsBody(0, 250, MENU.buttonWidth, MENU.buttonHeight, MENU.button)
        self.button.rect.centerx = SCREEN.width/2
        self.button_pos = 0
        self.state = STATE.menu
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
        self.text = self.font.render("3", True, COLOR.ice_blue)

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
        self.text = self.font.render(seconds, True, COLOR.ice_blue)
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

        self.assemble()


    def assemble(self):
        self.logo.rect.center = (SCREEN.width/2, SCREEN.height/2)

    def update(self):
        self.animate()
        self.timer += 1
        if self.timer >= GAME.fps * 7:
            self.timeout = True

        if self.timeout:
            self.state = STATE.menu
            
    def draw(self, screen):
        screen.fill((16, 16, 16))
        screen.blit(self.logo.image, self.logo.rect)

    def animate(self):
        #image = self.image
        if self.timer >= GAME.fps * 2:
            alpha = 254
            self.logo.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            