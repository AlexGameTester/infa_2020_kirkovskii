import pygame as pg
import pygame.draw as draw
from random import randint

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball(surface, x_range=(100, 1100), y_range=(100, 900), radius_range=(10, 100)):
    """
    Draws new ball with random position, color and radius
    :param surface: surface to draw on
    :param x_range: tuple of minimal and maximal x coordinates of the center of the ball
    :param y_range: tuple of minimal and maximal y coordinates of the center of the ball
    :param radius_range: tuple of minimal and maximal ball's radius values
    """
    global x, y, r
    x = randint(*x_range)
    y = randint(*y_range)
    r = randint(*radius_range)
    color = COLORS[randint(0, 5)]
    draw.circle(surface, color, (x, y), r)


def distance(p1, p2):
    """
    Calculates distance between to points
    :param p1: tuple (x, y) of point 1 coordinates
    :param p2: tuple (x, y) of point 2 coordinates
    :return: float positive distance
    """
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def on_mouse_down(surface, event):
    """
    Mouse button down event handler
    :param surface: main screen of te app
    :param event: a MOUSEBUTTONDOWN event
    """
    x_mouse, y_mouse = event.pos
    print("You got it" if (distance((x_mouse, y_mouse), (x, y)) <= r) else "Try again")


def draw_frame(screen):
    """
    Draws next frame on screen
    :param screen: screen to draw on
    """
    pass


def main():
    pg.init()

    fps = 30
    screen = pg.display.set_mode((1200, 900))

    pg.display.update()
    clock = pg.time.Clock()
    finished = False

    new_ball(screen)

    while not finished:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                on_mouse_down(screen, event)

            draw_frame(screen)
            pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
