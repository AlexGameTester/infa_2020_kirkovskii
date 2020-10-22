import pygame as pg
import pygame.draw as draw
import graphics
from random import randint, random
from math import sin, cos, pi, sqrt

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
POLYS_NUMBER = 5
FONT = 0
SCORE_FOR_POLY = 0.5
SCORE_FOR_BALL = 1
STARTING_TIME = 10
TIME_FOR_BALL = 0.4
TIME_FOR_POLY = 0.13

time_left = 0
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


def new_polygon(vertices_range=(3, 8), x_range=(100, 1100), y_range=(100, 900), radius_range=(10, 100),
                velocity_range=(80, 180), acceleration_range=(20, 40), rotation_speed_range=(30, 90)):
    """
    Creates new polygon with random number of vertices, position, velocity,
    acceleration, rotation_speed, radius and color
    and rotation set to 0
    :param acceleration_range: tuple of maximal and minimal acceleration projection on Ox|Oy axis
    in pixels per second squared
    :param vertices_range: tuple of minimal and maximal numbers of polygon's vertices
    :param x_range: tuple of minimal and maximal x coordinates of the center of the polygon
    :param y_range: tuple of minimal and maximal y coordinates of the center of the polygon
    :param radius_range: tuple of minimal and maximal polygon's outer radius values
    :param velocity_range: tuple of maximal and minimal velocity projection on Ox|Oy axis in pixels per second
    :param rotation_speed_range: tuple of maximal and minimal rotation speed absolute value
    :return: dictionary that stores polygon's properties
    """

    n = randint(*vertices_range)
    x = randint(*x_range)
    y = randint(*y_range)
    r = randint(*radius_range)
    vel = random_vector(velocity_range)
    acc = random_vector(acceleration_range)
    rot_speed = (-1)**randint(0, 1) * randint(*rotation_speed_range)
    color = COLORS[randint(0, 5)]
    return {'vertices': n, 'position': (x, y), 'velocity': vel, 'acceleration': acc,
            'rotation': 0, 'rotation_speed': rot_speed, 'radius': r, 'color': color}


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


def on_mouse_down(surface, event, balls, polygons):
    """
    Mouse button down event handler
    :param surface: main screen of te app
    :param event: a MOUSEBUTTONDOWN event
    :param balls: list of balls that are on the surface
    :param polygons: list of polygons that are on the surface
    """
    global score
    objects_caught = 0
    got_score = 0

    for i, (pos, vel, color) in enumerate(balls):
        x, y, r = pos
        if distance(event.pos, (x, y)) <= r:
            got_score += on_ball_caught(surface, event, balls, i)
            objects_caught += 1

    for i, poly in enumerate(polygons):
        poly_pos = poly['position']
        r = poly['radius']
        if distance(event.pos, poly_pos) <= r:
            got_score += on_poly_caught(surface, event, polygons, i)
            objects_caught += 1

    # player gets extra score if he catches more than one object at a time
    score += objects_caught * got_score


def on_poly_caught(surface, event, polygons, poly_index):
    """
    Called when player catches a poly
    :param surface: surface where the poly was located
    :param event: MOUSEBUTTONDOWN event of catching click
    :param polygons: list of all polygons that are on the screen
    :param poly_index: index of the poly in polygons that has been caught
    :return: integer amount of score player has got from this object
    """
    global time_left

    n = polygons[poly_index]['vertices']
    got_score = int(SCORE_FOR_POLY * n)
    time_left += n * TIME_FOR_POLY

    polygons.pop(poly_index)
    polygons.append(new_polygon())

    return got_score


def on_ball_caught(surface, event, balls, ball_index):
    """
    Called when player catches the ball
    :param balls: list of all balls that are on the screen
    :param ball_index: index of a ball in balls that has been caught
    :param surface: surface where the ball was located
    :param event: MOUSEBUTTONDOWN event of catching click
    :return: integer amount of score player has got from this object
    """
    global time_left

    time_left += TIME_FOR_BALL

    balls.pop(ball_index)
    balls.append(new_ball())
    return SCORE_FOR_BALL


def change_vector(vector, vector_changer, dt):
    """
    Adds vector_changer * dt to the vector
    :param vector: tuple (v_x, v_y) that represents a vector to change
    :param vector_changer: tuple (v_x, v_y) that represents a vector that provides changes
    :param dt: time interval
    :return: vector + vector_changer * dt
    """
    x, y = vector
    c_x, c_y = vector_changer
    return x + c_x * dt, y + c_y * dt


