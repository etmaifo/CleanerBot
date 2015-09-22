import pygame

class Asset(object):
    def __init__(self, spriteSheet, spriteMap):
        self.spriteSheet = spriteSheet
        self.textFile = spriteMap
        self.sprites = []

    def load_sprites(self):
        info = open(self.textFile, 'r')
        lines = []
        for line in info:
            lines.append(line.split())
        for line in lines:
            sprite = self.get_image(int(line[2]), int(line[3]), int(line[4]), int(line[5])) # 0 0 0 0
            self.sprites.append([line[0], sprite])

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spriteSheet, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))

        return image


class ObjectAsset(Asset):
    def __init__(self, spriteSheet, spriteMap):
        Asset.__init__(self, spriteSheet, spriteMap)
        self.load_sprites()

    def get_walk_frames(self):
        walkFrames = [frame[1] for frame in self.sprites if "walk" in frame[0]]
        return walkFrames

    def get_idle_frames(self):
        idleFrames = [frame[1] for frame in self.sprites if "idle" in frame[0]]
        return idleFrames

    def get_jump_frames(self):
        jumpFrames = [frame[1] for frame in self.sprites if "jump" in frame[0]]
        return jumpFrames

    def get_hurt_frames(self):
        hurtFrames = [frame[1] for frame in self.sprites if "hurt" in frame[0]]
        return hurtFrames

    def get_burn_frames(self):
        burnFrames = [frame[1] for frame in self.sprites if "burn" in frame[0]]
        return burnFrames

    def get_fall_frames(self):
        fallFrames = [frame[1] for frame in self.sprites if "fall" in frame[0]]
        return fallFrames

    def get_spin_frames(self):
        spinFrames = [frame[1] for frame in self.sprites if "spin" in frame[0]]
        return spinFrames

class BeamAsset(ObjectAsset):
    def __init__(self, spriteSheet, spriteMap):
        ObjectAsset.__init__(self, spriteSheet, spriteMap)

    def get_base_frames(self):
        frames = [frame[1] for frame in self.sprites if "base" in frame[0]]
        return frames

    def get_beam_frames(self):
        frames = [frame[1] for frame in self.sprites if "ray" in frame[0]]
        return frames