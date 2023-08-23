import arcade
from pointer import Pointer
from player import Player
from storage import Inventory, Vault
from info_window import InfoWindow
from constants import DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT


class HomeButtonBar(arcade.Sprite):
    def __init__(self, filename, offset_x, scale=1):
        super().__init__(filename, scale)
        self.offset_x = offset_x

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - self.offset_x
        self.center_y = window_pos_y / 2


class HomeButton(arcade.Sprite):
    def __init__(
        self, filename, pressed_image, button_bar, y_offset, reference, scale=1
    ):
        super().__init__(filename, scale)
        self.up_image = filename
        self.pressed_image = pressed_image
        self.button_bar = button_bar
        self.y_offset = y_offset
        self.reference = reference

        self.pressed = False
        self.pressed_image_loaded = False
        self.up_image_loaded = False

    def update(self):
        self.center_x = self.button_bar.center_x
        self.center_y = self.button_bar.center_y + self.y_offset

        if self.pressed:
            if self.pressed_image_loaded is False:
                self.texture = arcade.load_texture(self.pressed_image)
                self.pressed_image_loaded = True
                self.up_image_loaded = False
        else:
            if self.up_image_loaded is False:
                self.texture = arcade.load_texture(self.up_image)
                self.up_image_loaded = True
                self.pressed_image_loaded = False


class HomeView(arcade.View):
    def __init__(self):
        super().__init__()

        self.home_button_bar = HomeButtonBar(
            filename="assets/gui/button_bar/home_button_bar.png", offset_x=30
        )
        self.button_list = arcade.SpriteList()
        self.inventory_button = HomeButton(
            filename="assets/gui/button/inventory_up.png",
            pressed_image="assets/gui/button/inventory_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=100,
            reference="inventory",
        )
        self.vault_button = HomeButton(
            filename="assets/gui/button/vault_up.png",
            pressed_image="assets/gui/button/vault_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=50,
            reference="vault",
        )
        self.shop_button = HomeButton(
            filename="assets/gui/button/shop_up.png",
            pressed_image="assets/gui/button/shop_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=0,
            reference="shop",
        )
        self.dungeon_button = HomeButton(
            filename="assets/gui/button/dungeon_up.png",
            pressed_image="assets/gui/button/dungeon_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=-50,
            reference="dungeon",
        )
        self.info_button = HomeButton(
            filename="assets/gui/button/info_up.png",
            pressed_image="assets/gui/button/info_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=-100,
            reference="info",
        )
        self.button_list.append(self.inventory_button)
        self.button_list.append(self.vault_button)
        self.button_list.append(self.shop_button)
        self.button_list.append(self.dungeon_button)
        self.button_list.append(self.info_button)

        self.control_key_pressed = False
        self.window.set_mouse_visible(False)
        self.pointer = Pointer(filename="assets/pointers/gold_arrow.png")
        self.player = Player(filename="assets/player/base/human.png")
        self.inventory = None
        self.vault = None
        self.info_window = None

        self.default_background = True
        self.background = arcade.load_texture("assets/background/battleback4.png")

        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.window.width, self.window.height, self.background
        )
        self.player.draw(pixelated=True)

        # GUI Stuff
        self.home_button_bar.draw()
        self.button_list.draw()

        if self.info_window:
            self.info_window.draw()

        if self.inventory:
            self.inventory.draw(self.control_key_pressed, self.pointer)

        if self.vault:
            self.vault.draw()

        self.pointer.draw()
        # self.pointer.draw_hit_box(arcade.color.RED, line_thickness=1)

    def handle_info_event(self):
        if self.info_window:
            self.info_window = None
        else:
            self.close_all_windows()
            self.info_window = InfoWindow(
                filename="assets/gui/info/blue_card.png",
                window_width=self.window.width,
                window_height=self.window.height,
            )

    def toggle_button_press(self, button):
        if button.pressed:
            button.pressed = False
        else:
            for other_button in self.button_list:
                other_button.pressed = False
            button.pressed = True

    def close_all_windows(self):
        self.inventory = None
        self.vault = None
        self.info_window = None

    def handle_inventory_event(self):
        if self.inventory:
            self.inventory = None
        else:
            self.close_all_windows()
            self.inventory = Inventory(
                filename="assets/gui/storage/inventory.png",
                window_width=self.window.width,
                window_height=self.window.height,
            )

    def handle_right_click_event(self):
        if self.inventory:
            self.inventory.handle_item_equip(self.pointer)

    def handle_vault_event(self):
        if self.vault:
            self.vault = None
        else:
            self.close_all_windows()
            self.vault = Vault(
                filename="assets/gui/storage/vault.png",
                center_x=self.window.width,
                center_y=self.window.height,
            )

    def update_pointer_image_from_event(self):
        if self.inventory and self.inventory.grabbed_item:
            self.pointer.update_pointer_image("grab")
        elif self.inventory and self.pointer.collides_with_list(
            self.inventory.item_list
        ):
            self.pointer.update_pointer_image("hover")
        else:
            self.pointer.update_pointer_image("default")

    def handle_button_press_events(self):
        if button := arcade.check_for_collision_with_list(
            self.pointer, self.button_list
        ):
            clicked_button = button[0]
            self.toggle_button_press(clicked_button)
            event_handlers = {
                "inventory": self.handle_inventory_event,
                "vault": self.handle_vault_event,
                "info": self.handle_info_event,  # Add this line
            }
            event_handler = event_handlers.get(clicked_button.reference)
            if event_handler:
                event_handler()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.handle_button_press_events()
            self.pointer.left_click = True

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.handle_right_click_event()
            self.pointer.right_click = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.pointer.left_click = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.inventory.add_new_item()
        if key == arcade.key.LCTRL:
            self.control_key_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LCTRL:
            self.control_key_pressed = False

    def on_update(self, delta_time):
        self.pointer.update(self.window._mouse_x, self.window._mouse_y)
        self.player.update()
        self.home_button_bar.update(self.window.width, self.window.height)
        self.button_list.update()
        self.update_pointer_image_from_event()

        if self.inventory:
            self.inventory.update(self.window.width, self.window.height, self.pointer)

        if self.vault:
            self.vault.update(self.window.width, self.window.height)

        if self.info_window:  # Add this block
            mouse_x = self.window._mouse_x
            mouse_y = self.window._mouse_y
            self.info_window.update(
                self.window.width, self.window.height, mouse_x, mouse_y
            )

    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
