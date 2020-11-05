import random

import pygame as pg
from Lab8.common import GameObject, Colors, Vector
from Lab8.cannon import Cannon
from Lab8.enemy import Enemy


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

        self.screen = pg.display.set_mode(resolution)
        self.clock = pg.time.Clock()
        self.object_pool = []
        self.event_listeners = {}

    def add_object(self, game_object: GameObject):
        """
        Adds new game object to pool. This object is updated and drawn in every frame
        :param game_object: an object to add
        """
        self.object_pool.append(game_object)

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

    def update(self):
        """
        Called once in every frame to update game objects
        """
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

        self._cannon = Cannon(self)
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
