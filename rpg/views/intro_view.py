from .home_view import HomeView
import arcade


class IntroView(arcade.View):
    def __init__(self, text_speed=0.3):
        super().__init__()
        with open("assets/intro_text.txt", "r") as file:
            self.text = file.read()
        self.text_speed = text_speed
        self.font_size = 16
        # Set the initial position to start off-screen below the window
        self.text_position_y = -self.window.height - 200
        self.background_color = arcade.color.BLACK
        self.background = arcade.load_texture("assets/background/battleback8.png")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.window.width, self.window.height, self.background
        )
        width = self.window.width - 40
        arcade.draw_text(
            self.text,
            self.window.width // 2,
            self.text_position_y,
            arcade.color.DARK_BLUE,
            self.font_size,
            width=width,
            align="center",
            anchor_x="center",
            anchor_y="bottom",
            bold=True,
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        home_view = HomeView()
        self.window.show_view(home_view)

    def on_update(self, delta_time):
        self.text_position_y += self.text_speed
