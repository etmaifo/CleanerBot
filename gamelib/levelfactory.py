import pygame, os
import pytmx
from constants import SCREEN, ASSET, PARTICLE, GAME, PLAYER
from player import Player
from physicsbody import PhysicsBody
from datafragment import DataFragment
from saw import Saw
from particlefactory import Particle, LightParticle
from random import choice

class Level(object):
    def __init__(self, mapfile):
        self.players = []
        self.blocks = []
        self.datafragments = []
        self.enemies = []
        self.io_in = []
        self.portals = []
        self.saws = []
        self.bounds = []

        self.block_group = pygame.sprite.Group()
        self.datafragment_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.light_particles = pygame.sprite.Group()
        self.io_in_group = pygame.sprite.Group()
        self.portals_group = pygame.sprite.Group()
        self.saw_group = pygame.sprite.Group()
        self.bounds_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        self.display_group = pygame.sprite.OrderedUpdates()

        self.width = SCREEN.width
        self.height = SCREEN.height
        self.fragmentWidth = 0
        self.fragmentHeight = 0
        self.fragmentSpawnPos = []

        self.player1 = None
        self.player2 = None

        self.intro = False
        self.timer = 0
        self.p1_data = 0
        self.p2_data = 0
        self.elapsed = 0
        self.spawnTimer = 0
        self.bubbleTimer = 0        

        self.load_map(mapfile)
        self.create_level()

    def load_map(self, filename):
        self.data = pytmx.TiledMap(filename)
        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight

        for layer in self.data.layers:
            if layer.name.upper() == "PLAYER":
                p1 = layer[0]
                p2 = layer[1]
                self.player1 = Player(p1.x, p1.y, p1.width, p1.height, ASSET.player, PLAYER.one)
                self.player2 = Player(p2.x, p2.y, p2.width, p2.height, ASSET.player, PLAYER.two)
                self.player2.label.image = PLAYER.p2_label
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
            elif layer.name.upper() == "PORTALS":
                self.portals = layer

    def create_level(self):
        blockImage = ASSET.blockImage

        for block in self.blocks:
            if block[2] != 0:
                levelBlock = PhysicsBody(0, 0, self.data.tilewidth, self.data.tileheight, blockImage)
                levelBlock.rect.x = self.data.tilewidth * block[0]
                levelBlock.rect.y = self.data.tileheight * block[1]
                self.player1.collision_group.add(levelBlock)
                self.player2.collision_group.add(levelBlock)
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

        for port in self.portals:
            portal_base = PhysicsBody(port.x, port.y, port.width, port.height, ASSET.portal_base, "left")
            portal = PhysicsBody(0, 0, 60, 55, ASSET.portal, "left")
            portal.rect.centerx = portal_base.rect.centerx
            portal.rect.bottom = portal_base.rect.top
            self.portals_group.add(portal_base)
            self.display_group.add(portal_base)
            self.display_group.add(portal)

        for bound in self.bounds:
            sawBound = PhysicsBody(bound.x, bound.y, bound.width, bound.height, blockImage)
            self.bounds_group.add(sawBound)

        for saw in self.saws:
            sawblade = Saw(saw.x, saw.y, saw.width, saw.height, ASSET.sawFrames)
            sawblade.bounds = self.bounds_group.copy()
            self.saw_group.add(sawblade)
            self.display_group.add(sawblade)
            tempgroup = self.display_group.copy()
            self.display_group.empty()
            self.display_group.add(sawblade)
            self.display_group.add(tempgroup)

        for fragment in self.datafragment_group:
            fragment.killer_group = self.enemy_group.copy()
            fragment.storage_group.add(self.portals_group)
            fragment.collision_group.add(self.io_in_group)
            fragment.killer_group.add(self.saw_group)

        self.player1.collision_group.add(self.portals_group)
        self.player2.collision_group.add(self.portals_group)
        self.display_group.add(self.player1)
        self.display_group.add(self.player1.label)
        self.display_group.add(self.player2)
        self.display_group.add(self.player2.label)

    def update(self):
        now = pygame.time.get_ticks()/1000.0
        self.elapsed = now - self.timer
        self.spawnTimer += 1
        self.bubbleTimer += 1
        if self.bubbleTimer >= 1 * GAME.fps:
            self.spawn_light_particles(self.portals_group, choice([1, 2, 3, 4]))
            self.bubbleTimer = 0
        if self.spawnTimer >= 1.5 * GAME.fps:
            self.spawn_data()            
            self.spawnTimer = 0
        if self.intro:
            if self.elapsed > 2:
                self.intro = False
        else:
            if self.player1.shoot_data:
                self.player1.shoot_data = False
                self.player1.has_data = False
                shotx = self.player1.get_data_pos()[0] + (self.player1.rect.width / 2) - (self.fragmentWidth/2)
                shoty = self.player1.get_data_pos()[1]
                shotSpeed = self.player1.get_data_pos()[2]
                shotHeight = self.player1.get_data_pos()[3]
                self.shoot_data(shotx, shoty, shotSpeed, shotHeight)

            if self.player2.shoot_data:
                self.player2.shoot_data = False
                self.player2.has_data = False
                shotx = self.player2.get_data_pos()[0] + (self.player2.rect.width / 2) - (self.fragmentWidth/2)
                shoty = self.player2.get_data_pos()[1]
                shotSpeed = self.player2.get_data_pos()[2]
                shotHeight = self.player2.get_data_pos()[3]
                self.shoot_data(shotx, shoty, shotSpeed, shotHeight)

            for datafragment in self.datafragment_group:
                if datafragment.captured:
                    self.spawn_particles(datafragment.rect.centerx, datafragment.rect.centery, 10)
                    datafragment.kill()
                elif datafragment.safe:
                    datafragment.animate_storage()
                    if datafragment.playerId == "p1":
                        self.p1_data += 1
                    elif datafragment.playerId == "p2":
                        self.p2_data += 1
                    datafragment.kill()

            self.display_group.update()
            self.particles.update()

    def spawn_particles(self, x, y, number):
        for i in xrange(number):
            size = choice([2, 4, 6, 8, 10])
            # particle = Particle(x, y, PARTICLE.width, PARTICLE.height, PARTICLE.image)
            particle = Particle(x, y, size, size, PARTICLE.image)
            self.particles.add(particle)

    def spawn_light_particles(self, portals, number):
        for portal in portals:        
            for i in xrange(number):
                size = choice([2, 3, 4, 4, 6])
                particle = LightParticle(portal.rect.x, portal.rect.bottom, size, size, ASSET.light_particle)
                particle.portal_group.add(portals)
                self.light_particles.add(particle)
            self.display_group.add(self.light_particles)

    def spawn_data(self):
        datafragment = DataFragment(self.fragmentSpawnPos[0], self.fragmentSpawnPos[1], self.fragmentWidth, self.fragmentHeight, ASSET.dataFragmentFrames)
        datafragment.collision_group = self.player1.collision_group.copy()
        datafragment.collision_group = self.player2.collision_group.copy()
        self.player1.movingforce_group.add(datafragment)
        self.player2.movingforce_group.add(datafragment)
        self.display_group.add(datafragment)
        self.datafragment_group.add(datafragment)

        datafragment.killer_group = self.enemy_group.copy()
        datafragment.storage_group.add(self.portals_group)
        datafragment.collision_group.add(self.io_in_group)
        datafragment.killer_group.add(self.saw_group)


    def shoot_data(self, x, y, hspeed, vspeed):
        datafragment = DataFragment(x, y, self.fragmentWidth, self.fragmentHeight, ASSET.dataFragmentFrames)
        datafragment.collision_group = self.player1.collision_group.copy()
        datafragment.collision_group = self.player2.collision_group.copy()
        self.player1.movingforce_group.add(datafragment)
        self.player2.movingforce_group.add(datafragment)
        self.display_group.add(datafragment)
        self.datafragment_group.add(datafragment)

        datafragment.killer_group = self.enemy_group.copy()
        datafragment.storage_group.add(self.portals_group)
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