import pygame
from gamelib.physicsbody import PhysicsBody
from gamelib.constants import WORLD
from random import choice

class Enemy(PhysicsBody):
    def __init__(self, x, y, width, height, frames):
        image = frames.get_walk_frames()[0]
        PhysicsBody.__init__(self, x, y, width, height, image)

        self.hspeed = choice([-1, 1])

    def update(self):
        self.vspeed += WORLD.gravity
        self.move(self.hspeed, self.vspeed)

    def detect_collision(self, dx, dy):
        tempRect = pygame.Rect(self.rect)
        tempRect.x += dx
        tempRect.y += dy

        for sprite in self.collision_group:
            if tempRect.colliderect(sprite.rect):
                # Check x-axis
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
                    self.grounded = True
                elif dy < 0:
                    self.rect.top = sprite.rect.bottom
                    self.vspeed = 0
                return
        self.rect = pygame.Rect(tempRect)


