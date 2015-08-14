from physicsbody import PhysicsBody
from random import choice, randrange
import pygame

class Enemy(PhysicsBody):
    def __init__(self, x, y, width, height, animationFrames):
        image = animationFrames.get_walk_frames()[0]
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.speed = 3

    def update(self):
        if self.grounded and not self.grounded:
            self.hunt()
        self.vspeed += self.gravity
        self.move(self.hspeed, self.vspeed)

    def hunt(self):
        self.hspeed = choice([0, 1, 0, 2])

    def detect_collision(self, dx, dy):
        tempRect = pygame.Rect(self.rect)
        tempRect.x += dx
        tempRect.y += dy
        #self.grounded = False

        for sprite in self.collision_group:
            if tempRect.colliderect(sprite.rect):
                # Check x-axis
                self.rect.x += sprite.hspeed
                if dx > 0 and sprite.vspeed == 0:
                    self.rect.right = sprite.rect.left
                    self.hspeed = -dx
                elif dx < 0 and sprite.vspeed == 0:
                    self.rect.left = sprite.rect.right
                    self.hspeed = -dx

                # Check y axis
                if dy > 0:
                    self.rect.bottom = sprite.rect.top
                    self.rect.y += sprite.vspeed
                    self.vspeed = 0
                    self.vspeed = choice([randrange(-20, 0, 1)])
                    self.grounded = True
                elif dy < 0:
                    self.rect.top = sprite.rect.bottom
                    self.vspeed = 0
                    self.vspeed = 5
                return
        self.rect = pygame.Rect(tempRect)
