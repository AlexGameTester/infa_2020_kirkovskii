import pygame as pg
import pygame.draw as draw
from Lab8.common import GameObject, Vector, Colors


class Cannon(GameObject):
    max_shooting_power = 1.0
    shooting_power_per_second = 0.25
    target_max_velocity = 30
    size = 1 / 20
    y_pos = 100

    def __init__(self, game):
        print("Cannon created")
        height = game.resolution[1]
        self.game = game
        super().__init__(Vector(Cannon.y_pos, height / 2), game)

        self.shooting_power = 0
        self.direction = Vector(1, 0)
        self.is_mouse_down = False

    def update(self, fps):
        x, y = pg.mouse.get_pos()
        self.direction = Vector(x, y).normalize()

    def draw(self, surface):
        width, height = self.game.resolution
        x_center, y_center = self.pos
        rect = (int(x_center - Cannon.size * width / 2), int(y_center - Cannon.size * height / 2),
                int(Cannon.size * width), int(Cannon.size * height))
        draw.rect(surface, Colors.red, rect)

    def on_destroyed(self):
        pass


class Shell(GameObject):
    def update(self, fps):
        pass

    def draw(self, surface):
        pass

    def on_destroyed(self):
        pass