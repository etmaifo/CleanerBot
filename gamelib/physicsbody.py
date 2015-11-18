import pygame
from constants import WORLD, DIRECTION, SCREEN


class PhysicsBody(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, direction="right", playerId="p1"):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.smoothscale(image, (width, height)).convert_alpha()
        self.playerId = playerId
        if direction == DIRECTION.left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vspeed = 0
        self.hspeed = 0
        self.gravity = WORLD.gravity
        self.speed = 0
        self.grounded = True

        self.collision_group = pygame.sprite.Group()
        self.movingforce_group = pygame.sprite.Group()
        self.assign_player()

    def assign_player(self):
        if self.rect.x > (SCREEN.width / 2):
            self.playerId = "p2"

    def handle_events(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        if dx != 0:
            self.detect_collision(dx, 0)
        if dy != 0:
            self.detect_collision(0, dy)

    def check_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.hspeed = -self.hspeed
        elif self.rect.right > SCREEN.width:
            self.rect.right = SCREEN.width
            self.hspeed = -self.hspeed

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
                elif dx < 0 and sprite.vspeed == 0:
                    self.rect.left = sprite.rect.right

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
