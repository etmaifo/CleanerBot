from gamelib.constants import STATE, ASSET, GAME
from gamelib.physicsbody import PhysicsBody
from gamelib.splashscreen import SplashScreen


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
