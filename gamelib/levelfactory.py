import pygame, os
import pytmx
from constants import SCREEN, ASSET, PARTICLE, GAME
from player import Player
from physicsbody import PhysicsBody
from datafragment import DataFragment
from enemy import Enemy
from particlefactory import Particle

class Level(object):
    def __init__(self, mapfile):
        self.players = []
        self.blocks = []
        self.datafragments = []
        self.enemies = []
        self.io_in = []
        self.io_out = []

        self.block_group = pygame.sprite.Group()
        self.datafragment_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.io_in_group = pygame.sprite.Group()
        self.io_out_group = pygame.sprite.Group()

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
                #self.player = Player(player.x, player.y, player.width, player.height, ASSET.player)
                self.player = Player(player.x, player.y, 50, 50, ASSET.player)
            elif layer.name.upper() == "BLOCKS":
                self.blocks = layer
            elif layer.name.upper() == "DATA":
                self.datafragments = layer
            elif layer.name.upper() == "ENEMIES":
                self.enemies = layer
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
            datafragment = DataFragment(dataorb.x, dataorb.y, dataorb.width, dataorb.height, ASSET.dataFragmentFrames)
            datafragment.collision_group = self.player.collision_group.copy()
            self.player.movingforce_group.add(datafragment)
            self.display_group.add(datafragment)
            self.datafragment_group.add(datafragment)
        for port in self.io_in:
            io_port = PhysicsBody(port.x, port.y, port.width, port.height, ASSET.ioInImage)
            self.io_in_group.add(io_port)
            self.display_group.add(io_port)
            self.fragmentSpawnPos = [port.x + port.width/2, port.y + port.height]
        for port in self.io_out:
            io_port = PhysicsBody(port.x, port.y, port.width, port.height, ASSET.ioOutImage)
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

        for fragment in self.datafragment_group:
            fragment.killer_group = self.enemy_group.copy()
            fragment.storage_group.add(self.io_out_group)
            fragment.collision_group.add(self.io_in_group)

        self.player.collision_group.add(self.io_out_group)
        self.display_group.add(self.player)


    def update(self):
        now = pygame.time.get_ticks()/1000.0
        self.elapsed = now - self.timer
        self.spawnTimer += 1
        if self.spawnTimer >= 5 * GAME.fps:
            self.spawn_data()
            self.spawnTimer = 0
        if self.intro:
            if self.elapsed > 2:
                self.intro = False
        else:
            for datafragment in self.datafragment_group:
                if datafragment.captured:
                    self.spawn_particles(datafragment.rect.centerx, datafragment.rect.centery, 10)
                    datafragment.kill()
                elif datafragment.safe:
                    datafragment.animate_storage()
                    datafragment.kill()
                    self.storedData += 1
                #elif datafragment.givePoint:

            self.display_group.update()
            self.particles.update()

    def spawn_particles(self, x, y, number):
        for i in xrange(number):
            particle = Particle(x, y, PARTICLE.width, PARTICLE.height, PARTICLE.image)
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