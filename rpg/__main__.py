import arcade
from pointer import Pointer
from player import Player

SPRITE_SCALING = 0.5

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Labyrinth of Mort"


class HomeButtonBar(arcade.Sprite):
    def __init__(self, filename, offset_x, scale=1):
        super().__init__(filename, scale)
        self.offset_x = offset_x

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - self.offset_x
        self.center_y = window_pos_y / 2


class HomeButton(arcade.Sprite):
    def __init__(self, filename, pressed_image, button_bar, y_offset, scale=1):
        super().__init__(filename, scale)
        self.up_image = filename
        self.pressed = False
        self.pressed_image_loaded = False
        self.up_image_loaded = False
        self.pressed_image = pressed_image
        self.button_bar = button_bar
        self.y_offset = y_offset

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
        
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        arcade.set_background_color(arcade.color.AMAZON)
        self.home_button_bar = HomeButtonBar(
            filename="assets/gui/button_bar/home_button_bar.png", offset_x=30
        )
        self.button_list = arcade.SpriteList()
        self.inventory_button = HomeButton(
            filename="assets/gui/button/inventory_up.png",
            pressed_image="assets/gui/button/inventory_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=100,
        )
        self.vault_button = HomeButton(
            filename="assets/gui/button/vault_up.png",
            pressed_image="assets/gui/button/vault_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=50,
        )
        self.shop_button = HomeButton(
            filename="assets/gui/button/shop_up.png",
            pressed_image="assets/gui/button/shop_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=0,
        )
        self.dungeon_button = HomeButton(
            filename="assets/gui/button/dungeon_up.png",
            pressed_image="assets/gui/button/dungeon_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=-50,
        )
        self.info_button = HomeButton(
            filename="assets/gui/button/info_up.png",
            pressed_image="assets/gui/button/info_pressed.png",
            button_bar=self.home_button_bar,
            y_offset=-100,
        )
        self.button_list.append(self.inventory_button)
        self.button_list.append(self.vault_button)
        self.button_list.append(self.shop_button)
        self.button_list.append(self.dungeon_button)
        self.button_list.append(self.info_button)

        self.set_mouse_visible(False)
        self.pointer = Pointer(filename="assets/pointers/gold_arrow.png")
        self.player = Player(filename="assets/player/base/human.png")

        self.background = arcade.load_texture("assets/background/forest.png")

        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.width, self.height, self.background
        )
        self.player.draw(pixelated=True)

        # GUI Stuff
        self.camera_gui.use()
        self.home_button_bar.draw()
        self.button_list.draw()
        self.pointer.draw()
        # self.pointer.draw_hit_box(arcade.color.RED, line_thickness=1)
        
    def button_press_pointer_check(self):
        if button := arcade.check_for_collision_with_list(
            self.pointer, self.button_list
        ):  
            if button[0].pressed:
                button[0].pressed = False
                return
            
            for other_button in self.button_list:
                other_button.pressed = False
            button[0].pressed = True
            
    def on_mouse_press(self, x, y, button, modifiers):
        self.button_press_pointer_check()
        
    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass

    def on_update(self, delta_time):
        self.pointer.update(self._mouse_x, self._mouse_y)
        self.player.update()

        self.home_button_bar.update(self.width, self.height)
        self.button_list.update()

    def on_resize(self, width, height):
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
