import arcade
from constants import DEFAULT_SCREEN_HEIGHT, DEFAULT_SCREEN_WIDTH, SCREEN_TITLE
from views.intro_view import IntroView


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.views = {}


def main():
    window = Window(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    intro_view = IntroView()
    window.show_view(intro_view)
    arcade.run()


if __name__ == "__main__":
    main()
