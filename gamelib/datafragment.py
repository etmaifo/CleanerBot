from physicsbody import PhysicsBody
from constants import GAME
import pygame

class DataFragment(PhysicsBody):
    def __init__(self, x, y, width, height, animationFrames):
        self.animationFrames = animationFrames
        image = animationFrames.get_walk_frames()[0]
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.frameNumber = 0
        self.speed = 3
        self.timeout = 0
        self.captured = False
        self.safe = False
        self.givePoint = False
        self.id = 0
        self.killer_group = pygame.sprite.Group()
        self.storage_group = pygame.sprite.Group()

    def update(self):
        if self.grounded: 
            self.animate_walk()
        if self.captured:
            "print captured"
        else:
            self.vspeed += self.gravity
            self.move(self.hspeed, self.vspeed)


    def animate_storage(self):
        self.timeout += 1
        if self.timeout >= GAME.fps:
            self.givePoint = True

    def animate_walk(self):
        self.image = self.animationFrames.get_walk_frames()[self.frameNumber]


    def detect_collision(self, dx, dy):
        tempRect = pygame.Rect(self.rect)
        tempRect.x += dx
        tempRect.y += dy
        #self.grounded = False

        for sprite in self.killer_group:
            if tempRect.colliderect(sprite.rect):
                self.captured = True
                return

        for sprite in self.storage_group:
            if tempRect.colliderect(sprite.rect):
                self.playerId = sprite.playerId
                self.safe = True

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
                    if dy > 3:
                        self.vspeed = -(abs(self.vspeed)-3)
                    else:
                        self.rect.bottom = sprite.rect.top
                        self.rect.y += sprite.vspeed
                        self.vspeed = 0
                        self.grounded = True

                    if self.hspeed != 0:
                        if self.hspeed < 0:
                            self.hspeed += 0.125/2
                        else:
                            self.hspeed -= 0.125/2
                elif dy < 0:
                    self.rect.top = sprite.rect.bottom
                    self.vspeed = 5

                
                return
        self.rect = pygame.Rect(tempRect)