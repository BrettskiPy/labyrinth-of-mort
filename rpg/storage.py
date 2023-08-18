import arcade


class Inventory(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x - 187
        self.center_y = center_y / 2 + 14

    def debug_draw_inventory_slots(self):
        # Adjust base_x and base_y based on sprite's current position
        base_x = self.center_x  + 22
        base_y = self.center_y - 68
        
        offset_x = 32 + 4
        offset_y = 32 + 4
        slots_per_row = 4

        for row in range(6):
            for slot in range(slots_per_row):
                arcade.draw_rectangle_outline(base_x + offset_x * slot,
                                              base_y + offset_y * row,
                                              32, 32, arcade.color.RED)
        # # necklace
        # arcade.draw_rectangle_outline(self.center_x - 45, self.center_y + 105, 32, 32, arcade.color.BLUE)
        # # helmet
        # arcade.draw_rectangle_outline(self.center_x - 77, self.center_y + 105, 32, 32, arcade.color.BLUE)
        # # shield
        # arcade.draw_rectangle_outline(self.center_x - 45, self.center_y + 74, 32, 32, arcade.color.BLUE)
        # arcade.draw_rectangle_outline(self.center_x - 40, self.center_y + 90, 32, 32, arcade.color.BLUE)
        # arcade.draw_rectangle_outline(self.center_x - 40, self.center_y + 90, 32, 32, arcade.color.BLUE)
        # arcade.draw_rectangle_outline(self.center_x - 40, self.center_y + 90, 32, 32, arcade.color.BLUE)
        # arcade.draw_rectangle_outline(self.center_x - 40, self.center_y + 90, 32, 32, arcade.color.BLUE)
        # arcade.draw_rectangle_outline(self.center_x - 40, self.center_y + 90, 32, 32, arcade.color.BLUE)
        # arcade.draw_rectangle_outline(self.center_x - 40, self.center_y + 90, 32, 32, arcade.color.BLUE)

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