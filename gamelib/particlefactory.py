from random import randrange
from physicsbody import PhysicsBody
from constants import GAME
import pygame

class Particle(PhysicsBody):
    def __init__(self, x, y, width, height, image):
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.image = pygame.transform.smoothscale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timeout = 0

        self.vspeed = randrange(-13, -3)
        self.hspeed = randrange(-3, 4, 1)

    def update(self):
        self.timeout += 1
        if self.timeout >= 1 * GAME.fps:
            self.kill()
        self.vspeed += 0.5 #WORLD.gravity
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed