import arcade
import random


class Item(arcade.Sprite):
    def __init__(
        self,
        filename,
        scale=1,
        mapped_slot_position=None,
        slot_index=None,
        item_type=None,
    ):
        super().__init__(filename, scale)
        self.center_x, self.center_y = mapped_slot_position
        self.slot_index = slot_index
        self.original_slot_index = slot_index
        self.foo_stat = random.randint(1, 100)
        self.item_type = item_type
