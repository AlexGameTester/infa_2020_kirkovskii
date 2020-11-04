import pygame as pg
from Lab8.common import GameObject, Colors
from Lab8.cannon import Cannon


class Game:
    """
    Class that represents game session and holds it's processes
    """

    def __init__(self, resolution=(1280, 720), fps=50, background=Colors.black):
        pg.init()

        self.resolution = resolution
        self.fps = fps
        self.background = background

        self.screen = pg.display.set_mode(resolution)
        self.clock = pg.time.Clock()
        self.object_pool = []

    def add_object(self, game_object: GameObject):
        self.object_pool.append(game_object)

    def update(self):
        """
        Called once in every frame to update game objects
        """
        for game_object in self.object_pool:
            game_object.update(self.fps)

    def draw(self):
        """
        Called once in every frame to draw game objects
        """
        self.screen.fill(self.background)

        for game_object in self.object_pool:
            game_object.draw(self.screen)

    def on_finished(self):
        """
        Called when the game is finished
        """
        pass

    def start_loop(self):
        """
        Starts game's main loop. Can execute infinitely long
        """
        finished = False

        self.cannon = Cannon(self)

        while not finished:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True
                    self.on_finished()

                self.update()
                self.draw()
                pg.display.update()


def main():
    game = Game()
    game.start_loop()


if __name__ == '__main__':
    main()
