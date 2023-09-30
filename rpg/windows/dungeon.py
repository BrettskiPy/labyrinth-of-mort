import arcade

X_OFFSET = 270
Y_OFFSET = 10
PORTAL_SPACING = 60


def calculate_portal_positions(top_left_x, top_left_y):
    portal_positions = []
    for row in range(5):
        for col in range(6):
            x = top_left_x + col * PORTAL_SPACING + PORTAL_SPACING / 2
            y = top_left_y - row * PORTAL_SPACING - PORTAL_SPACING / 2
            portal_positions.append((x, y))
    return portal_positions


class Portal(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, level, scale=1):
        super().__init__(filename, scale)
        self.level = level
        self.center_x = center_x
        self.center_y = center_y


class Dungeon(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.center_x = center_x - X_OFFSET
        self.center_y = center_y / 2 + Y_OFFSET
        self.portal_list = arcade.SpriteList()
        self.map_portals()

    def map_portals(self):
        top_left_x = self.left + 14
        top_left_y = self.top - 24
        portal_positions = calculate_portal_positions(top_left_x, top_left_y)

        for i, (x, y) in enumerate(portal_positions, start=1):
            portal = Portal(f"assets/portals/portal_{i}.png", x, y, level=i, scale=1.3)
            self.portal_list.append(portal)

    def update_portals(self, delta_x, delta_y):
        for portal in self.portal_list:
            portal.center_x += delta_x
            portal.center_y += delta_y

    def draw(self):
        super().draw()
        self.portal_list.draw()

    def update(self, window_width, window_height):
        new_center_x = window_width - X_OFFSET
        new_center_y = window_height / 2 + Y_OFFSET
        delta_x = new_center_x - self.center_x
        delta_y = new_center_y - self.center_y

        if delta_x != 0 or delta_y != 0:
            self.center_x = new_center_x
            self.center_y = new_center_y
            self.update_portals(delta_x, delta_y)
