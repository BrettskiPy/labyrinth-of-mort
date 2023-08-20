import arcade
import random


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

class Item(arcade.Sprite):
    def __init__(self, filename, scale=1, mapped_slot_position=None, slot_index=None):
        super().__init__(filename, scale)
        self.center_x, self.center_y = mapped_slot_position
        self.slot_index = slot_index

class Inventory(arcade.Sprite):
    def __init__(self, filename, window_width, window_height, scale=1):
        super().__init__(filename, scale)
        self.open = False   
        self.item_glabbed = False

        self.center_x = window_width - 211
        self.center_y = window_height / 2 - 10

        self.inventory_slot_sprites = arcade.SpriteList()
        self.equipment_slot_sprites = arcade.SpriteList()
        self.mapped_slots = {
            'inventory': [],
            'equipment': []
        }
        self.map_slots()
        self.item_list = arcade.SpriteList()
        self.iconized_item = None

    def add_new_item(self):
        available_slot = self.find_next_available_slot()
        if available_slot is not None:
            new_item = Item(
                filename=random.choice(["assets/test_item1.png", "assets/test_item2.png" , "assets/test_item3.png"]),
                slot_index=available_slot,
                mapped_slot_position=self.mapped_slots['inventory'][available_slot]
            )
            self.item_list.append(new_item)
        else:
            print("Inventory full!")

    def find_next_available_slot(self):
        occupied_slots = [item.slot_index for item in self.item_list]
        for slot in range(len(self.mapped_slots['inventory'])):
            if slot not in occupied_slots:
                return slot
        return None  # Return None if all slots are occupied
    
    def map_slots(self):
        self.map_inventory_slots()
        self.map_equipment_slots()

    def map_inventory_slots(self):
        base_x = self.center_x + BASE_X_OFFSET
        base_y = self.center_y + BASE_Y_OFFSET
        slot_number = 0
        for row in range(6):
            for slot in range(SLOTS_PER_ROW):
                x = base_x + SLOT_ROW_OFFSET_X * slot
                y = base_y + SLOT_ROW_OFFSET_Y * row
                self.mapped_slots['inventory'].append((x, y))
                slot_sprite = self.add_slot_sprite(self.inventory_slot_sprites, x, y)
                slot_sprite.slot_number = slot_number
                slot_number += 1

    def map_equipment_slots(self):
        equipment_slot_number = 0
        for equipment, x_offset, y_offset in EQUIPMENT_SLOTS_CONFIG:
            x = self.center_x + x_offset
            y = self.center_y + y_offset
            self.mapped_slots['equipment'].append((x, y))
            slot_sprite = self.add_slot_sprite(self.equipment_slot_sprites, x, y)
            slot_sprite.equipment_slot_number = equipment_slot_number
            equipment_slot_number += 1

    def add_slot_sprite(self, sprite_list, x, y):
        slot_sprite = arcade.Sprite("assets/square.png", scale=1, hit_box_algorithm=None)
        slot_sprite.width = 16
        slot_sprite.height = 16
        slot_sprite.center_x = x
        slot_sprite.center_y = y
        sprite_list.append(slot_sprite)
        return slot_sprite

    def draw_inventory_slots(self):
        for slot_sprite in self.inventory_slot_sprites:
            # arcade.draw_text(str(slot_sprite.slot_number), slot_sprite.center_x, slot_sprite.center_y, arcade.color.WHITE, font_size=10, anchor_x="center", anchor_y="center")
            slot_sprite.draw_hit_box(color=arcade.color.RED)
        for equipment_sprite in self.equipment_slot_sprites:
            # arcade.draw_text(str(equipment_sprite.equipment_slot_number), equipment_sprite.center_x, equipment_sprite.center_y, arcade.color.WHITE, font_size=10, anchor_x="center", anchor_y="center")
            equipment_sprite.draw_hit_box(color=arcade.color.BLUE) 

    def draw(self):
        super().draw()
        self.draw_inventory_slots()
        self.item_list.draw()
        if self.iconized_item:
            self.iconized_item.draw()

    def update_slot_positions(self, sprite_list, delta_x, delta_y):
        for sprite in sprite_list:
            sprite.center_x += delta_x
            sprite.center_y += delta_y

    def update_item_positions(self, delta_x, delta_y):
        for item in self.item_list:
            item.center_x += delta_x
            item.center_y += delta_y

    def update(self, window_width, window_height, pointer):
        delta_x = window_width - 211 - self.center_x
        delta_y = (window_height / 2 - 10) - self.center_y
        self.center_x = window_width - 211
        self.center_y = window_height / 2 - 10
        self.update_slot_positions(self.inventory_slot_sprites, delta_x, delta_y)
        self.update_slot_positions(self.equipment_slot_sprites, delta_x, delta_y)
        self.update_item_positions(delta_x, delta_y)

        grabbed_item = pointer.collides_with_list(self.item_list)
        if grabbed_item and pointer.left_click:
            item = grabbed_item[0]
            print(item.position)
            print(item.slot_index)

        self.item_list.update()
            

class Vault(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x - 249
        self.center_y = center_y / 2 + 10

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - 249
        self.center_y = window_pos_y / 2 + 10