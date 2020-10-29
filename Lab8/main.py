import pygame as pg


class Game:

    def __init__(self, resolution=(1280, 720), fps=50):
        pg.init()

        self.resolution = resolution
        self.fps = fps
        self.screen = pg.display.set_mode(resolution)
        self.clock = pg.time.Clock()

    def update(self):
        pass

    def on_finished(self):
        pass

    def start_loop(self):
        finished = False

        while not finished:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True
                    self.on_finished()

                self.update()


def main():
    game = Game()
    game.start_loop()


if __name__ == '__main__':
    main()
