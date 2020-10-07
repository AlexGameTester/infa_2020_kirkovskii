import pygame
import pygame.draw as draw
import math
import random as rand

COLORS = {
    'yellow': 0xFFFF00,
    'black': 0x0,
    'white': 0xffffff,
    'red': 0xff0000,
    'sky blue': 0xafdde9,
    'grass green': 0xaade87,
    'mountain grey': 0xb3b3b3,
    'flower key color': 0xf0f0aa,
    'eye purple': 0xe580ff,
    'bush green': 0x71c837
}


def main():
    """
    Initializes pygame, draws background, animal and bush.

    :return: None
    """
    pygame.init()
    FPS = 60

    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size)
    screen.fill(COLORS['sky blue'])

    draw_mountains(screen, screen_size)
    draw_land(screen, screen_size)
    draw_animal(screen, 0, 0, 0.8)
    draw_bush(screen, 250, 450, 0.45)

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = True
    while finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = False
    pygame.quit()


def rand_pos(r, offset):
    ox, oy = offset
    angle = 2 * math.pi * rand.random()
    return int(r * math.sin(angle)) + ox, int(r * math.cos(angle) + oy)


def draw_mountains(screen, size):
    """
    Draws mountain chain on screen.

    :param screen: pygame Surface object
    :param size: (width, height), tuple with screen's width and height
    :return: None
    """
    mountains_coeff = [
        (0, 0.325),
        (0.18, 0.25),
        (0.26, 0.275),
        (0.5, 1 / 8),
        (0.54, 0.225),
        (0.64, 0.275),
        (0.8, 3 / 16),
        (0.86, 0.225),
        (1, 0.175),
        (1, 1),
        (0, 1),
    ]
    mountains_vertices = [(int(x * size[0]), int(y * size[1]))
                          for x, y in mountains_coeff]
    draw.polygon(screen, COLORS['mountain grey'], mountains_vertices)
    draw.aalines(screen, COLORS['black'], False, mountains_vertices[:-2])


def draw_land(screen, size):
    """
    Draws land on screen.

    :param screen: pygame Surface object
    :param size: (width, height), tuple with screen's width and height
    :return:
    """
    surface_coeff = [
        (0, 31 / 80),
        (0.04, 307 / 800),
        (0.06, 309 / 800),
        (0.09, 63 / 160),
        (0.46, 0.4),
        (0.47, 33 / 80),
        (0.48, 69 / 160),
        (0.488, 0.475),
        (0.496, 39 / 80),
        (0.504, 0.525),
        (0.52, 0.5275),
        (0.56, 419 / 800),
        (1, 0.525),
        (1, 1),
        (0, 1),
    ]
    surface_vertices = [(int(x * size[0]), int(y * size[1]))
                        for x, y in surface_coeff]
    draw.polygon(screen, COLORS['grass green'], surface_vertices)
    draw.aalines(screen, COLORS['black'], False, surface_vertices[:-2])


def draw_animal(screen, x, y, size, reverse=False):
    """
    Draws animal on `screen` pygame Surface object.

    :param screen: pygame Surface object
    :param x: top left x-coordinate of picture
    :param y: top left y-coordinate of picture
    :param size: size of the picture
    :param reverse: Bool, if True animal looks left, either right.
    :return:
    """
    surface = pygame.Surface((600, 800))
    surface.fill(COLORS['flower key color'])

    leg_coord = (
        (90, 435),
        (130, 450),
        (300, 450),
        (335, 430),
    )
    for i, j in leg_coord:
        draw_leg(surface, i, j)
    body_rect = (75, 360, 300, 130)
    draw_head(surface, 345, 240)
    draw.ellipse(surface, COLORS['white'], body_rect)

    if reverse:
        surface = pygame.transform.flip(surface, True, False)

    surface = pygame.transform.scale(
        surface,
        (int(600 * size), int(800 * size))
    )
    surface.set_colorkey(COLORS['flower key color'])
    screen.blit(surface, (x, y))


