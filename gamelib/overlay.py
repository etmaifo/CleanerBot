import pygame, os
from gamelib.constants import COLOR, SCREEN, ASSET, GAME, FONT
from gamelib.physicsbody import PhysicsBody
import pygame.mixer as mixer


class CountDownOverlay(object):
    def __init__(self):
        mixer.init()
        self.overlay = PhysicsBody(0, SCREEN.height/5, SCREEN.width * 3/4, 37, ASSET.countdown_overlay)
        self.overlay.rect.centerx = SCREEN.width/2
        self.font = pygame.font.Font(FONT.default, 20)
        self.font.set_bold(True)
        self.text = self.font.render("3", True, COLOR.white)

        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.overlay.rect.center
        self.sound = mixer.Sound(os.path.join("assets", "sfx", "start.wav"))
        self.sound.set_volume(0.3)
        self.sound_playing = False
        self.blink = 0

    def update(self, remainingSeconds):
        self.blink += 1
        if self.blink > GAME.fps:
            self.blink = 0
        seconds = str(int(remainingSeconds/GAME.fps)-1)
        if seconds == "0":
            seconds = "GO!"
            if not self.sound_playing:
                self.sound.play()
                self.sound_playing = True
        self.text = self.font.render(seconds, True, COLOR.white)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.overlay.rect.center

    def draw(self, screen):
        if self.blink < GAME.fps/2:
            screen.blit(self.overlay.image, self.overlay.rect)
            screen.blit(self.text, self.text_rect)