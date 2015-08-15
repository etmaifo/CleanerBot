import pygame
from pygame.locals import *
from physicsbody import PhysicsBody

class Player(PhysicsBody):
    def __init__(self, x, y , width, height, animationFrames):
        image = animationFrames.get_walk_frames()[0]
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.jumpHeight = -18
        self.speed = 5

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if (event.key == K_o or event.key == K_UP) and self.grounded:
                self.vspeed = self.jumpHeight
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d or event.key == K_LEFT or event.key == K_RIGHT:
                self.hspeed = 0

    def update(self):
        self.grounded = False
        key = pygame.key.get_pressed()
        if key[K_a] or key[K_LEFT]:
            if self.rect.x <= 0: # Avoid disappearing on left side of screen
                self.hspeed = 0
            else:
                self.hspeed = -self.speed
        elif key[K_d] or key[K_RIGHT]:
            self.hspeed = self.speed

        self.vspeed += self.gravity
        self.move(self.hspeed, self.vspeed)