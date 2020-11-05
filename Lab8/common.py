from abc import ABC, abstractmethod
import cmath
import random


class Colors:
    """
    Class that contains basic colors
    """
    black = (0, 0, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)


class Vector:
    """
    Class that represents planar vector with it's common operations
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._iter_counter = 0

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if not isinstance(other, float) and not isinstance(other, int):
            raise TypeError('other must be int or float but received', type(other))

        return Vector(self.x * other, self.y * other)

    def __iter__(self):
        return [self.x, self.y].__iter__()

    def __sub__(self, other):
        return self + (other * (-1))

    def magnitude(self):
        """
        Returns magnitude of the vector
        :return: float magnitude of vector
        """
        return (self.x ** 2 + self.y ** 2) ** (1 / 2)

    def normalize(self):
        """
        Returns normalized vector
        :return: Normalized vector - vector with the same direction as this one and magnitude of 1
        """
        magn = self.magnitude()
        return self * (1 / magn)

    def rotate(self, angle):
        """
        Rotates vector counterclockwise
        :param angle: angle to rotate
        :return: rotated vector
        """
        c_repr = self.x + 1j * self.y
        new_c_repr = c_repr * cmath.exp(1j * angle)
        return Vector(new_c_repr.real, new_c_repr.imag)

    def int_tuple(self):
        """
        Converts the vector into tuple of 2 integers
        :return: tuple of 2 integers
        """
        return int(self.x), int(self.y)

    @staticmethod
    def random_vector(magnitude_range, angle_range=(0, 2 * cmath.pi)):
        """
        Creates random vector
        :param magnitude_range: tuple of (min magnitude, max magnitude) of created vector
        :param angle_range: tuple of (min angle, max angle) in radians of created vector. Angle 0 corresponds
        to vector forwarded in positive Ox direction
        :return: random vector
        """
        min_magn, max_magn = magnitude_range
        min_angle, max_angle = angle_range
        magnitude = min_magn + random.random() * (max_magn - min_magn)
        angle = min_angle + random.random() * (max_angle - min_angle)
        return Vector(magnitude, 0).rotate(angle)

    @staticmethod
    def i():
        """
        Ox unit vector
        :return: Ox unit vector
        """
        return Vector(1, 0)

    @staticmethod
    def j():
        """
        Oy unit vector
        :return: Oy unit vector
        """
        return Vector(0, 1)


class GameObject(ABC):
    """
    Represents an abstract game object with it's default properties and methods
    """

    def __init__(self, pos: Vector, game):
        """
        GameObject constructor
        :param pos: position of object(not on screen but in fixed coordinate system of a game)
        :param game: Game class object which contains this GameObject
        """
        self.pos = pos
        self.game = game

        self.is_alive = True

        game.add_object(self)

    @abstractmethod
    def update(self):
        """
        Called once in every frame when updating of objects occur
        :return: None
        """
        pass

    @abstractmethod
    def draw(self, surface):
        """
        Called once in every frame to draw object on surface
        :param surface: surface to draw on
        :return: None
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        Called to destroy this object
        :return: None
        """
        self.game.destroy_object(self)


class PhysicalObject(GameObject, ABC):
    def __init__(self, pos, game, velocity, radius):
        super().__init__(pos, game)

        game.add_physical(self)

        self.velocity = velocity
        self.radius = radius

    @abstractmethod
    def check_collision(self, other):
        """
        Returns if this object collides with other
        :param other: other physical object
        :return: True if collides, False otherwise
        """
        return (self.pos - other.pos).magnitude() <= self.radius + other.radius

    @abstractmethod
    def on_collision(self, other):
        """
        Called when this object collides with other
        :param other: an object that collided with this one
        :return: True if other.on_collision should also be called, False otherwise
        """
        return True

    def destroy(self):
        super().destroy()

        self.game.destroy_physical(self)


