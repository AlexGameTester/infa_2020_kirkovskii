import pygame as pg
import pygame.draw as draw
from Lab8.common import GameObject, Vector, Colors


class Cannon(GameObject):
    """
    Represents a stationary cannon that can shoot projectiles
    """
    max_shooting_power = 1.0
    shooting_power_per_second = 0.25
    target_max_velocity = 30
    line_width = 20
    line_length = 150
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
        self.direction = (Vector(x, y) - self.pos).normalize()

    def draw(self, surface):
        start_pos = tuple(self.pos)
        end_pos = tuple(self.pos + self.direction * Cannon.line_length)

        draw.line(surface, Colors.red, start_pos, end_pos, Cannon.line_width)

    def on_destroyed(self):
        pass


class Shell(GameObject):
    def update(self, fps):
        pass

    def draw(self, surface):
        pass

    def on_destroyed(self):
        pass