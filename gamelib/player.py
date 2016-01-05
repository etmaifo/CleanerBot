import pygame
from pygame.locals import *
from physicsbody import PhysicsBody
from constants import DIRECTION, PLAYER, ASSET, GAME
from particlefactory import Particle
from random import choice

class Player(PhysicsBody):
    def __init__(self, x, y , width, height, animationFrames, id):
        image = animationFrames
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.jumpHeight = PLAYER.jump
        self.speed = PLAYER.speed
        self.has_data = False
        self.shoot_data = False
        self.direction = DIRECTION.left
        self.id = id
        self.invulnerable = False
        self.hurt = False
        self.dead = False
        self.cooldown = 0
        self.show = True
        self.frozen = False
        self.respawn = False
        self.reconstruct = False
        self.reconstruction_timer = 2.5
        self.blink_timer = 0
        self.label = PhysicsBody(0, 0, 17, 12, PLAYER.p1_label)
        self.glow = PhysicsBody(0, 0, 48, 48, ASSET.player1_glow)
        self.blink = PhysicsBody(0, 0, 32, 32, ASSET.player_hurt)
        self.original_image = self.image
        self.danger_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        
        self.sort_players()
        self.update_label()
        self.original_glow_image = self.glow.image
        self.original_blink_image = self.blink.image
        self.respawn_position = x, y
        self.death_pos = self.rect.centerx, self.rect.centery

        self.controller1 = self.get_controller(1)
        self.controller2 = self.get_controller(2)

    def handle_events(self, event):
        if not self.frozen:
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

                if event.type == JOYBUTTONDOWN:
                    if (self.controller1.get_button(1) == 1) and self.grounded:
                        self.vspeed = self.jumpHeight
                    if self.controller1.get_button(2) == 1:
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

                if event.type == JOYBUTTONDOWN and self.controller2 is not None:
                    if (self.controller2.get_button(1) == 1) and self.grounded:
                        self.vspeed = self.jumpHeight
                    if self.controller2.get_button(2) == 1:
                        if self.has_data:
                            self.shoot_data = True

    def update(self):
        self.detect_reconstruction()
        self.animate_size()
        self.check_bounds()
        self.check_danger()
        self.grounded = False

        if not self.frozen:
            self.get_movement()
            self.vspeed += self.gravity
            self.move(self.hspeed, self.vspeed)

        self.detect_data()
        self.update_label()
        self.update_effects()

    def get_controller(self, player):
        number_of_joysticks = pygame.joystick.get_count()
        if number_of_joysticks == 1:
            if player == 1:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                return joystick
            else:
                return None
        elif number_of_joysticks > 1:
            if player == 1:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                return joystick
            if player == 2:
                joystick = pygame.joystick.Joystick(1)
                joystick.init()
                return joystick
        return None

    def animate_size(self):
        if self.has_data:
            self.grow()
        else:
            self.shrink()

    def update_label(self):
        self.label.rect.centerx = self.rect.centerx
        self.label.rect.bottom = self.rect.top - 5

    def animate_blink(self):
        if self.respawn:
            self.rect.x = self.respawn_position[0]
            self.rect.y = self.respawn_position[1]
            self.respawn = False
            self.dead = True
        self.shrink()
        self.blink_timer += 1
        if self.blink_timer < GAME.fps/8:
            self.image = ASSET.player_hurt
            self.original_glow_image = ASSET.player_hurt_glow
        elif self.blink_timer < GAME.fps/4:
            self.image = self.original_image
            if self.id == PLAYER.one:
                self.original_glow_image = ASSET.player1_glow
            else:
                self.original_glow_image = ASSET.player2_glow
        else:
            self.blink_timer = 0

    def update_effects(self):
        self.glow.rect.center = self.rect.center

        if self.hurt:
            self.animate_blink()
            self.cooldown += 1
            if self.cooldown == GAME.fps and not self.reconstruct:
                self.reconstruct = True
            if self.cooldown > 2.5 * GAME.fps:
                self.frozen = False
                self.label.frozen = False
                self.glow.frozen = False
            if self.cooldown > 4 * GAME.fps:
                self.cooldown = 0
                self.hurt = False
            elif self.cooldown == 1:
                self.respawn = True
                self.frozen = True
                self.label.frozen = True
                self.glow.frozen = True
        else:
            self.reset_images()
        
    def sort_players(self):
        if self.id == PLAYER.two:
            self.glow = PhysicsBody(0, 0, 48, 48, ASSET.player2_glow)
            self.label = PhysicsBody(0, 0, 17, 12, PLAYER.p2_label)
        self.glow.rect.center = self.rect.center

    def get_movement(self):
        key = pygame.key.get_pressed()

        if self.id == PLAYER.one:
            if key[K_a] or (self.controller1 is not None and self.controller1.get_hat(0)[0] == -1):
                self.direction = DIRECTION.left
                if self.rect.x <= 0:
                    self.hspeed = 0
                else:
                    self.hspeed = -self.speed
            elif key[K_d] or (self.controller1 is not None and self.controller1.get_hat(0)[0] == 1):
                self.direction = DIRECTION.right
                self.hspeed = self.speed
            if self.controller1 is not None and self.controller1.get_hat(0)[0] == 0:
                self.hspeed = 0

        elif self.id == PLAYER.two:
            if key[K_LEFT] or (self.controller2 is not None and self.controller2.get_hat(0)[0] == -1):
                self.direction = DIRECTION.left
                if self.rect.x <= 0: # Avoid disappearing on left side of screen
                    self.hspeed = 0
                else:
                    self.hspeed = -self.speed
            elif key[K_RIGHT] or (self.controller2 is not None and self.controller2.get_hat(0)[0] == 1):
                self.direction = DIRECTION.right
                self.hspeed = self.speed
            if self.controller2 is not None and self.controller2.get_hat(0)[0] == 0:
                self.hspeed = 0

    def detect_data(self):
        for sprite in self.movingforce_group:
            if self.rect.colliderect(sprite.rect) and not self.has_data and not self.frozen:
                self.has_data = True
                sprite.kill()

    def detect_reconstruction(self):
        for sprite in self.particle_group:
            if self.rect.colliderect(sprite.rect):
                for particle in self.particle_group:
                    particle.kill()
                self.particle_group.empty()
                self.frozen = False
                return

    def check_danger(self):
        for sprite in self.danger_group:
            if self.rect.colliderect(sprite.rect):
                self.hurt = True
                self.has_data = False
                self.death_pos = self.rect.centerx, self.rect.centery

    def get_data_pos(self):
        hspeed = 6
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
        
        self.glow.image = pygame.transform.smoothscale(self.original_glow_image, (64, 64))
        self.glow.rect = self.glow.image.get_rect()
        self.glow.rect.center = self.rect.center

    def shrink(self):
        centerx = self.rect.centerx
        bottom = self.rect.bottom
        self.image = pygame.transform.smoothscale(self.original_image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.jumpHeight = PLAYER.jump
        
        self.glow.image = pygame.transform.smoothscale(self.original_glow_image, (48, 48))
        self.glow.rect = self.glow.image.get_rect()
        self.glow.rect.center = self.rect.center

    def reset_images(self):
        if self.id == PLAYER.one:
            self.original_glow_image = ASSET.player1_glow
        else:
            self.original_glow_image = ASSET.player2_glow

