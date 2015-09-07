import pygame
from pygame.locals import *
from physicsbody import PhysicsBody
from constants import DIRECTION

class Player(PhysicsBody):
    def __init__(self, x, y , width, height, animationFrames):
        image = animationFrames.get_walk_frames()[0]
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.jumpHeight = -18
        self.speed = 5
        self.has_data = False
        self.shoot_data = False
        self.direction = DIRECTION.left

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if (event.key == K_o or event.key == K_UP or event.key == K_SPACE) and self.grounded:
                self.vspeed = self.jumpHeight
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d or event.key == K_LEFT or event.key == K_RIGHT:
                self.hspeed = 0
            if event.key == K_i:
                if self.has_data:
                    self.shoot_data = True

    def update(self):
        self.grounded = False
        key = pygame.key.get_pressed()
        if key[K_a] or key[K_LEFT]:
            self.direction = DIRECTION.left
            if self.rect.x <= 0: # Avoid disappearing on left side of screen
                self.hspeed = 0
            else:
                self.hspeed = -self.speed
        elif key[K_d] or key[K_RIGHT]:
            self.direction = DIRECTION.right
            self.hspeed = self.speed

        self.vspeed += self.gravity
        self.move(self.hspeed, self.vspeed)
        self.detect_data()

    def detect_data(self):
        for sprite in self.movingforce_group:
            if self.rect.colliderect(sprite.rect) and not self.has_data:
                self.has_data = True
                sprite.kill()

    def get_data_pos(self):
        hspeed = 5
        vspeed = -12
        if self.direction == DIRECTION.left:
            hspeed = -6
        x = self.rect.x + self.hspeed
        y = self.rect.top - 32 + self.vspeed
        return x, y, hspeed, vspeed

