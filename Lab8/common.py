from abc import ABC, abstractmethod
import cmath


class Colors:
    """
    Class that contains basic colors
    """
    black = (0, 0, 0)
    red = (255, 0, 0)


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
        self.is_alive = True
        game.add_object(self)

    @abstractmethod
    def update(self, fps):
        """
        Called once in every frame when updating of objects occur
        :param fps: FPS
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
    def on_destroyed(self):
        """
        Called when object is destroyed
        :return: None
        """
        pass
