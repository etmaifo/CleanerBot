from gamelib.physicsbody import PhysicsBody
from gamelib.constants import GAME, COLOR
import pygame, os
import pygame.mixer as mixer

class DataFragment(PhysicsBody):
    def __init__(self, x, y, width, height, image):
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.image.set_colorkey(COLOR.black)
        self.frameNumber = 0
        self.speed = 3
        self.timeout = 0
        self.captured = False
        self.safe = False
        self.givePoint = False
        self.id = 0
        self.killer_group = pygame.sprite.Group()
        self.storage_group = pygame.sprite.Group()

        self.dead_sound = mixer.Sound(os.path.join("assets", "sfx", "data_explode.wav"))
        self.point_sound = mixer.Sound(os.path.join("assets", "sfx", "sfx_zap.ogg"))
        self.dead_sound.set_volume(0.4)
        self.point_sound.set_volume(0.5)

    def update(self):
        self.check_bounds()
        if self.grounded: 
            self.animate_walk()
        if not self.captured:
            self.vspeed += self.gravity
            self.move(self.hspeed, self.vspeed)

    def animate_storage(self):
        self.timeout += 1
        if self.timeout >= GAME.fps:
            self.givePoint = True

    def animate_walk(self):
        pass   

    def animate_jump(self):
        self.image = pygame.transform.smoothscale(self.image, (self.rect.width/2, self.rect.height))
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def animate_bounce(self):
        self.image = pygame.transform.smoothscale(self.image, (self.rect.width, self.rect.height/2))
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def detect_collision(self, dx, dy):
        tempRect = pygame.Rect(self.rect)
        tempRect.x += dx
        tempRect.y += dy

        for sprite in self.killer_group:
            if tempRect.colliderect(sprite.rect):
                self.captured = True
                self.dead_sound.play()
                return

        for sprite in self.storage_group:
            if tempRect.colliderect(sprite.rect):
                self.playerId = sprite.playerId
                self.safe = True
                self.point_sound.play()

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