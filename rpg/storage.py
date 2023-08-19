import arcade


class Inventory(arcade.Sprite):
    def __init__(self, filename, scale=1):
        super().__init__(filename, scale)
        self.open = False

        self.inventory_slot_sprites = arcade.SpriteList()
        self.equipment_slot_sprites = arcade.SpriteList()
        self.mapped_slots = {
            'inventory': [],
            'equipment': []
        }
        self.slots_mapping()

    def slots_mapping(self):
        BASE_X_OFFSET = 22
        BASE_Y_OFFSET = -68
        SLOT_SIZE = 32
        SLOT_ROW_OFFSET_X = SLOT_SIZE + 5
        SLOT_ROW_OFFSET_Y = SLOT_SIZE + 4
        SLOTS_PER_ROW = 4

        # Base coordinates
        base_x = self.center_x + BASE_X_OFFSET
        base_y = self.center_y + BASE_Y_OFFSET

        # Map inventory slots
        for row in range(6):
            for slot in range(SLOTS_PER_ROW):
                x = base_x + SLOT_ROW_OFFSET_X * slot
                y = base_y + SLOT_ROW_OFFSET_Y * row
                self.mapped_slots['inventory'].append((x, y))

                slot_sprite = arcade.Sprite("assets/square.png", scale=1, hit_box_algorithm=None)
                slot_sprite.width = 16
                slot_sprite.height = 16 
                slot_sprite.center_x = x
                slot_sprite.center_y = y
                self.inventory_slot_sprites.append(slot_sprite)

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

        for equipment, x_offset, y_offset in equipment_slots:
            x = self.center_x + x_offset
            y = self.center_y + y_offset
            self.mapped_slots['equipment'].append((x, y))
            
            equipment_sprite = arcade.Sprite("assets/square.png", scale=1, hit_box_algorithm=None)
            equipment_sprite.width = 16
            equipment_sprite.height = 16
            equipment_sprite.center_x = x
            equipment_sprite.center_y = y
            self.equipment_slot_sprites.append(equipment_sprite)
            
    def draw_inventory_slots(self):
        for slot_sprite in self.inventory_slot_sprites:
            slot_sprite.draw_hit_box(color=arcade.color.RED)
        for equipment_sprite in self.equipment_slot_sprites:
            equipment_sprite.draw_hit_box(color=arcade.color.BLUE) 

    def draw(self):
        super().draw()
        self.draw_inventory_slots()

    def update(self, window_pos_x, window_pos_y):
        delta_x = window_pos_x - 211 - self.center_x
        delta_y = (window_pos_y / 2 - 10) - self.center_y
        self.center_x = window_pos_x - 211
        self.center_y = window_pos_y / 2 - 10

        for slot_sprite in self.inventory_slot_sprites:
            slot_sprite.center_x += delta_x
            slot_sprite.center_y += delta_y
        for equipment_sprite in self.equipment_slot_sprites:
            equipment_sprite.center_x += delta_x
            equipment_sprite.center_y += delta_y
            
class Vault(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x - 249
        self.center_y = center_y / 2 + 10

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - 249
        self.center_y = window_pos_y / 2 + 10