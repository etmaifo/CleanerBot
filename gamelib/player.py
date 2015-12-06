import pygame
from pygame.locals import *
from physicsbody import PhysicsBody
from constants import DIRECTION, PLAYER, ASSET

class Player(PhysicsBody):
    def __init__(self, x, y , width, height, animationFrames, id):
        #image = animationFrames.get_walk_frames()[0]
        image = animationFrames
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.jumpHeight = PLAYER.jump
        self.speed = PLAYER.speed
        self.has_data = False
        self.shoot_data = False
        self.direction = DIRECTION.left
        self.id = id
        self.invulnerable = False
        self.label = PhysicsBody(0, 0, 17, 12, PLAYER.p1_label)
        self.glow = PhysicsBody(0, 0, 64, 64, ASSET.player1_glow)
        self.original_image = self.image
        self.update_label()
        self.update_effects()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.label.image, self.label.rect)
        screen.blit(self.glow, self.glow.rect)

    def handle_events(self, event):
        if event.type == JOYAXISMOTION:
            print "Detected joystick"
        if self.id == PLAYER.one:
            if event.type == KEYDOWN:
                if (event.key == K_o or event.key == K_SPACE) and self.grounded:
                    self.vspeed = self.jumpHeight
            if event.type == KEYUP:
                if event.key == K_a or event.key == K_d:
                    self.hspeed = 0
                if event.key == K_i:
                    if self.has_data:
                        self.shoot_data = True
        if self.id == PLAYER.two:
            if event.type == KEYDOWN:
                if event.key == K_UP and self.grounded:
                    self.vspeed = self.jumpHeight
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    self.hspeed = 0
                if event.key == K_m:
                    if self.has_data:
                        self.shoot_data = True
    
    def animate_size(self):
        if self.has_data:
            self.grow()
        else:
            self.shrink()

    def update_label(self):
        self.label.rect.centerx = self.rect.centerx
        self.label.rect.bottom = self.rect.top - 5
        
    def update_effects(self):
        self.glow.rect.center = self.rect.center

    def update(self):
        self.animate_size()
        self.check_bounds()
        self.grounded = False
        key = pygame.key.get_pressed()
        if self.id == PLAYER.one:
            if key[K_a]:
                self.direction = DIRECTION.left
                if self.rect.x <= 0: # Avoid disappearing on left side of screen
                    self.hspeed = 0
                else:
                    self.hspeed = -self.speed
            elif key[K_d]:
                self.direction = DIRECTION.right
                self.hspeed = self.speed
        elif self.id == PLAYER.two:
            if key[K_LEFT]:
                self.direction = DIRECTION.left
                if self.rect.x <= 0: # Avoid disappearing on left side of screen
                    self.hspeed = 0
                else:
                    self.hspeed = -self.speed
            elif key[K_RIGHT]:
                self.direction = DIRECTION.right
                self.hspeed = self.speed

        self.vspeed += self.gravity
        self.move(self.hspeed, self.vspeed)
        self.detect_data()
        self.update_label()
        self.update_effects()

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

    def grow(self):
        centerx = self.rect.centerx
        bottom = self.rect.bottom
        self.image = pygame.transform.smoothscale(self.original_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.jumpHeight = PLAYER.jump + 2

    def shrink(self):
        centerx = self.rect.centerx
        bottom = self.rect.bottom
        self.image = pygame.transform.smoothscale(self.original_image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.jumpHeight = PLAYER.jump

