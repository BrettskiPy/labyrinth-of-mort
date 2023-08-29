import arcade

X_OFFSET = 249
Y_OFFSET = 10


class Dungeon(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x - X_OFFSET
        self.center_y = center_y / 2 + Y_OFFSET

    def draw(self):
        super().draw()

    def update(self, window_width, window_height):
        new_center_x = window_width - X_OFFSET
        new_center_y = window_height / 2 + Y_OFFSET

        delta_x = new_center_x - self.center_x
        delta_y = new_center_y - self.center_y

        if delta_x != 0 or delta_y != 0:
            self.center_x = new_center_x
            self.center_y = new_center_y
