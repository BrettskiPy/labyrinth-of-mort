import arcade

VAULT_X_OFFSET = 249
VAULT_Y_OFFSET = 10


class Vault(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale=1):
        super().__init__(filename, scale)
        self.open = False
        self.center_x = center_x - VAULT_X_OFFSET
        self.center_y = center_y / 2 + VAULT_Y_OFFSET

    def update(self, window_pos_x, window_pos_y):
        self.center_x = window_pos_x - VAULT_X_OFFSET
        self.center_y = window_pos_y / 2 + VAULT_Y_OFFSET
