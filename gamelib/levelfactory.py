import pygame, os
import pytmx
from constants import SCREEN, ASSET, PARTICLE, GAME
from player import Player
from physicsbody import PhysicsBody
from datafragment import DataFragment
from enemy import Enemy
from saw import Saw
from particlefactory import Particle
from random import choice

class Level(object):
    def __init__(self, mapfile):
        self.players = []
        self.blocks = []
        self.datafragments = []
        self.enemies = []
        self.io_in = []
        self.io_out = []
        self.saws = []
        self.bounds = []

        self.block_group = pygame.sprite.Group()
        self.datafragment_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.io_in_group = pygame.sprite.Group()
        self.io_out_group = pygame.sprite.Group()
        self.saw_group = pygame.sprite.Group()
        self.bounds_group = pygame.sprite.Group()

        self.width = SCREEN.width
        self.height = SCREEN.height
        self.fragmentWidth = 0
        self.fragmentHeight = 0
        self.fragmentSpawnPos = []

        self.player = None

        self.intro = False
        self.timer = 0
        self.storedData = 0
        self.elapsed = 0
        self.spawnTimer = 0
        self.display_group = pygame.sprite.OrderedUpdates()

        self.load_map(mapfile)
        self.create_level()

    def load_map(self, filename):
        self.data = pytmx.TiledMap(filename)
        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight

        for layer in self.data.layers:
            if layer.name.upper() == "PLAYER":
                player = layer[0]
                self.player = Player(player.x, player.y, player.width, player.height, ASSET.player)
            elif layer.name.upper() == "BLOCKS":
                self.blocks = layer
            elif layer.name.upper() == "DATA":
                self.datafragments = layer
            elif layer.name.upper() == "ENEMIES":
                self.enemies = layer
            elif layer.name.upper() == "SAWS":
                self.saws = layer
            elif layer.name.upper() == "SAW_BOUNDS":
                self.bounds = layer
            elif layer.name.upper() == "IO_IN":
                self.io_in = layer
            elif layer.name.upper() == "IO_OUT":
                self.io_out = layer

    def create_level(self):
        blockImage = ASSET.blockImage

        for block in self.blocks:
            if block[2] != 0:
                levelBlock = PhysicsBody(0, 0, self.data.tilewidth, self.data.tileheight, blockImage)
                levelBlock.rect.x = self.data.tilewidth * block[0]
                levelBlock.rect.y = self.data.tileheight * block[1]
                self.player.collision_group.add(levelBlock)
                self.display_group.add(levelBlock)
                self.block_group.add(levelBlock)

        for dataorb in self.datafragments:
            self.fragmentWidth = dataorb.width
            self.fragmentHeight = dataorb.height

        for vport in self.io_in:
            io_port = PhysicsBody(vport.x, vport.y, vport.width, vport.height, ASSET.ioInImage)
            self.io_in_group.add(io_port)
            self.display_group.add(io_port)
            self.fragmentSpawnPos = [vport.x + vport.width/2, vport.y + vport.height]

        for port in self.io_out:
            io_port = PhysicsBody(port.x, port.y, port.width, port.height, ASSET.ioOutImage, port.properties['direction'])
            self.io_out_group.add(io_port)
            self.display_group.add(io_port)

        for enemy_ in self.enemies:
            enemy = Enemy(enemy_.x, enemy_.y, enemy_.width, enemy_.height, ASSET.enemyFrames)
            enemy.collision_group = self.block_group.copy()
            enemy.collision_group.add(self.io_out_group)
            self.player.collision_group.add(enemy)
            for item in self.player.movingforce_group:
                item.collision_group.add(enemy)
            self.enemy_group.add(enemy)
            self.display_group.add(enemy)

        for bound in self.bounds:
            sawBound = PhysicsBody(bound.x, bound.y, bound.width, bound.height, blockImage)
            self.bounds_group.add(sawBound)

        for saw in self.saws:
            sawblade = Saw(saw.x, saw.y, saw.width, saw.height, ASSET.sawFrames)
            sawblade.bounds = self.bounds_group.copy()
            self.saw_group.add(sawblade)
            self.display_group.add(sawblade)

        for fragment in self.datafragment_group:
            fragment.killer_group = self.enemy_group.copy()
            fragment.storage_group.add(self.io_out_group)
            fragment.collision_group.add(self.io_in_group)
            fragment.killer_group.add(self.saw_group)

        self.player.collision_group.add(self.io_out_group)
        self.display_group.add(self.player)


    def update(self):
        now = pygame.time.get_ticks()/1000.0
        self.elapsed = now - self.timer
        self.spawnTimer += 1
        if self.spawnTimer >= 3 * GAME.fps:
            self.spawn_data()
            self.spawnTimer = 0
        if self.intro:
            if self.elapsed > 2:
                self.intro = False
        else:
            if self.player.shoot_data:
                self.player.shoot_data = False
                self.player.has_data = False
                shotx = self.player.get_data_pos()[0] + (self.player.rect.width / 2) - (self.fragmentWidth/2)
                shoty = self.player.get_data_pos()[1]
                shotSpeed = self.player.get_data_pos()[2]
                shotHeight = self.player.get_data_pos()[3]
                self.shoot_data(shotx, shoty, shotSpeed, shotHeight)
            for datafragment in self.datafragment_group:
                if datafragment.captured:
                    self.spawn_particles(datafragment.rect.centerx, datafragment.rect.centery, 10)
                    datafragment.kill()
                elif datafragment.safe:
                    datafragment.animate_storage()
                    datafragment.kill()
                    self.storedData += 1

            self.display_group.update()
            self.particles.update()

    def spawn_particles(self, x, y, number):
        for i in xrange(number):
            size = choice([2, 4, 6, 8, 10])
            #particle = Particle(x, y, PARTICLE.width, PARTICLE.height, PARTICLE.image)
            particle = Particle(x, y, size, size, PARTICLE.image)
            self.particles.add(particle)

    def spawn_data(self):
        datafragment = DataFragment(self.fragmentSpawnPos[0], self.fragmentSpawnPos[1], self.fragmentWidth, self.fragmentHeight, ASSET.dataFragmentFrames)
        datafragment.collision_group = self.player.collision_group.copy()
        self.player.movingforce_group.add(datafragment)
        self.display_group.add(datafragment)
        self.datafragment_group.add(datafragment)

        datafragment.killer_group = self.enemy_group.copy()
        datafragment.storage_group.add(self.io_out_group)
        datafragment.collision_group.add(self.io_in_group)
        datafragment.killer_group.add(self.saw_group)


    def shoot_data(self, x, y, hspeed, vspeed):
        datafragment = DataFragment(x, y, self.fragmentWidth, self.fragmentHeight, ASSET.dataFragmentFrames)
        datafragment.collision_group = self.player.collision_group.copy()
        self.player.movingforce_group.add(datafragment)
        self.display_group.add(datafragment)
        self.datafragment_group.add(datafragment)

        datafragment.killer_group = self.enemy_group.copy()
        datafragment.storage_group.add(self.io_out_group)
        datafragment.collision_group.add(self.io_in_group)
        datafragment.killer_group.add(self.saw_group)

        datafragment.hspeed = hspeed        
        datafragment.vspeed = vspeed


class Stage(object):
    def __init__(self):
        self.levels = []
        self.levelIndex = 0

        self.load_files()
        self.level = self.levels[0]

    def load_files(self):
        levels = os.listdir(os.path.join("assets", "levels"))
        for level in levels:
            self.levels.append(Level(os.path.join("assets", "levels", level)))

    def load_file(self, filename):
        level = Level(os.path.join("assets", "levels", filename))
        self.levels.append(level)

    def get_next(self):
        if self.levelIndex >= len(self.levels):
            self.levelIndex = 0

        i = self.levelIndex + 1
        self.levelIndex += 1
        return self.levels[i]

    def load_next(self):
        self.levelIndex += 1
        if self.levelIndex >= len(self.levels):
            self.levelIndex = 0
        i = self.levelIndex
        self.level = self.levels[i]
        self.level.timer = pygame.time.get_ticks()/1000.0

    def reload_level(self):
        number = self.levelIndex
        if number < 10:
            number = "0" + str(self.levelIndex + 1)
        number = str(number)
        self.level = self.levels[self.levelIndex - 1]

    def update(self):
        pass