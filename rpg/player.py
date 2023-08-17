import arcade


class Player(arcade.Sprite):
    def __init__(self, filename, scale=2):
        super().__init__(filename, scale)

        self.center_x = 100
        self.center_y = 100
