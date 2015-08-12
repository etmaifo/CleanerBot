from physicsbody import PhysicsBody

class Enemy(PhysicsBody):
    def __init__(self, x, y, width, height, animationFrames):
        image = animationFrames.get_walk_frames()[0]
        PhysicsBody.__init__(self, x, y, width, height, image)
        self.speed = 3

    def update(self):
        self.hunt()
        self.vspeed += self.gravity
        self.move(self.hspeed, self.vspeed)

    def hunt(self):
        pass