def move_object(position, velocity, dt):
    """
    Moves object with velocity
    :param position: tuple (x, y) of object's coordinates before motion happens
    :param velocity: (v_x, v_y) tuple that represents velocity vector
    :param dt: time interval of motion
    :return: new position of the object
    """
    return change_vector(position, velocity, dt)


def accelerate_object(velocity, acceleration, dt):
    """
    Changes object's velocity with acceleration
    :param velocity: (v_x, v_y) tuple that represents velocity vector
    :param acceleration: (a_x, a_y) tuple that represents acceleration
    :param dt: time interval of motion
    :return: new position of the object
    """
    return change_vector(velocity, acceleration, dt)


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


def draw_frame(surface, balls, polygons, fps):
    """
    Draws next frame on screen
    :param surface: screen to draw on
    :param balls: a list of balls that are on the surface
    :param polygons: a list of polygons that are on the surface
    "param fps: FPS
    """
    global score, time_left

    border_size = surface.get_size()
    dt = 1 / fps

    surface.fill(BLACK)

    for i, (pos_and_r, vel, color) in enumerate(balls):
        *pos, r = pos_and_r
        new_pos_x, new_pos_y = move_object(pos, vel, dt)
        new_vel = collide_with_wall((new_pos_x, new_pos_y), vel, r, border_size)
        balls[i] = (new_pos_x, new_pos_y, r), new_vel, color
        int_pos = int(new_pos_x), int(new_pos_y)
        draw.circle(surface, color, int_pos, r)

    for poly in polygons:
        r = poly['radius']
        n = poly['vertices']
        rot_speed = poly['rotation_speed']
        color = poly['color']
        pos = poly['position']
        vel = poly['velocity']
        vel = collide_with_wall(pos, vel, r, border_size)
        acc = poly['acceleration']
        poly['position'] = move_object(pos, vel, dt)
        poly['velocity'] = accelerate_object(vel, acc, dt)
        poly['rotation'] += rot_speed * dt
        int_pos = tuple(map(int, poly['position']))
        graphics.draw_right_poly(surface, color, n, int_pos, r, rotation=poly['rotation'])

    time_left = max(time_left - dt, 0)

    # drawing scores
    score_surface = FONT.render(str(score), False, WHITE)
    score_position = (30, 10)
    surface.blit(score_surface, score_position)

    # drawing timer
    timer_surface = FONT.render('%.2f' % time_left, False, WHITE)
    timer_position = (1050, 10)
    surface.blit(timer_surface, timer_position)


def read_name(screen, fps, clock):
    """
    Reads players name and writes it to leaderboard
    :param screen: main screen of the game
    :param fps: FPS
    :param clock: pygame clock
    """
    def draw_name_frame(surface : pg.Surface, name):
        width, height = surface.get_size()
        message = 'Write your name:'
        message_pos = (width // 2, height // 10 * 4)
        message_surface = FONT.render(message, False, WHITE)

        name_string = ''.join(name)
        name_pos = (width // 2, height // 2)
        name_surface = FONT.render(name_string, False, WHITE)

        surface.fill(BLACK)
        surface.blit(message_surface, message_pos)
        surface.blit(name_surface, name_pos)

    global score
    finished = False

    name = []

    while not finished:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    finished = True
                elif event.key == pg.K_BACKSPACE:
                    if name:
                        name.pop()
                elif event.key == pg.K_RETURN:
                    write_name(''.join(name))
                    finished = True
                else:
                    name.append(event.unicode)

        draw_name_frame(screen, name)
        pg.display.update()


def write_name(name, path=''):
    """
    Writes player's name and score to leaderboard file
    :param name: player's name
    :param path: path to leaderboard file
    """
    print(name)
    pass


def main():
    global FONT, time_left
    pg.init()
    FONT = pg.font.SysFont("Comic Sans MS", 46)

    fps = 50
    screen = pg.display.set_mode((1200, 900))

    pg.display.update()
    clock = pg.time.Clock()
    finished = False
    time_left = STARTING_TIME

    # tuple ((x, y, r), (v_x, v_y), color) represents a ball
    balls = [new_ball() for n in range(BALLS_NUMBER)]

    polygons = [new_polygon() for n in range(POLYS_NUMBER)]

    while not finished and time_left > 0:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                on_mouse_down(screen, event, balls, polygons)

        draw_frame(screen, balls, polygons, fps)
        pg.display.update()

    read_name(screen, fps, clock)

    pg.quit()


if __name__ == "__main__":
    main()
