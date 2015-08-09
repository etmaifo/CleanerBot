
from player import Player

class Scene(object):
    def __init__(self):
        self.player = Player()

    def update(self):
        self.player.update()

    def draw(self, screen):
        screen.blit(self.player.image, self.player.pos)