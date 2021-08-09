import pygame, os
#import pytmx
from pytmx import pytmx
from gamelib.constants import SCREEN, ASSET, PARTICLE, GAME, PLAYER
from gamelib.player import Player
from gamelib.physicsbody import PhysicsBody
from gamelib.datafragment import DataFragment
from gamelib.saw import Saw
from gamelib.particlefactory import Particle, Bubble
from random import choice, randrange
import pygame.mixer as mixer


class Level(object):
    def __init__(self, mapfile):
        mixer.init()
        
        self.players = []
        self.blocks = []
        self.datafragments = []
        self.enemies = []
        self.dataspawner = []
        self.portals = []
        self.saws = []
        self.bounds = []

        self.block_group = pygame.sprite.Group()
        self.datafragment_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.bubbles = pygame.sprite.Group()
        self.dataspawner_group = pygame.sprite.Group()
        self.portals_group = pygame.sprite.Group()
        self.saw_group = pygame.sprite.Group()
        self.bounds_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        self.display_group = pygame.sprite.OrderedUpdates()
        self.player_group = pygame.sprite.Group()

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
        
        self.datafragment_break_sound = mixer.Sound(os.path.join("assets", "sfx", "break.wav"))

    def load_map(self, filename):
        self.data = pytmx.TiledMap(filename)
        self.width = self.data.width * self.data.tilewidth
        self.height = self.data.height * self.data.tileheight

        for layer in self.data.layers:
            if layer.name.upper() == "PLAYER":
                p1 = layer[0]
                p2 = layer[1]
                self.player1 = Player(p1.x, p1.y, p1.width, p1.height, ASSET.player1, PLAYER.one)
                self.player2 = Player(p2.x, p2.y, p2.width, p2.height, ASSET.player2, PLAYER.two)                

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
            elif layer.name.upper() == "DATASPAWNER":
                self.dataspawner = layer
            elif layer.name.upper() == "PORTALS":
                self.portals = layer

    def create_level(self):
        blockImage = ASSET.blockImage

        for block in self.blocks:
            if block[2] != 0:
                levelBlock = PhysicsBody(0, 0, self.data.tilewidth, self.data.tileheight, blockImage)
                levelBlock.image = levelBlock.image.convert_alpha()
                levelBlock.rect.x = self.data.tilewidth * block[0]
                levelBlock.rect.y = self.data.tileheight * block[1]
                self.player1.collision_group.add(levelBlock)
                self.player2.collision_group.add(levelBlock)
                self.display_group.add(levelBlock)
                self.block_group.add(levelBlock)

        for dataorb in self.datafragments:
            self.fragmentWidth = dataorb.width
            self.fragmentHeight = dataorb.height

        for vport in self.dataspawner:
            io_port = PhysicsBody(vport.x, vport.y, vport.width, vport.height, ASSET.ioInImage)
            io_port.hspeed = 4
            self.dataspawner_group.add(io_port)
            self.display_group.add(io_port)
            self.fragmentSpawnPos = [vport.x + vport.width/2, vport.y + vport.height]

        for port in self.portals:
            portal_base = PhysicsBody(port.x, port.y, port.width, port.height, ASSET.portal_base, "left")
            if portal_base.rect.centerx < SCREEN.width/2:
                portal = PhysicsBody(0, 0, 60, 55, ASSET.p1_portal, "left")
            else:
                portal = PhysicsBody(0, 0, 60, 55, ASSET.p2_portal, "left")
            portal.rect.centerx = portal_base.rect.centerx
            portal.rect.bottom = portal_base.rect.top
            self.portals_group.add(portal_base)
            self.display_group.add(portal_base)
            self.display_group.add(portal)

        for bound in self.bounds:
            saw_bound = PhysicsBody(bound.x, bound.y, bound.width, bound.height, blockImage)
            self.bounds_group.add(saw_bound)

        for saw in self.saws:
            sawblade = Saw(saw.x, saw.y, saw.width, saw.height, ASSET.sawFrames)
            sawblade.bounds = self.bounds_group.copy()
            self.saw_group.add(sawblade)
            self.display_group.add(sawblade)
            tempgroup = self.display_group.copy()
            self.display_group.empty()
            self.display_group.add(sawblade)
            self.display_group.add(tempgroup)
            self.player1.danger_group.add(self.saw_group)
            self.player2.danger_group.add(self.saw_group)

        for fragment in self.datafragment_group:
            fragment.killer_group = self.enemy_group.copy()
            fragment.storage_group.add(self.portals_group)
            fragment.collision_group.add(self.dataspawner_group)
            fragment.killer_group.add(self.saw_group)

        self.player1.collision_group.add(self.portals_group)
        self.player2.collision_group.add(self.portals_group)
        self.player_group.add(self.player1)
        self.player_group.add(self.player1.label)
        self.player_group.add(self.player1.glow)
        self.player_group.add(self.player2)
        self.player_group.add(self.player2.label)
        self.player_group.add(self.player2.glow)

    def update(self):
        now = pygame.time.get_ticks()/1000.0
        self.elapsed = now - self.timer
        self.spawnTimer += 1
        self.bubbleTimer += 1

        if self.bubbleTimer >= GAME.fps/3:
            self.spawn_bubbles(self.portals_group, choice([1, 2, 3, 4]))
            self.bubbleTimer = 0
        if self.spawnTimer >= 1 * GAME.fps:
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

            if self.player1.dead:
                self.spawn_player_debris(self.player1.death_pos[0], self.player1.death_pos[1], ASSET.p1_debris, 20)
                self.player1.dead = False
            if self.player2.dead:
                self.spawn_player_debris(self.player2.death_pos[0], self.player2.death_pos[1], ASSET.p2_debris, 20)
                self.player2.dead = False
            if self.player1.reconstruct:
                x_pos = self.player1.respawn_position[0] + self.player1.rect.width/2
                y_pos = self.player1.respawn_position[1] + self.player1.rect.height/2
                self.restructure_player(x_pos, y_pos, ASSET.p1_debris, 20, self.player1.particle_group, self.player2.reconstruction_timer)
                self.player1.reconstruct = False
            if self.player2.reconstruct:
                x_pos = self.player2.respawn_position[0] + self.player2.rect.width/2
                y_pos = self.player2.respawn_position[1] + self.player2.rect.height/2
                self.restructure_player(x_pos, y_pos, ASSET.p2_debris, 20, self.player2.particle_group, self.player2.reconstruction_timer)
                self.player2.reconstruct = False

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
            self.player_group.update()
            self.particles.update()

    def spawn_particles(self, x, y, number):
        for i in range(number):
            size = choice([2, 4, 6, 8, 10])
            particle = Particle(x, y, size, size, ASSET.particle)
            particle.image = particle.image.convert()
            particle.multiplier = 3
            particle.frame = -64
            particle.fade = False
            self.particles.add(particle)
            #particle.collision_group = self.player1.collision_group.copy()
            particle.splash_group = self.player1.collision_group.copy()

    def spawn_player_debris(self, x, y, image, number):

        for i in range(number):
            size = choice([2, 4, 6, 8, 10])
            debris = Particle(x, y, size, size, image)
            debris.hspeed = choice([-5, -4, -3, -2, 2, 3, 4, 5])
            debris.vspeed = choice([-5, -4, -3, -2, 2, 3, 4, 5])
            debris.hspeed *= 1.5
            debris.vspeed *= 1.5
            debris.gravity = 0
            debris.fade = True
            debris.friction = 0.010 * 2
            self.particles.add(debris)

    def restructure_player(self, x, y, image, number, sprite_group, kill_time):
        for i in range(number):
            size = choice([2, 4, 6, 8, 10])
            debris = Particle(x, y, size, size, image)
            debris.hspeed = choice([-4, -3, -2, 2, 3, 4])
            debris.vspeed = choice([-4, -3, -2, 2, 3, 4])
            debris.gravity = 0
            debris.fade = False

            for i in range(int(GAME.fps/2)):
                debris.fade = False
                debris.update()
                debris.timeout = 0
            debris.multiplier = kill_time
            debris.hspeed = -debris.hspeed
            debris.vspeed = -debris.vspeed

            self.particles.add(debris)
            sprite_group.add(debris)

    def spawn_bubbles(self, portals, number):
        for portal in portals:
            if portal.rect.centerx < SCREEN.width/2:
                image = ASSET.p1_debris
            else:
                image = ASSET.p2_debris
            for i in range(number):
                size = choice([3, 4, 4, 6, 8])
                particle = Bubble(portal.rect.x, portal.rect.top, size, size, image)
                particle.portal_group.add(portals)
                self.bubbles.add(particle)
            self.display_group.add(self.bubbles)

    def spawn_data(self):
        speed = 0
        x = 0
        y = 0
        for spawner in self.dataspawner_group:
            x = spawner.rect.x + spawner.rect.width/2
            y = spawner.rect.y + spawner.rect.height
            speed = spawner.hspeed
        datafragment = DataFragment(x, y, self.fragmentWidth, self.fragmentHeight, ASSET.dataFragment)
        datafragment.hspeed = speed
        datafragment.collision_group = self.player1.collision_group.copy()
        datafragment.collision_group = self.player2.collision_group.copy()
        self.player1.movingforce_group.add(datafragment)
        self.player2.movingforce_group.add(datafragment)
        self.display_group.add(datafragment)
        self.datafragment_group.add(datafragment)

        datafragment.killer_group = self.enemy_group.copy()
        datafragment.storage_group.add(self.portals_group)
        datafragment.collision_group.add(self.dataspawner_group)
        datafragment.killer_group.add(self.saw_group)

    def shoot_data(self, x, y, hspeed, vspeed):
        datafragment = DataFragment(x, y, self.fragmentWidth, self.fragmentHeight, ASSET.dataFragment)
        datafragment.collision_group = self.player1.collision_group.copy()
        datafragment.collision_group = self.player2.collision_group.copy()
        self.player1.movingforce_group.add(datafragment)
        self.player2.movingforce_group.add(datafragment)
        self.display_group.add(datafragment)
        self.datafragment_group.add(datafragment)

        datafragment.killer_group = self.enemy_group.copy()
        datafragment.storage_group.add(self.portals_group)
        datafragment.collision_group.add(self.dataspawner_group)
        datafragment.killer_group.add(self.saw_group)

        datafragment.hspeed = hspeed        
        datafragment.vspeed = vspeed


class Stage(object):
    def __init__(self, level):
        self.levels = []
        self.levelIndex = 0

        self.load_files()
        try:
            self.level = self.levels[level-1]
        except:
            self.level = self.levels[0]
        self.number_of_levels = len(self.levels)

    def load_files(self):
        levels = os.listdir(os.path.join("assets", "levels"))
        for level in levels:
            self.levels.append(Level(os.path.join("assets", "levels", level)))

    def load_file(self, filename):
        level = Level(os.path.join("assets", "levels", filename))
        self.levels.append(level)

    def draw(self, screen):
        for entity in self.level.display_group:
            screen.blit(entity.image, entity.rect)
        for player in self.level.player_group:
            if not player.frozen:
                screen.blit(player.image, player.rect)
