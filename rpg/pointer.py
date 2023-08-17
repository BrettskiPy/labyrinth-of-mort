import arcade


class Pointer(arcade.Sprite):
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)
        hitbox_points = [
            (-5, 7),  # Top-left
            (1, 0),  # Top-right
            (4, 0),  # Bottom-right
            (-5, 0),  # Bottom-left
        ]
        self.set_hit_box(hitbox_points)

    def update(self, pos_x, pos_y):
        self.center_x = pos_x
        self.center_y = pos_y
