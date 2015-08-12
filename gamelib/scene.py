
from player import Player

class Scene(object):
    def __init__(self, levelFile):
        self.player = Player()
        self.bounds = self.create_bounds(levelFile)

    def update(self):
        self.player.update()

    def draw(self, screen):
        screen.blit(self.player.image, self.player.pos)

    def create_bounds(self, filename):
        pass