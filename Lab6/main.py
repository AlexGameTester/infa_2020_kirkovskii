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


def new_ball(surface, x_range=(100, 1100), y_range=(100, 900), radius_range=(10, 100), velocity_range=(5, 50)):
    """
    Creates new ball with random position, velocity, radius and color
    :param surface: surface to draw on
    :param x_range: tuple of minimal and maximal x coordinates of the center of the ball
    :param y_range: tuple of minimal and maximal y coordinates of the center of the ball
    :param radius_range: tuple of minimal and maximal ball's radius values
    :param velocity_range: tuple of maximal and minimal velocity projection on Ox|Oy axis in pixels per second
    :return: ((x, y, r), (v_x, v_y), color) tuple that contains information about a new ball
    """
    x = randint(*x_range)
    y = randint(*y_range)
    r = randint(*radius_range)
    v_x, v_y = randint(*velocity_range), randint(*velocity_range)
    color = COLORS[randint(0, 5)]
    return (x, y, r), (v_x, v_y), color


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


def on_mouse_down(surface, event, balls):
    """
    Mouse button down event handler
    :param surface: main screen of te app
    :param event: a MOUSEBUTTONDOWN event
    :param balls: list of balls that are on the surface
    """
    for i, (pos, vel, color) in enumerate(balls):
        x, y, r = pos
        if distance(event.pos, (x, y)) <= r:
            on_ball_caught(surface, event, balls, i)


def on_ball_caught(surface, event, balls, ball_index):
    """
    Called when player catches the ball
    :param balls: list of all balls that are on the screen
    :param ball_index: index of a ball in balls that has been caught
    :param surface: surface where the ball was located
    :param event: MOUSEBUTTONDOWN event of catching click
    """
    balls.pop(ball_index)


def move_ball(position, velocity, dt):
    """
    Moves ball with velocity
    :param position: tuple (x, y) of ball's coordinates before motion happens
    :param velocity: (v_x, v_y) tuple that represents velocity vector
    :param dt: time interval of motion
    :return: new position of the ball
    """
    x, y = position
    v_x, v_y = velocity
    return int(x + v_x * dt), int(y + v_y * dt)


def draw_frame(surface, balls, fps):
    """
    Draws next frame on screen
    :type fps: FPS
    :param surface: screen to draw on
    :param balls: a list of balls that are on the surface
    """
    surface.fill(BLACK)
    for i, (pos_and_r, vel, color) in enumerate(balls):
        *pos, r = pos_and_r
        new_pos_x, new_pos_y = move_ball(pos, vel, 1 / fps)
        balls[i] = (new_pos_x, new_pos_y, r), vel, color
        draw.circle(surface, color, (new_pos_x, new_pos_y), r)


def main():
    pg.init()

    # tuple ((x, y, r), (v_x, v_y)) represents a ball
    balls = []

    fps = 30
    screen = pg.display.set_mode((1200, 900))

    pg.display.update()
    clock = pg.time.Clock()
    finished = False

    balls.append(new_ball(screen))

    while not finished:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                on_mouse_down(screen, event, balls)

        draw_frame(screen, balls, fps)
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
