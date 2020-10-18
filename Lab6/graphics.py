import pygame as pg
import pygame.draw as draw
import math


def draw_right_poly(surface, color, n, position, radius, rotation=0):
    """
    Draws right polygon with n vertices
    :param surface: surface to draw on
    :param color: color of the polygon
    :param position: tuple (x,y) of coordinates of center of the polygon
    :param radius: distance from the center of the polygon to any of it's vertices
    :param n: number of sides in polygon
    :param rotation: if rotation is 0, the polygon is symmetrical relative to Oy axis, else it is rotated 'rotation'
    degrees clockwise
    """
    x0, y0 = position

    angle_step = 2 * math.pi / n
    angle0 = math.radians(rotation) - angle_step / 2 # with this minus the symmetry is being kept

    vertices = [
        (int(x0 + radius * math.sin(angle0 + i * angle_step)), int(y0 + radius * math.cos(angle0 + i * angle_step)))
        for i in range(n)]

    draw.polygon(surface, color, vertices)
