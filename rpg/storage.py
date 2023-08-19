import arcade

BASE_X_OFFSET = 22
BASE_Y_OFFSET = -68
SLOT_SIZE = 32
SLOT_ROW_OFFSET_X = SLOT_SIZE + 5
SLOT_ROW_OFFSET_Y = SLOT_SIZE + 4
SLOTS_PER_ROW = 4

EQUIPMENT_SLOTS_CONFIG = [
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

class TestItem(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/test_item.png") 
        self.width = 16
        self.height = 16


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
        self.map_slots()

    def map_slots(self):
        self.map_inventory_slots()
        self.map_equipment_slots()

    def map_inventory_slots(self):
        base_x = self.center_x + BASE_X_OFFSET
        base_y = self.center_y + BASE_Y_OFFSET

        for row in range(6):
            for slot in range(SLOTS_PER_ROW):
                x = base_x + SLOT_ROW_OFFSET_X * slot
                y = base_y + SLOT_ROW_OFFSET_Y * row
                self.mapped_slots['inventory'].append((x, y))
                self.add_slot_sprite(self.inventory_slot_sprites, x, y)

    def map_equipment_slots(self):
        for equipment, x_offset, y_offset in EQUIPMENT_SLOTS_CONFIG:
            x = self.center_x + x_offset
            y = self.center_y + y_offset
            self.mapped_slots['equipment'].append((x, y))
            self.add_slot_sprite(self.equipment_slot_sprites, x, y)

    def add_slot_sprite(self, sprite_list, x, y):
        slot_sprite = arcade.Sprite("assets/square.png", scale=1, hit_box_algorithm=None)
        slot_sprite.width = 16
        slot_sprite.height = 16
        slot_sprite.center_x = x
        slot_sprite.center_y = y
        sprite_list.append(slot_sprite)

    def draw_inventory_slots(self):
        for slot_sprite in self.inventory_slot_sprites:
            slot_sprite.draw_hit_box(color=arcade.color.RED)
        for equipment_sprite in self.equipment_slot_sprites:
            equipment_sprite.draw_hit_box(color=arcade.color.BLUE) 

    def draw(self):
        super().draw()
        self.draw_inventory_slots()

    def update_slot_positions(self, sprite_list, delta_x, delta_y):
        for sprite in sprite_list:
            sprite.center_x += delta_x
            sprite.center_y += delta_y

    def update(self, window_pos_x, window_pos_y):
        delta_x = window_pos_x - 211 - self.center_x
        delta_y = (window_pos_y / 2 - 10) - self.center_y
        self.center_x = window_pos_x - 211
        self.center_y = window_pos_y / 2 - 10

        self.update_slot_positions(self.inventory_slot_sprites, delta_x, delta_y)
        self.update_slot_positions(self.equipment_slot_sprites, delta_x, delta_y)
            
class Vault(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x - 249
        self.center_y = center_y / 2 + 10

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - 249
        self.center_y = window_pos_y / 2 + 10