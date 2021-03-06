import math
import random
import itertools
import pygame as pg

from common import GameObject, Colors, Vector, PhysicalObject
from cannon import Cannon
from enemy import Enemy
from scoreboard import Scoreboard
from tank import Tank


class Game:
    """
    Class that represents game session and holds it's processes
    """
    min_enemies = 2
    max_enemies = 6

    def __init__(self, resolution=(1280, 720), fps=50, background=Colors.black):
        pg.init()

        self.resolution = resolution
        self.fps = fps
        self.dt = 1 / fps
        self.background = background

        width, height = resolution
        self._x_border = (0, width)
        self._y_border = (0.1 * height, height)

        self.screen = pg.display.set_mode(resolution)
        self.clock = pg.time.Clock()

        self.object_pool = []
        self.physical_pool = []
        self.event_listeners = {}

        self.scoreboard = Scoreboard(self)

    def add_object(self, game_object: GameObject):
        """
        Adds new game object to pool. This object is updated and drawn in every frame
        :param game_object: an object to add
        """
        self.object_pool.append(game_object)

    def destroy_object(self, game_object: GameObject):
        """
        Tries to destroy a game object
        :param game_object: an object to destroy
        :return: if the object was destroyed
        """
        try:
            self.object_pool.remove(game_object)
            return True
        except ValueError:
            return False

    def add_physical(self, physical_object: PhysicalObject):
        """
        Adds new physical object to pool. Collision of this object with other physical objects is checked every frame
        :param physical_object: an object to add
        """
        self.physical_pool.append(physical_object)

    def destroy_physical(self, physical_object: PhysicalObject):
        """
        Tries to destroy a physical object
        :param physical_object: an object to destroy
        :return: if the object was destroyed
        """
        try:
            self.physical_pool.remove(physical_object)
            return True
        except ValueError:
            return False

    def subscribe_to_event(self, event_type, listener):
        """
        Subscribes a listener function to event so it is called when event happens
        :param event_type: event.type value of an event to listen
        :param listener: (event) -> None event listener function
        """
        if event_type in self.event_listeners.keys():
            self.event_listeners[event_type].append(listener)
        else:
            self.event_listeners[event_type] = [listener]

    def _collide_with_border(self, physical_object):
        """
        Checks and performs collision with border if necessary
        :param physical_object: an object to check
        :param energy_conserved: how much kinetic energy is conserved during collision
        """
        x, y = physical_object.pos
        min_x, max_x = self._x_border
        min_y, max_y = self._y_border
        speed = physical_object.velocity.magnitude()
        direction = physical_object.velocity.normalize()
        radius = physical_object.radius
        collided = False

        if (x <= min_x + radius and direction.x < 0) or (x >= max_x - radius and direction.x > 0):
            speed = math.sqrt(physical_object.energy_conserved * speed**2)
            direction = Vector(-direction.x, direction.y)
            physical_object.velocity = direction * speed
            collided = True

        if (y <= min_y + radius and direction.y < 0) or (y >= max_y - radius and direction.y > 0):
            if not collided:
                speed = math.sqrt(physical_object.energy_conserved * speed ** 2)
            direction = Vector(direction.x, -direction.y)
            physical_object.velocity = direction * speed

    def update_physics(self):
        """
        Called once in every frame to check collisions
        """
        for ph_object in self.physical_pool:
            if ph_object.collides_with_borders:
                self._collide_with_border(ph_object)
        for object1, object2 in itertools.combinations(self.physical_pool, 2):
            if object1.check_collision(object2):
                if object1.on_collision(object2):
                    object2.on_collision(object1)

    def update(self):
        """
        Called once in every frame to update game objects
        """
        self.update_physics()

        for game_object in self.object_pool:
            game_object.update()

    def draw(self):
        """
        Called once in every frame to draw game objects
        """
        self.screen.fill(self.background)

        for game_object in self.object_pool:
            game_object.draw(self.screen)

    def spawn_enemies(self):
        number = random.randint(Game.min_enemies, Game.max_enemies + 1)
        self.enemies = [Enemy(Vector(200, 200), self) for i in range(number)]

    def on_finished(self):
        """
        Called when the game is finished
        """
        pass

    def start_loop(self):
        """
        Starts game's main loop. Can execute infinitely long
        """
        def do_loop():
            self.update()
            self.draw()
            pg.display.update()

        finished = False

        self._tank = Tank(self)
        self.spawn_enemies()

        while not finished:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type in self.event_listeners:
                    for listener in self.event_listeners[event.type]:
                        listener(event)
                if event.type == pg.QUIT:
                    finished = True
                    self.on_finished()

            do_loop()


def main():
    game = Game()
    game.start_loop()


if __name__ == '__main__':
    main()
