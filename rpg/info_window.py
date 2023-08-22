import arcade
import time
import random

from math import sin,  pi, atan, atan2, cos

class InfoWindow(arcade.Sprite):
    def __init__(self, filename, window_width, window_height, scale=2):
        super().__init__(filename, scale)
        self.window_width = window_width
        self.window_height = window_height
        self.center_x = self.window_width / 2
        self.center_y = self.window_height / 2
        self.eye_globe = arcade.Sprite("assets/gui/info/blank_eye.png", scale=2)
        self.eye_center = arcade.Sprite("assets/gui/info/eye_center.png", scale=2)
        self.pupil = arcade.Sprite("assets/gui/info/pupil.png", scale=1)
        self.pupil_state = 0
        self.pupil_scale_target = 1
        self.pupil_scale_time = 0
        self.update_eye_globe_position()
        self.start_time = time.time()  
        self.update_eye_center_position(0, 0)

    def draw(self):
        super().draw()
        self.eye_globe.draw()
        self.eye_center.draw()
        self.pupil.draw()
        top_text_y = self.center_y + self.height / 2 - 40
        bottom_text_y = self.center_y - self.height / 2 + 40
        arcade.draw_text("Coded by BrettskiPy", self.center_x, top_text_y, arcade.color.WHITE, 16, anchor_x="center", bold=True)
        arcade.draw_text("With special thanks to", self.center_x, bottom_text_y, arcade.color.WHITE, 16, anchor_x="center", bold=True)
        arcade.draw_text("the Python Arcade Library", self.center_x, bottom_text_y - 20, arcade.color.WHITE, 16, anchor_x="center", bold=True)

    def update_eye_globe_position(self):
        # Position the centered sprite relative to the InfoWindow
        self.eye_globe.center_x = self.center_x
        self.eye_globe.center_y = self.center_y

    def update_eye_center_position(self, mouse_x, mouse_y):
        # Calculate the angle between the eye globe center and the mouse pointer
        angle = atan2(mouse_y - self.eye_globe.center_y, mouse_x - self.eye_globe.center_x)
        distance = 15
        self.eye_center.center_x = self.eye_globe.center_x + cos(angle) * distance
        self.eye_center.center_y = self.eye_globe.center_y + sin(angle) * distance
        self.pupil.center_x = self.eye_center.center_x
        self.pupil.center_y = self.eye_center.center_y
        # Determine the current time
        t = time.time() - self.start_time

        # Randomly decide to change the pupil state
        if random.random() < 0.01:  # 1% chance per frame
            self.pupil_state = random.choice([0, 1, 2])  # Normal, expand, or contract
            self.pupil_scale_time = t

        # Update the pupil scale based on the state
        if self.pupil_state == 0:  # Normal
            self.pupil_scale_target = 1.5
        elif self.pupil_state == 1:  # Expand
            self.pupil_scale_target = 2.5
        elif self.pupil_state == 2:  # Contract
            self.pupil_scale_target = 1.1

        # Smoothly transition to the target scale over 0.5 seconds
        transition_time = 0.5
        progress = min((t - self.pupil_scale_time) / transition_time, 1)
        self.pupil.scale = self.pupil.scale + (self.pupil_scale_target - self.pupil.scale) * progress

    def update(self, window_width, window_height, mouse_x, mouse_y):
        delta_x = window_width - self.window_width
        delta_y = window_height - self.window_height

        # Check if the window has been resized
        if delta_x != 0 or delta_y != 0:
            self.window_width = window_width
            self.window_height = window_height
            self.center_x = self.window_width / 2
            self.center_y = self.window_height / 2
            self.update_eye_globe_position()

        # Update the eye center position to follow the mouse pointer
        self.update_eye_center_position(mouse_x, mouse_y)