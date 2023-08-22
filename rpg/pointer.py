import arcade


class Pointer(arcade.Sprite):
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)
        self.left_click = False
        self.right_click = False
        self.default_pointer = filename
        self.hover_pointer = "assets/pointers/finger_pointing.png"
        self.grab_pointer = "assets/pointers/finger_grabbing.png"
        hitbox_points = [
            (-5, 7),  # Top-left
            (1, 0),  # Top-right
            (4, 0),  # Bottom-right
            (-5, 0),  # Bottom-left
        ]
        self.set_hit_box(hitbox_points)

    def update_pointer_image(self, state):
        if state == "default":
            self.texture = arcade.load_texture(self.default_pointer)
        elif state == "hover":
            self.texture = arcade.load_texture(self.hover_pointer)
        elif state == "grab":
            self.texture = arcade.load_texture(self.grab_pointer)

    def update(self, pos_x, pos_y):
        self.center_x = pos_x
        self.center_y = pos_y