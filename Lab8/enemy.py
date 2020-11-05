from Lab8.common import GameObject, Vector, Colors
import pygame.draw as draw
import random


class Enemy(GameObject):
    velocity_range = (30, 100)
    velocity_time_min = 0.5
    velocity_time_max = 2.5

    @staticmethod
    def _random_velocity_time():
        """
        Returns random time till velocity must be changed
        :return: float time
        """
        return Enemy.velocity_time_min + (Enemy.velocity_time_max - Enemy.velocity_time_min) * random.random()

    @staticmethod
    def _random_velocity():
        """
        Returns random velocity
        :return: random velocity vector
        """
        return Vector.random_vector(Enemy.velocity_range)

    def __init__(self, pos: Vector, game):
        super().__init__(pos, game)

        self.radius = 25

        self.velocity = Enemy._random_velocity()
        self.till_velocity_changed = Enemy._random_velocity_time()

    def update(self):
        dt = self.game.dt
        self.pos += self.velocity * dt

        self.till_velocity_changed -= dt
        if self.till_velocity_changed <= 0:
            self.velocity = Enemy._random_velocity()
            self.till_velocity_changed = Enemy._random_velocity_time()

    def draw(self, surface):
        draw.circle(surface, Colors.white, self.pos.int_tuple(), self.radius)

    def on_destroyed(self):
        pass