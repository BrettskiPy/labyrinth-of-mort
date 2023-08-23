import arcade
import random
from item import Item

INV_OFFSET = 60

BASE_X_OFFSET = 22
BASE_Y_OFFSET = -14
SLOT_SIZE = 32
SLOT_ROW_OFFSET_X = SLOT_SIZE + 5
SLOT_ROW_OFFSET_Y = SLOT_SIZE + 4
SLOTS_PER_ROW = 4

EQUIPMENT_SLOTS_CONFIG = [
    ("necklace", -33, 156),
    ("helmet", -77, 156),
    ("offhand", -33, 110),
    ("chest", -77, 110),
    ("sword", -121, 110),
    ("right ring", -33, 65),
    ("legs", -77, 65),
    ("left ring", -121, 65),
    ("boots", -77, 20),
]


class Inventory(arcade.Sprite):
    def __init__(self, filename, window_width, window_height, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.item_glabbed = False
        self.grabbed_item = None
        self.center_x = window_width - 211
        self.center_y = window_height / 2 - INV_OFFSET
        self.inventory_slot_sprites = arcade.SpriteList()
        self.equipment_slot_sprites = arcade.SpriteList()
        self.mapped_slots = {"inventory": [], "equipment": []}
        self.map_slots()
        self.item_list = arcade.SpriteList()
        self.item_data_window = arcade.Sprite(
            "assets/gui/storage/item_data_window.png", scale=1
        )

    def add_new_item(self):
        available_slot = self.find_next_available_slot()
        if available_slot is not None and available_slot < len(
            self.mapped_slots["inventory"]
        ):
            new_item = Item(
                filename=random.choice(
                    [
                        "assets/test_item1.png",
                        "assets/test_item2.png",
                        "assets/test_item3.png",
                    ]
                ),
                slot_index=available_slot,
                mapped_slot_position=self.mapped_slots["inventory"][available_slot],
                item_type=random.choice(["helmet", "necklace", "offhand", "chest"]),
            )
            self.item_list.append(new_item)
        else:
            print("Inventory full!")

    def find_next_available_slot(self):
        occupied_slots = [item.slot_index for item in self.item_list]
        for slot in range(
            len(self.mapped_slots["inventory"]) + len(self.mapped_slots["equipment"])
        ):
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
                self.mapped_slots["inventory"].append((x, y))
                slot_sprite = self.add_slot_sprite(self.inventory_slot_sprites, x, y)
                slot_sprite.slot_number = slot_number
                slot_number += 1

    def map_equipment_slots(self):
        equipment_slot_index = 0
        for equipment, x_offset, y_offset in EQUIPMENT_SLOTS_CONFIG:
            x = self.center_x + x_offset
            y = self.center_y + y_offset
            self.mapped_slots["equipment"].append((x, y))
            slot_sprite = self.add_slot_sprite(self.equipment_slot_sprites, x, y)
            slot_sprite.equipment_slot_index = equipment_slot_index
            equipment_slot_index += 1

    def add_slot_sprite(self, sprite_list, x, y):
        slot_sprite = arcade.Sprite(
            "assets/square.png", scale=1, hit_box_algorithm=None
        )
        slot_sprite.width = 16
        slot_sprite.height = 16
        slot_sprite.center_x = x
        slot_sprite.center_y = y
        sprite_list.append(slot_sprite)
        return slot_sprite

    def draw_inventory_slots(self):
        for slot_sprite in self.inventory_slot_sprites:
            slot_sprite.draw_hit_box(color=arcade.color.RED)
        for equipment_sprite in self.equipment_slot_sprites:
            equipment_sprite.draw_hit_box(color=arcade.color.BLUE)

    def draw_item_stats_if_hovered(self, control_key_pressed, pointer):
        if control_key_pressed:
            hovered_item = pointer.collides_with_list(self.item_list)
            if hovered_item:
                item = hovered_item[0]
                x, y = item.center_x, item.center_y

                stats_text = f"Test Stat: {item.foo_stat}"
                index_text = f"Index: {item.slot_index}"
                item_type_text = f"Type: {item.item_type}"

                # Update the sprite's position
                self.item_data_window.center_x = x - 50
                self.item_data_window.center_y = y + 118
                self.item_data_window.draw()  # Draw the sprite

                # Draw text on top of the sprite
                arcade.draw_text(
                    stats_text,
                    x - 110,
                    y + 200,
                    arcade.color.WHITE,
                    font_size=12,
                    bold=True,
                )
                arcade.draw_text(
                    index_text,
                    x - 108,
                    y + 180,
                    arcade.color.WHITE,
                    font_size=12,
                    bold=True,
                )
                arcade.draw_text(
                    item_type_text,
                    x - 110,
                    y + 160,
                    arcade.color.WHITE,
                    font_size=12,
                    bold=True,
                )

    def draw(self, control_key_pressed, pointer):
        super().draw()
        self.item_list.draw()
        if self.grabbed_item:
            self.grabbed_item.draw()

        self.draw_item_stats_if_hovered(control_key_pressed, pointer)
        # arcade.draw_text("ATK: 123", start_x=self.center_x - 140, start_y=self.center_y - self.height + 350, font_size=12)

    def update_slot_positions(self, sprite_list, delta_x, delta_y):
        for sprite in sprite_list:
            sprite.center_x += delta_x
            sprite.center_y += delta_y

    def update_item_positions(self, delta_x, delta_y):
        for item in self.item_list:
            item.center_x += delta_x
            item.center_y += delta_y

    def handle_item_drag_and_drop(self, pointer):
        if not self.grabbed_item and pointer.left_click:
            collided_items = pointer.collides_with_list(self.item_list)
            if collided_items:
                self.grabbed_item = collided_items[0]
                self.grabbed_item.original_slot_index = self.grabbed_item.slot_index
                self.item_list.remove(self.grabbed_item)

        if self.grabbed_item:
            self.grabbed_item.center_x = pointer.center_x
            self.grabbed_item.center_y = pointer.center_y
            if not pointer.left_click:
                if self.try_place_in_slot("inventory", self.inventory_slot_sprites):
                    return
                if self.try_place_in_slot("equipment", self.equipment_slot_sprites):
                    return
                self.reset_grabbed_item()

    def try_place_in_slot(self, slot_type, slot_sprites):
        for slot_sprite in slot_sprites:
            if self.grabbed_item.collides_with_sprite(slot_sprite):
                slot_number_attr = (
                    "slot_number"
                    if slot_type == "inventory"
                    else "equipment_slot_index"
                )
                slot_number = getattr(slot_sprite, slot_number_attr)

                # Check for equipment slots and verify the item type
                if slot_type == "equipment":
                    slot_number += len(self.mapped_slots["inventory"])
                    expected_equipment_type = EQUIPMENT_SLOTS_CONFIG[
                        slot_number - len(self.mapped_slots["inventory"])
                    ][0]
                    if self.grabbed_item.item_type != expected_equipment_type:
                        continue  # Skip this slot if the item type doesn't match

                existing_item = next(
                    (item for item in self.item_list if item.slot_index == slot_number),
                    None,
                )

                # If we're trying to place an item in an equipment slot and the existing item type doesn't match, continue
                if (
                    existing_item
                    and slot_type == "equipment"
                    and existing_item.item_type != self.grabbed_item.item_type
                ):
                    continue

                # If we're swapping between inventory and equipment and the types don't match, deny the swap
                if (
                    existing_item
                    and self.grabbed_item.original_slot_index
                    < len(self.mapped_slots["inventory"])
                    and existing_item.slot_index >= len(self.mapped_slots["inventory"])
                    and existing_item.item_type != self.grabbed_item.item_type
                ):
                    continue

                # If the slot is occupied, swap the items
                if existing_item:
                    existing_item.slot_index = self.grabbed_item.original_slot_index
                    (
                        existing_item.center_x,
                        existing_item.center_y,
                    ) = self.get_mapped_slot(existing_item.slot_index)

                self.grabbed_item.slot_index = slot_number
                (
                    self.grabbed_item.center_x,
                    self.grabbed_item.center_y,
                ) = self.get_mapped_slot(slot_number)
                self.item_list.append(self.grabbed_item)
                self.grabbed_item = None
                return True
        return False

    def handle_item_equip(self, pointer):
        if not pointer.right_click:
            return

        collided_items = pointer.collides_with_list(self.item_list)
        if collided_items:
            clicked_item = collided_items[0]

            # Check if the clicked item is in an equipment slot
            if clicked_item.slot_index >= len(self.mapped_slots["inventory"]):
                # Find the next available inventory slot
                available_slot = self.find_next_available_slot()
                if available_slot is not None:
                    clicked_item.slot_index = available_slot
                    clicked_item.center_x, clicked_item.center_y = self.get_mapped_slot(
                        available_slot
                    )
            else:
                # Equip the item
                slot_index = self.find_equipment_slot_for_item(clicked_item.item_type)
                if slot_index is not None:
                    existing_item = next(
                        (
                            item
                            for item in self.item_list
                            if item.slot_index == slot_index
                        ),
                        None,
                    )

                    if existing_item:
                        # Swap the items
                        existing_item.slot_index = clicked_item.slot_index
                        (
                            existing_item.center_x,
                            existing_item.center_y,
                        ) = self.get_mapped_slot(existing_item.slot_index)

                    clicked_item.slot_index = slot_index
                    clicked_item.center_x, clicked_item.center_y = self.get_mapped_slot(
                        slot_index
                    )

    def find_equipment_slot_for_item(self, item_type):
        for index, (equipment_type, _, _) in enumerate(EQUIPMENT_SLOTS_CONFIG):
            if equipment_type == item_type:
                return len(self.mapped_slots["inventory"]) + index
        return None

    def get_mapped_slot(self, slot_index):
        return (
            self.mapped_slots["inventory"][slot_index]
            if slot_index < len(self.mapped_slots["inventory"])
            else self.mapped_slots["equipment"][
                slot_index - len(self.mapped_slots["inventory"])
            ]
        )

    def recalculate_slot_mappings(self):
        self.mapped_slots["inventory"] = []
        self.mapped_slots["equipment"] = []
        self.map_slots()

    def reset_grabbed_item(self):
        self.grabbed_item.slot_index = self.grabbed_item.original_slot_index
        self.grabbed_item.center_x, self.grabbed_item.center_y = self.get_mapped_slot(
            self.grabbed_item.original_slot_index
        )
        self.item_list.append(self.grabbed_item)
        self.grabbed_item = None

    def update(self, window_width, window_height, pointer):
        delta_x = window_width - 211 - self.center_x
        delta_y = (window_height / 2 - INV_OFFSET) - self.center_y

        # Check if the window has been resized
        if delta_x != 0 or delta_y != 0:
            self.center_x = window_width - 211
            self.center_y = window_height / 2 - INV_OFFSET
            self.update_slot_positions(self.inventory_slot_sprites, delta_x, delta_y)
            self.update_slot_positions(self.equipment_slot_sprites, delta_x, delta_y)
            self.update_item_positions(delta_x, delta_y)
            self.recalculate_slot_mappings()  # Recalculate the slot mappings
        self.handle_item_drag_and_drop(pointer)
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
