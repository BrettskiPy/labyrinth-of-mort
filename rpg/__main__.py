import arcade
from views.home_view import HomeView

SPRITE_SCALING = 0.5

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Labyrinth of Mort"


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.views = {}

def main():
    window = Window(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    home_view = HomeView()
    window.show_view(home_view)
    arcade.run()


if __name__ == "__main__":
    main()
