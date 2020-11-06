from Lab8.cannon import Cannon
import pygame as pg
import pygame.draw as draw

from Lab8.common import Vector, Colors


class Tank(Cannon):
    """
    Represents a moving tank that can shoot different types of projectiles
    """
    motion_keys = {pg.K_a: (-1), pg.K_d: 1}
    motion_zone_border = (1 / 10, 9 / 10)
    speed = 200
    y_pos = 6 / 7
    x_pos = 1 / 2
    x_size = 1 / 12
    y_size = 1 / 15

    def __init__(self, game):
        width, height = game.resolution
        super().__init__(Vector(Tank.x_pos * width, Tank.y_pos * height), game)

        game.subscribe_to_event(pg.KEYDOWN, self._keydown_listener)
        game.subscribe_to_event(pg.KEYUP, self._keyup_listener)

        self.motion_direction = 0

    def draw(self, surface):
        width, height = self.game.resolution
        size_vector = Vector(Tank.x_size * width, Tank.y_size * width)
        rect = (self.pos - size_vector * 0.5).int_tuple(), size_vector.int_tuple()
        
        draw.rect(surface, Colors.white, rect)
        super().draw(surface)

    def update(self):
        super().update()

        motion_zone_start, motion_zone_finish = Tank.motion_zone_border
        width, height = self.game.resolution

        if (motion_zone_start * width < self.pos.x or self.motion_direction == 1) \
                and (self.pos.x < motion_zone_finish * width or self.motion_direction == -1):
            self.pos += Vector.i() * self.motion_direction * Tank.speed * self.game.dt

    def _keydown_listener(self, event):
        """
        KEYDOWN event listener
        :param event: an event object
        """
        if self.motion_direction == 0 and event.key in Tank.motion_keys:
            self.motion_direction = Tank.motion_keys[event.key]

    def _keyup_listener(self, event):
        """
        KEYUP event listener
        :param event: an event object
        """
        if event.key in Tank.motion_keys:
            self.motion_direction = 0