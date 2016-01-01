from constants import SCREEN, STATE, ASSET, GAME
from physicsbody import PhysicsBody


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