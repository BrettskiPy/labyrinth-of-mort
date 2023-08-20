import arcade
import pointer
from player import Player
from storage import Inventory, Vault


DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600


class HomeButtonBar(arcade.Sprite):
    def __init__(self, filename, offset_x, scale=1):
        super().__init__(filename, scale)
        self.offset_x = offset_x

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - self.offset_x
        self.center_y = window_pos_y / 2


class HomeButton(arcade.Sprite):
    def __init__(self, filename, pressed_image, button_bar, y_offset, reference, scale=1):
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
            reference='inventory'
        )
        self.vault_button = HomeButton(
            filename="assets/gui/button/vault_up.png",
            pressed_image="assets/gui/button/vault_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=50,
            reference='vault'
        )
        self.shop_button = HomeButton(
            filename="assets/gui/button/shop_up.png",
            pressed_image="assets/gui/button/shop_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=0,
            reference='shop'
        )
        self.dungeon_button = HomeButton(
            filename="assets/gui/button/dungeon_up.png",
            pressed_image="assets/gui/button/dungeon_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=-50,
            reference='dungeon'
        )
        self.info_button = HomeButton(
            filename="assets/gui/button/info_up.png",
            pressed_image="assets/gui/button/info_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=-100,
            reference='info'
        )
        self.button_list.append(self.inventory_button)
        self.button_list.append(self.vault_button)
        self.button_list.append(self.shop_button)
        self.button_list.append(self.dungeon_button)
        self.button_list.append(self.info_button)

        self.window.set_mouse_visible(False)
        self.pointer = pointer.Pointer(filename="assets/pointers/gold_arrow.png")
        self.player = Player(filename="assets/player/base/human.png")
        self.inventory = None
        self.vault = None

        self.default_background = True
        self.background = arcade.load_texture("assets/background/forest.png")

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
        self.camera_gui.use()
        self.home_button_bar.draw()
        self.button_list.draw()
        if self.inventory:
            self.inventory.draw()

        if self.vault:
            self.vault.draw()


        self.pointer.draw()
        # self.pointer.draw_hit_box(arcade.color.RED, line_thickness=1)

    def toggle_button_press(self, button):
        if button.pressed:
            button.pressed = False
        else:
            for other_button in self.button_list:
                other_button.pressed = False
            button.pressed = True

    def close_all_storage(self):
        self.inventory = None
        self.vault = None

    def handle_inventory_event(self):
        if self.inventory:
            self.inventory = None
        else:
            self.close_all_storage()  
            self.inventory = Inventory(filename="assets/gui/storage/inventory.png", window_width=self.window.width, window_height=self.window.height)

    def handle_vault_event(self):
        if self.vault:
            self.vault = None
        else:
            self.close_all_storage()
            self.vault = Vault(filename="assets/gui/storage/vault.png", 
                               center_x=self.window.width, center_y=self.window.height)
            
    def button_press_check_event_launch(self):

        if button := arcade.check_for_collision_with_list(self.pointer, self.button_list):
            clicked_button = button[0]
            self.toggle_button_press(clicked_button)
            
            if clicked_button.reference == 'inventory':
                self.handle_inventory_event()
            elif clicked_button.reference == 'vault':
                self.handle_vault_event()

    def on_mouse_press(self, x, y, button, modifiers):
        self.button_press_check_event_launch()

    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass

    def on_update(self, delta_time):
        self.pointer.update(self.window._mouse_x, self.window._mouse_y)
        self.player.update()
        self.home_button_bar.update(self.window.width, self.window.height)
        self.button_list.update()

        if self.inventory:
            self.inventory.update(self.window.width, self.window.height)

        if self.vault:
            self.vault.update(self.window.width, self.window.height)
            
    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))