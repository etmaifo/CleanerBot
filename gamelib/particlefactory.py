from random import randrange, choice, uniform
from physicsbody import PhysicsBody
from constants import GAME
import pygame

class Particle(PhysicsBody):
    def __init__(self, x, y, width, height, image):
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.image = pygame.transform.smoothscale(image, (width, height)).convert()
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timeout = 0
        self.frame = 0
        self.fade = False

        self.vspeed = uniform(-12, -1)
        self.hspeed = randrange(-3, 4, 1)
        self.gravity = 0.5

    def update(self):
        self.timeout += 1
        if self.timeout >= 2 * GAME.fps:
            self.kill()
        
        self.vspeed += self.gravity

        if self.hspeed < 0:
            self.hspeed += self.friction
        elif self.hspeed > 0:
            self.hspeed -= self.friction
        if self.vspeed < 0:
            self.vspeed += self.friction
        else:
            self.vspeed -= self.friction

        self.move(self.hspeed, int(self.vspeed))
        if self.fade:
            self.animate_fade()

    def animate_fade(self):
        self.frame += 1
        if self.frame < GAME.fps * 2:
            self.image.set_alpha(254 - self.frame * 2)
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


class Bubble(Particle):
    def __init__(self, x, bottom, width, height, image):
        Particle.__init__(self, x, bottom, width, height, image)
        self.image = self.image.convert()
        self.rect.bottom = bottom
        x+=8
        self.rect.x = choice([x, x+8, x+16, x+32])
        self.vspeed = uniform(-2, 0)
        self.initial_pos = bottom
        self.portal_group = pygame.sprite.Group()
        self.frame = 0

    def update(self):
        self.rect.y += self.vspeed
        self.animate()
        if self.rect.width > 1:
            if self.frame in [1, 15, 30, 60]:
                self.animate_size()
        if self.initial_pos - self.rect.y > 60:
            self.kill()

    def animate(self):
        self.frame += 1
        alpha = 240 - self.frame * 8
        if alpha < 0:
            alpha = 0
        if self.frame < 60:
            self.image.set_alpha(alpha)
        else:
            self.frame = 0

    def animate_size(self):
        x, y, width, height = self.rect
        self.image = pygame.transform.smoothscale(self.image, (width-1, height-1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y