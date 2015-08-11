from physicsbody import PhysicsBody

class Platform(PhysicsBody):
    def __init__(self, x, y, width, height, image):
        PhysicsBody.__init__(self, x, y, width, height, image)

    def update(self):
        self.move(self.hspeed, self.vspeed)
