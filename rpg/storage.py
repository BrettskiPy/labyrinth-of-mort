import arcade


class Inventory(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x
        self.center_y = center_y
        self.offset_x = self.width 

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - (self.offset_x - 64)
        self.center_y = window_pos_y / 2 + 14


class Vault(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x
        self.center_y = center_y

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - (self.width - 123)
        self.center_y = window_pos_y / 2 + 10