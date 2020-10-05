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

    screen_size = (794, 1123)
    screen = pygame.display.set_mode(screen_size)
    screen.fill(COLORS['sky blue'])

    draw_mountains(screen, screen_size)
    draw_land(screen, screen_size)
    animal_rect = (
        int(0.12 * screen_size[0]),
        int(0.42 * screen_size[1]),
        int(0.27 * screen_size[0]),
        int(0.3 * screen_size[1]),
    )
    draw_animal(screen, *animal_rect)
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
    return int(r * math.sin(angle) + ox), int(r * math.cos(angle) + oy)


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
    mountains_vertices = [(int(x * size[0]), int(y * size[1])) for x, y in mountains_coeff]
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
    surface_vertices = [(int(x * size[0]), int(y * size[1])) for x, y in surface_coeff]
    draw.polygon(screen, COLORS['grass green'], surface_vertices)
    draw.aalines(screen, COLORS['black'], False, surface_vertices[:-2])


def draw_animal(screen, x, y, width, height, reverse=False):
    """
    Draws animal on screen at x, y coordinates.

    :param screen: pygame Surface object
    :param x: x-coordinate of top left point
    :param y: y-coordinate of top left point
    :param width: full width of animal
    :param height: full height of animal
    :param reverse: if False, animal looks right
    :return: None
    """
    surf = pygame.Surface((width, height))
    surf.set_colorkey(COLORS['black'])

    head_rect = (
        int(0.7 * width),
        height // 22,
        int(0.3 * width),
        int(0.54 * height)
    )
    draw_head(surf, *head_rect)
    legs_xy = (
        (width//10, height//2),
        (int(0.25 * width), int(0.58 * height)),
        (width//2, height//2),
        (int(0.65 * width), int(0.58 * height)),
    )
    for x_, y_, in legs_xy:
        leg_width = width // 6
        leg_height = int(0.38 * height)
        draw_leg(surf, x_, y_, leg_width, leg_height)
    body_rect = (
        0,
        int(0.41 * height),
        6 * width // 7,
        int(0.22 * height),
    )
    draw.ellipse(surf, COLORS['white'], body_rect)

    if reverse:
        surf = pygame.transform.flip(surf, True, False)

    screen.blit(surf, (x, y))


def draw_head(screen, x, y, width, height):
    """
    Draws animal's head and neck on `screen`.

    :param screen: pygame Surface object
    :param x: x-coordinate of top left point of image head
    :param y: y-coordinate of top left point of image head
    :param width: width of head
    :param height: neck and head total height
    :return: none
    """
    # TODO make eye_horn function, draw head, neck
    pass


def draw_leg(screen, x, y, width, height):
    """
    Draws a leg consisting of 2 vertical and 1 horizontal ellipses on pygame Surface.

    :param screen: pygame Surface object
    :param x: x-coordinate of top left point
    :param y: y-coordinate of top left point
    :param width: width of foot
    :param height: full width of 3 pieces
    :return: None
    """
    height0 = int(0.4 * height)
    width0 = int(0.7 * width)
    draw.ellipse(screen, COLORS['white'], (x, y, width0, height0))
    draw.ellipse(screen, COLORS['white'], (x, y + int(0.95*height0), width0, height0))
    draw.ellipse(screen, COLORS['white'],
                 (
                    x + 2,
                    y + int(1.9 * height0),
                    int(0.9 * width),
                    int(0.15 * height),
                 ))


def draw_bush(screen, x, y, scale):
    def get_flower(scale, rotation_angle=0):
        surface = pygame.Surface((400, 400))
        surface.fill(COLORS['flower key color'])
        # flower.set_colorkey(COLORS['flower key color'])
        x0 = 200
        y0 = 200

        centre_x = 60
        centre_y = 24
        draw.ellipse(surface, COLORS['yellow'], ((x0 - centre_x // 2, y0 - centre_y // 2), (centre_x, centre_y)))

        number_of_petals = 7
        dist_x = 36
        dist_y = 22
        petal_x = 48
        petal_dx = 2
        petal_y = 26
        petal_dy = 2
        for angle in [2 * math.pi / number_of_petals * n for n in range(number_of_petals)]:
            size_x = petal_x + rand.randint(-petal_dx, petal_dx)
            size_y = petal_y + rand.randint(-petal_dy, petal_dy)
            rect = (
                int(x0 + dist_x * math.cos(angle) - size_x / 2), int(y0 + dist_y * math.sin(angle) - size_y / 2),
                size_x,
                size_y)
            draw.ellipse(surface, COLORS['white'], rect)
            draw.ellipse(surface, COLORS['black'], rect, 1)
            angle += 2 * math.pi / number_of_petals

        # draw.ellipse(flower, COLORS['yellow'], ((x0 - centre_x/2, y0 - centre_y/2), (centre_x, centre_y)))

        surface = pygame.transform.scale(surface, (int(400 * scale), int(400 * scale)))
        surface.set_colorkey(COLORS['flower key color'])
        return surface

    number_of_flowers = rand.randint(3, 6)

    surface = pygame.Surface((600, 600))
    surface.fill(COLORS['flower key color'])

    bush_radius = 270
    draw.circle(surface, COLORS['bush green'], (300, 300), bush_radius)
    flower_area_radius = bush_radius - 200
    min_size = 0.4

    offset = (200, 200)  # half of flower surface size
    surface.blits(
        [(get_flower(min_size + (1 - min_size) * rand.random()), rand_pos(flower_area_radius, offset)) for i in
         range(number_of_flowers)])

    surface = pygame.transform.scale(surface, (int(600 * scale), int(600 * scale)))
    surface.set_colorkey(COLORS['flower key color'])
    screen.blit(surface, (x, y))


if __name__ == '__main__':
    main()
