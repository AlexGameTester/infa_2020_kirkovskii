import pygame as pg
import pygame.draw as draw
from random import randint, random
from math import sin, cos, pi

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
BALLS_NUMBER = 3
FONT = 0

score = 0


def random_vector(magnitude_range):
    """
    Return's vector with magnitude from range [m_min, m_max] and random direction
    :param magnitude_range: tuple (m_min, m_max) of maximal and minimal possible vector magnitudes
    :return: tuple (v_x, v_y) of vector's coordinates
    """
    v = randint(*magnitude_range)
    a = 2 * pi * random()
    return v * cos(a), v * sin(a)


def new_ball(x_range=(100, 1100), y_range=(100, 900), radius_range=(10, 100), velocity_range=(80, 180)):
    """
    Creates new ball with random position, velocity, radius and color
    :param x_range: tuple of minimal and maximal x coordinates of the center of the ball
    :param y_range: tuple of minimal and maximal y coordinates of the center of the ball
    :param radius_range: tuple of minimal and maximal ball's radius values
    :param velocity_range: tuple of maximal and minimal velocity projection on Ox|Oy axis in pixels per second
    :return: ((x, y, r), (v_x, v_y), color) tuple that contains information about a new ball
    """

    x = randint(*x_range)
    y = randint(*y_range)
    r = randint(*radius_range)
    v_x, v_y = random_vector(velocity_range)
    color = COLORS[randint(0, 5)]
    return (x, y, r), (v_x, v_y), color


def new_poly(vertices_range=(3, 8), x_range=(100, 1100), y_range=(100, 900), radius_range=(10, 100),
             velocity_range=(80, 180), acceleration_range=(0, 8)):
    """
    Creates new poly with random number of vertices, position, velocity, acceleration, radius and color and rotation set to 0
    :param acceleration_range: tuple of maximal and minimal acceleration projection on Ox|Oy axis in pixels per second squared
    :param vertices_range: tuple of minimal and maximal numbers of poly's vertices
    :param x_range: tuple of minimal and maximal x coordinates of the center of the poly
    :param y_range: tuple of minimal and maximal y coordinates of the center of the poly
    :param radius_range: tuple of minimal and maximal poly's outer radius values
    :param velocity_range: tuple of maximal and minimal velocity projection on Ox|Oy axis in pixels per second
    :return: dictionary that stores poly's properties
    """

    n = randint(*vertices_range)
    x = randint(*x_range)
    y = randint(*y_range)
    r = randint(*radius_range)
    vel = random_vector(velocity_range)
    acc = random_vector(acceleration_range)
    color = COLORS[randint(0, 5)]
    return {'vertices': n, 'position': (x, y), 'velocity': vel,
            'acceleration': acc, 'rotation': 0, 'radius': r, 'color': color}


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
    global score

    balls.pop(ball_index)
    score += 1
    balls.append(new_ball())


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


def collide_with_wall(position, velocity, radius, border_size):
    """
    Checks if ball collides with a wall and does collision if necessary
    :param position: tuple (x, y) of ball's coordinates
    :param velocity: (v_x, v_y) tuple that represents velocity vector
    :param radius: ball's radius
    :param border_size: (width, height) tuple of border coordinates
    :return:
    """
    width, height = border_size
    x, y = position
    v_x, v_y = velocity
    if (x <= radius and v_x < 0) or (width - x <= radius and v_x > 0):
        v_x = -v_x
    if (y <= radius and v_y < 0) or (height - y <= radius and v_y > 0):
        v_y = -v_y

    return v_x, v_y


def draw_frame(surface, balls, fps):
    """
    Draws next frame on screen
    :type fps: FPS
    :param surface: screen to draw on
    :param balls: a list of balls that are on the surface
    """
    global score

    border_size = surface.get_size()

    surface.fill(BLACK)
    for i, (pos_and_r, vel, color) in enumerate(balls):
        *pos, r = pos_and_r
        new_pos_x, new_pos_y = move_ball(pos, vel, 1 / fps)
        new_vel = collide_with_wall((new_pos_x, new_pos_y), vel, r, border_size)
        balls[i] = (new_pos_x, new_pos_y, r), new_vel, color
        draw.circle(surface, color, (new_pos_x, new_pos_y), r)

    text_surface = FONT.render(str(score), False, WHITE)
    text_position = (30, 10)
    surface.blit(text_surface, text_position)


def main():
    global FONT
    pg.init()
    FONT = pg.font.SysFont("Comic Sans MS", 46)

    fps = 30
    screen = pg.display.set_mode((1200, 900))

    pg.display.update()
    clock = pg.time.Clock()
    finished = False

    # tuple ((x, y, r), (v_x, v_y), color) represents a ball
    balls = [new_ball() for n in range(BALLS_NUMBER)]

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
