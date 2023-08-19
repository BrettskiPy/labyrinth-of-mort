import arcade


class Inventory(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = self.center_x  + 22
        self.center_y = self.center_y - 68

    def debug_draw_inventory_slots(self):
        # Constants
        BASE_X_OFFSET = 22
        BASE_Y_OFFSET = -68
        SLOT_SIZE = 32
        SLOT_ROW_OFFSET_X = SLOT_SIZE + 5
        SLOT_ROW_OFFSET_Y = SLOT_SIZE + 4
        SLOTS_PER_ROW = 4
        RED_COLOR = arcade.color.RED
        BLUE_COLOR = arcade.color.BLUE

        # Calculate base coordinates
        base_x = self.center_x + BASE_X_OFFSET
        base_y = self.center_y + BASE_Y_OFFSET

        # Draw inventory slots
        for row in range(6):
            for slot in range(SLOTS_PER_ROW):
                x = base_x + SLOT_ROW_OFFSET_X * slot
                y = base_y + SLOT_ROW_OFFSET_Y * row
                self._draw_slot(x, y, SLOT_SIZE, SLOT_SIZE, RED_COLOR)

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

        # Draw equipment slots
        for _, x_offset, y_offset in equipment_slots:
            x = self.center_x + x_offset
            y = self.center_y + y_offset
            self._draw_slot(x, y, SLOT_SIZE, SLOT_SIZE, BLUE_COLOR)

    def _draw_slot(self, x, y, width, height, color):
        """Helper function to draw a rectangle for an inventory slot."""
        arcade.draw_rectangle_outline(x, y, width, height, color)


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