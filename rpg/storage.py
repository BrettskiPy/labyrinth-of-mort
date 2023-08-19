import arcade


class Inventory(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x
        self.center_y = center_y

        # Sprite for inventory items to snap items to
        self.square_sprite = arcade.Sprite("assets/square.png", scale=1, hit_box_algorithm=None)
        self.square_sprite.width = 16
        self.square_sprite.height = 16  

        # Sprite for equipment items to snap items to
        self.equipment_sprite = arcade.Sprite("assets/square.png", scale=1, hit_box_algorithm=None)
        self.equipment_sprite.width = 16
        self.equipment_sprite.height = 16  

    def debug_draw_inventory_slots(self):
        BASE_X_OFFSET = 22
        BASE_Y_OFFSET = -68
        SLOT_SIZE = 32
        SLOT_ROW_OFFSET_X = SLOT_SIZE + 5
        SLOT_ROW_OFFSET_Y = SLOT_SIZE + 4
        SLOTS_PER_ROW = 4

        # Base coordinates
        base_x = self.center_x + BASE_X_OFFSET
        base_y = self.center_y + BASE_Y_OFFSET

        # Draw inventory slots using square sprites
        for row in range(6):
            for slot in range(SLOTS_PER_ROW):
                x = base_x + SLOT_ROW_OFFSET_X * slot
                y = base_y + SLOT_ROW_OFFSET_Y * row
                self._draw_square_sprite(self.square_sprite, x, y, arcade.color.RED)

        # Equipment slots with their respective offsets
        equipment_slots = [
            ("necklace", -32, 103),
            ("helmet", -77, 103),
            ("offhand", -32, 58),
            ("chest", -77, 58),
            ("sword", -121, 58),
            ("right ring", -32, 13),
            ("legs", -77, 13),
            ("left ring", -121, 13),
            ("boots", -77, -32)
        ]

        # Draw equipment slots using square sprites with blue collision color
        for _, x_offset, y_offset in equipment_slots:
            x = self.center_x + x_offset
            y = self.center_y + y_offset
            self._draw_square_sprite(self.equipment_sprite, x, y, arcade.color.BLUE)

    def _draw_square_sprite(self, sprite, x, y, collision_color):
        sprite.center_x = x
        sprite.center_y = y
        sprite.draw_hit_box(color=collision_color, line_thickness=1)

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - 211
        self.center_y = window_pos_y / 2 - 10


class Vault(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x - 249
        self.center_y = center_y / 2 + 10

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - 249
        self.center_y = window_pos_y / 2 + 10