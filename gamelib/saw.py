import pygame
from gamelib.physicsbody import PhysicsBody
from random import choice
from gamelib.constants import GAME

class Saw(PhysicsBody):
    def __init__(self, x, y, width, height, frames):
        self.frames = frames
        image = frames[0]
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.bounds = pygame.sprite.Group()
        self.changeDirection = False
        self.angle = 0

        self.hspeed = choice([-3, -2, 2, 3])
        self.index = 0
        self.frame = 0

    def update(self):
        self.vspeed = 0
        self.move(self.hspeed, self.vspeed)
        self.animate()
        self.rest(3)

    def detect_collision(self, dx, dy):
        tempRect = pygame.Rect(self.rect)
        tempRect.x += dx
        tempRect.y += dy

        for sprite in self.bounds:
            if tempRect.colliderect(sprite.rect):
                # Check x-axis
                if dx > 0:
                    self.rect.right = sprite.rect.left
                elif dx < 0:
                    self.rect.left = sprite.rect.right
                self.hspeed = -dx

                return
        self.rect = pygame.Rect(tempRect)

    def animate(self):
        self.index += 1
        if self.index >= 1:
            self.index = 0
            self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0
        self.image = self.frames[self.frame]


    def rest(self, duration):
        count = 0
        for i in range(GAME.fps * duration, -1, -1):
            if count >= i:
                self.changeDirection = False