def draw_head(surface, x, y):
    """
    Draws the head of the animal on `surface`.

    :param surface: pygame Surface object
    :param x: x-coordinate of the head
    :param y: y-coordinate of the head
    :return:
    """

    def draw_horn(x, y):
        """
        Draws horn of the animal.

        :param x: x-coordinate of the horn
        :param y: x-coordinate of the horn
        :return:
        """
        horn_vertices = [(x, y), (x - 22, y - 30), (x + 2, y - 6)]
        draw.polygon(surface, COLORS['white'], horn_vertices)

    def draw_eye(x, y, width, height):
        """
        Draws the eye of the animal.

        :param x: x-coordinate of the eye
        :param y: y-coordinate of the eye
        :param width: width of the eye
        :param height: of the eye
        :return: None
        """
        draw.ellipse(surface, COLORS['eye purple'],
                     (
                         x - width // 2,
                         y - height // 2,
                         width,
                         height
                     ))
        pupil_radius = 9
        draw.circle(surface, COLORS['black'], (x + 3, y), pupil_radius)
        flare_start = (x - 7, y - 6)
        flare_end = (x + 1, y - 3)
        draw.line(surface, COLORS['white'], flare_start, flare_end, 6)

    neck_height = 190
    neck_width = 40
    draw.ellipse(surface, COLORS['white'], (x, y, neck_width, neck_height))

    head_rect = (x, y, 62, 40)
    draw.ellipse(surface, COLORS['white'], head_rect)

    eye_offset_x, eye_offset_y = 28, 18
    draw_eye(x + eye_offset_x, y + eye_offset_y, 34, 30)

    horn_offset_x, horn_offset_y = 5, 12
    horn_delta_y, horn_delta_x = 6, -6
    draw_horn(x + horn_offset_x, y + horn_offset_y)
    draw_horn(
        x + horn_offset_x + horn_delta_x,
        y + horn_offset_y + horn_delta_y
    )


def draw_leg(surface, x, y):
    """
    Draws a leg of the animal consisting from 3 ellipses.

    :param surface: pygame Surface object
    :param x: x-coordinate of picture's left part
    :param y: y-coordinate of picture's top part
    :return: None
    """
    top_height = 70
    rects = (
        (x, y, 40, top_height),
        (x, y + top_height - 4, 44, 80),
        (x, y + 130, 58, 30),
    )
    for rec in rects:
        draw.ellipse(surface, COLORS['white'], rec)


def draw_bush(screen, x, y, scale):
    """
    Draws a bush with flowers on a pygame Surface object.

    :param screen: pygame Surface object
    :param x: x-coordinate of the top left point
    :param y: y-coordinate of the top left point
    :param scale: scaling parameter
    :return: None
    """
    number_of_flowers = rand.randint(3, 6)
    surface = pygame.Surface((600, 600))
    surface.fill(COLORS['flower key color'])

    bush_radius = 270
    draw.circle(surface, COLORS['bush green'], (300, 300), bush_radius)
    flower_area_radius = bush_radius - 200
    min_size = 0.4
    offset = (200, 200)  # half of flower surface size
    for i in range(number_of_flowers):
        flower = get_flower(
            min_size + (1 - min_size) * rand.random(),
            rand.randint(-25, 25)
        )
        pos = rand_pos(flower_area_radius, offset)
        surface.blit(flower, pos)

    surface = pygame.transform.scale(
        surface,
        (int(600 * scale), int(600 * scale))
    )
    surface.set_colorkey(COLORS['flower key color'])
    screen.blit(surface, (x, y))


def get_flower(scale, rotation_angle=0):
    """
    Makes a flower on a pygame Surface object, scales and returns it.

    :param scale: scaling parameter of the flower
    :param rotation_angle: angle, the flower is rotated at.
    :return: pygame Surface object with flower
    """
    surface = pygame.Surface((400, 400))
    surface.fill(COLORS['flower key color'])
    x0 = 200
    y0 = 200

    centre_x = 60
    centre_y = 24

    draw.ellipse(
        surface,
        COLORS['yellow'],
        (
            (x0 - centre_x // 2, y0 - centre_y // 2),
            (centre_x, centre_y)
        )
    )

    number_of_petals = 7
    dist_x, dist_y = 36, 22
    petal_x, petal_y = 48, 26
    petal_dx, petal_dy = 2, 2

    angles = [2 * math.pi / number_of_petals * n
              for n in range(number_of_petals)]
    for angle in angles:
        size_x = petal_x + rand.randint(-petal_dx, petal_dx)
        size_y = petal_y + rand.randint(-petal_dy, petal_dy)
        rect = (
            int(x0 + dist_x * math.cos(angle) - size_x / 2),
            int(y0 + dist_y * math.sin(angle) - size_y / 2),
            size_x,
            size_y
        )
        draw.ellipse(surface, COLORS['white'], rect)
        draw.ellipse(surface, COLORS['black'], rect, 1)
        angle += 2 * math.pi / number_of_petals

    surface = pygame.transform.scale(
        surface,
        (int(400 * scale), int(400 * scale))
    )
    surface.set_colorkey(COLORS['flower key color'])
    surface = pygame.transform.rotate(surface, rotation_angle)
    return surface


if __name__ == '__main__':
    main()
