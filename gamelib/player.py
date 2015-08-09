import pygame
from pygame.locals import *
from physicsbody import PhysicsBody
from constants import WORLD

class Player(PhysicsBody):
    def __init__(self, x, y , width, height, animationFrames):
        image = animationFrames.get_walk_frames()[0]
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.jumpHeight = -5
        self.speed = 7
        self.jumping = False

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_o and not self.jumping:
                self.vspeed = self.jumpHeight
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d:
                self.hspeed = 0

    def update(self):
        key = pygame.key.get_pressed()
        if key[K_a]:
            if self.rect.x <= 0: # Avoid disappearing on left side of screen
                self.hspeed = 0
            else:
                self.hspeed = -self.speed
        elif key[K_d]:
            self.hspeed = self.speed

        self.move(self.hspeed, self.vspeed)