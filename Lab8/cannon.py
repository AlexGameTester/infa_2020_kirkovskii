import pygame as pg
import pygame.draw as draw
from Lab8.common import GameObject, Vector, Colors, PhysicalObject
from Lab8.enemy import Enemy


class Cannon(GameObject):
    """
    Represents a stationary cannon that can shoot projectiles
    """
    max_shooting_power = 1.0
    shooting_power_per_second = 0.35
    projectile_max_velocity = 500
    projectile_min_velocity = 50
    line_width = 20
    line_length = 150

    def __init__(self, pos, game):
        super().__init__(pos, game)

        game.subscribe_to_event(pg.MOUSEBUTTONDOWN, self._mousebuttondown_listener)
        game.subscribe_to_event(pg.MOUSEBUTTONUP, self._mousebuttonup_listener)

        self.shooting_power = 0
        self.direction = Vector(1, 0)
        self.is_mouse_down = False
        self._projectiles = []

    def update(self):
        x, y = pg.mouse.get_pos()
        self.direction = (Vector(x, y) - self.pos).normalize()

        if self.is_mouse_down:
            self.shooting_power = min(self.shooting_power + Cannon.shooting_power_per_second * self.game.dt,
                                      Cannon.max_shooting_power)

    def draw(self, surface):
        start_pos = self.pos.int_tuple()
        end_pos = (self.pos + self.direction * Cannon.line_length).int_tuple()

        draw.line(surface, Colors.red, start_pos, end_pos, Cannon.line_width)

        if self.is_mouse_down:
            end_pos = (self.pos + self.direction * Cannon.line_length * max(self.shooting_power, 0.03)).int_tuple()
            # line is drawn incorrectly when it's length is 0 so an indent of 0.03 added

            draw.line(surface, Colors.white, start_pos, end_pos, Cannon.line_width)

    def destroy(self):
        super().destroy()

    def _mousebuttondown_listener(self, event: pg.event.Event):
        """
        MOUSEBUTTONDOWN event listener
        :param event: an event object
        """
        self.is_mouse_down = True
        self.shooting_power = 0

    def _mousebuttonup_listener(self, event: pg.event.Event):
        """
        MOUSEBUTTONUP event listener
        :param event: an event object
        """
        self.is_mouse_down = False
        self.shoot()
        self.shooting_power = 0

    def shoot(self):
        """
        Shoots a projectile
        """
        projectile_pos = self.pos + self.direction * Cannon.line_length
        projectile_velocity = self.direction * (Cannon.projectile_min_velocity + (Cannon.projectile_max_velocity - Cannon.projectile_min_velocity) * self.shooting_power)
        self._projectiles.append(Projectile(projectile_pos, projectile_velocity, self.game, self))

        self.game.scoreboard.projectile_shot()


class Projectile(PhysicalObject):
    """
    Represents basic projectile that is shot by a cannon and can damage enemies
    """
    gravitational_acceleration = Vector.j() * 20
    air_resistance_coefficient = 0.02
    max_radius = 10

    def __init__(self, pos, velocity, game, cannon):
        super().__init__(pos, game, velocity, Projectile.max_radius)

        self.cannon = cannon

    def update(self):
        dt = self.game.dt

        self.pos += self.velocity * dt
        self.velocity += (Projectile.gravitational_acceleration
                          - self.velocity * Projectile.air_resistance_coefficient) * dt

    def draw(self, surface):
        draw.circle(surface, Colors.white, self.pos.int_tuple(), Projectile.max_radius)

    def destroy(self):
        super().destroy()

    def check_collision(self, other):
        return super().check_collision(other)

    def on_collision(self, other):
        if isinstance(other, Enemy):
            other.destroy()
            self.destroy()
            self.game.scoreboard.enemy_destroyed()

        return True
