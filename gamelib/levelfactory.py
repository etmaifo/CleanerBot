import pygame, os
import pytmx
from constants import SCREEN, ASSET
from player import Player
from physicsbody import PhysicsBody

class Level(object):
    def __init__(self, mapfile):
        self.players = []
        self.blocks = []
        self.width = SCREEN.width
        self.height = SCREEN.height

        self.player = Player(0, 0, 32, 32, ASSET.player) # default

        self.intro = False
        self.timer = 0
        self.elapsed = 0
        self.entities = pygame.sprite.OrderedUpdates()

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

    def create_level(self):
        blockImage = ASSET.blockImage
        for block in self.blocks:
            if block[2] != 0:
                levelBlock = PhysicsBody(0, 0, self.data.tilewidth, self.data.tileheight, blockImage)
                levelBlock.rect.x = self.data.tilewidth * block[0]
                levelBlock.rect.y = self.data.tileheight * block[1]
                self.player.collision_group.add(levelBlock)
                self.entities.add(levelBlock)
        self.entities.add(self.player)

    def update(self):
        now = pygame.time.get_ticks()/1000.0
        self.elapsed = now - self.timer
        if self.intro:
            if self.elapsed > 2:
                self.intro = False
        else:
            self.entities.update()

class Stage(object):
    def __init__(self):
        self.levels = []
        self.levelIndex = 0

        self.load_files()
        self.level = self.levels[0]

    def load_files(self):
        levels = os.listdir(os.path.join("assets", "levels"))
        print levels
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