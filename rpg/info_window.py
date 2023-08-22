import arcade
import time
import random
from math import sin, atan2, cos


class FloatingEye:
    def __init__(self, scale, center_x, center_y):
        self.eye_globe = arcade.Sprite("assets/gui/info/blank_eye.png", scale)
        self.eye_center = arcade.Sprite("assets/gui/info/eye_center_white.png", scale)
        self.pupil = arcade.Sprite("assets/gui/info/pupil.png", scale * .7)
        self.delay = random.randint(0, 100)
        self.y_position = -self.delay
        self.y_speed = random.uniform(0.5, 2)

        self.eye_globe.center_x = center_x
        self.eye_globe.center_y = center_y

        # Randomize the eye color
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.eye_center._color = random_color


class InfoWindow(arcade.Sprite):
    def __init__(self, filename, window_width, window_height, scale=2):
        super().__init__(filename, scale)
        self.window_width = window_width
        self.window_height = window_height
        self.center_x = self.window_width / 2
        self.center_y = self.window_height / 2
        self.arcade_logo = arcade.Sprite("assets/gui/info/arcade_logo.png", scale=.5)
        self.eye_globe = arcade.Sprite("assets/gui/info/blank_eye.png", scale=1.3)
        self.eye_center = arcade.Sprite("assets/gui/info/eye_center.png", scale=1.3)
        self.pupil = arcade.Sprite("assets/gui/info/pupil.png", scale=.7)
        self.pupil_state = 0
        self.pupil_scale_target = 1
        self.pupil_scale_time = 0

        self.floating_eye_globes = arcade.SpriteList()
        self.floating_eye_centers = arcade.SpriteList()
        self.floating_eye_pupils = arcade.SpriteList()
        self.floating_eyes = [self.create_eye(scale=0.5) for _ in range(20)]

        self.update_eye_globe_position()
        self.start_time = time.time()
        self.update_eye_center_position(0, 0)
        self.update_arcade_logo_position()

    def create_eye(self, scale):
        eye_x = random.randint(int(self.left + 30), int(self.right - 30))
        eye_y = random.randint(int(self.bottom + 30), int(self.top - 30))
        eye = FloatingEye(scale, eye_x, eye_y)
        eye.y_position = eye_y - self.bottom

        self.floating_eye_globes.append(eye.eye_globe)
        self.floating_eye_centers.append(eye.eye_center)
        self.floating_eye_pupils.append(eye.pupil)

        return eye

    def update_floating_eyes(self, mouse_x, mouse_y):
        for eye in self.floating_eyes:
            eye.y_position += eye.y_speed
            if eye.y_position > self.height:
                eye.y_position = 0
                eye.eye_globe.center_x = random.randint(int(self.left + 30), int(self.right - 30))

            eye_y = self.bottom + eye.y_position
            eye.eye_globe.center_y = eye_y

            angle = atan2(mouse_y - eye_y, mouse_x - eye.eye_globe.center_x)
            distance = 15 * 0.5
            eye.eye_center.center_x = eye.eye_globe.center_x + cos(angle) * distance
            eye.eye_center.center_y = eye_y + sin(angle) * distance
            eye.pupil.center_x = eye.eye_center.center_x
            eye.pupil.center_y = eye.eye_center.center_y

    def update_arcade_logo_position(self):
        # Position the arcade logo relative to the InfoWindow (blue card)
        self.arcade_logo.center_x = self.center_x - 10
        self.arcade_logo.center_y = self.center_y - 40

    def draw(self):
        super().draw()
        self.floating_eye_globes.draw()
        self.floating_eye_centers.draw()
        self.floating_eye_pupils.draw()
        self.arcade_logo.draw()
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
        self.eye_globe.center_x = self.center_x - 50
        self.eye_globe.center_y = self.center_y + 38

    def update_eye_center_position(self, mouse_x, mouse_y):
        # Calculate the angle between the eye globe center and the mouse pointer
        angle = atan2(mouse_y - self.eye_globe.center_y, mouse_x - self.eye_globe.center_x)
        distance = 15
        self.update_floating_eyes(mouse_x, mouse_y)
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
            self.pupil_scale_target = 1
        elif self.pupil_state == 1:  # Expand
            self.pupil_scale_target = 1.5
        elif self.pupil_state == 2:  # Contract
            self.pupil_scale_target = .8

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
            self.update_arcade_logo_position()
            for eye in self.floating_eyes:
                eye.eye_globe.center_x = random.randint(int(self.left + 30), int(self.right - 30))
                eye.eye_globe.center_y = random.randint(int(self.bottom + 30), int(self.top - 30))
                eye.y_position = eye.eye_globe.center_y - self.bottom


        self.update_floating_eyes(mouse_x, mouse_y)
        # Update the eye center position to follow the mouse pointer
        self.update_eye_center_position(mouse_x, mouse_y)