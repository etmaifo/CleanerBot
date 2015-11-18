from random import randrange, choice
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
        self.frame = 0

        self.vspeed = randrange(-13, -3)
        self.hspeed = randrange(-3, 4, 1)

    def update(self):
        self.timeout += 1
        if self.timeout >= 2 * GAME.fps:
            self.kill()
        
        self.vspeed += 0.5 #WORLD.gravity
        self.move(self.hspeed, self.vspeed)
        #self.rect.x += self.hspeed
        #self.rect.y += self.vspeed
        self.animate_fade()

    def animate_fade(self):
        self.frame += 1
        if self.frame < 60:
            self.image.set_alpha(120 - self.frame * 2)
        else:
            self.frame = 0

    def detect_collision(self, dx, dy):
        tempRect = pygame.Rect(self.rect)
        tempRect.x += dx
        tempRect.y += dy

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
                elif dy < 0:
                    self.rect.top = sprite.rect.bottom
                    self.vspeed = 5
                return
        self.rect = pygame.Rect(tempRect)


class LightParticle(Particle):
    def __init__(self, x, y, width, height, image):
        Particle.__init__(self, x, y, width, height, image)
        self.vspeed = 0
        self.hspeed = 0


    def update(self):
        self.vspeed = choice[-1, -2]
        self.rect.y += self.vspeed
        self.move(self.hspeed, self.vspeed)

    def detect_collision(self, dx, dy):
        tempRect = pygame.Rect(self.rect)
        tempRect.x += dx
        tempRect.y += dy

        for sprite in self.collision_group:
            if tempRect.colliderect(sprite.rect):
                return
            self.kill()