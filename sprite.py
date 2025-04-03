class Sprite:

    def __init__(self, sprite, speed_x=0, speed_y=0):
        self.sprite = sprite
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self):
        self.sprite.draw()