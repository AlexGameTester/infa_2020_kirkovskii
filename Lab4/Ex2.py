import pygame
import pygame.draw as draw
import math
import random as rand


def draw_background(screen, colors):
    polygon_closing_verticies = [(500, 800), (0, 800)]

    def draw_mountains():
        mountains_verticies = [
            (0, 260),
            (90, 200),
            (130, 220),
            (250, 100),
            (270, 180),
            (320, 220),
            (400, 150),
            (430, 180),
            (500, 140)
        ]

        draw.polygon(screen, colors['mountain grey'], mountains_verticies + polygon_closing_verticies)

        draw.aalines(screen, colors['black'], False, mountains_verticies)

    def draw_surface():
        surface_verticies = [
            (0, 310),
            (20, 307),
            (30, 309),
            (45, 315),
            (230, 320),
            (235, 330),
            (240, 345),
            (244, 380),
            (248, 390),
            (252, 420),
            (260, 422),
            (280, 419),
            (500, 420),
        ]

        draw.polygon(screen, colors['grass green'],
                     surface_verticies + polygon_closing_verticies)
        draw.aalines(screen, colors['black'], False, surface_verticies)

    draw_mountains()
    draw_surface()


def draw_bush(screen, colors, x, y, size):
    def get_flower(scale, rotation_angle=0):
        flower = pygame.Surface((400, 400))
        flower.fill(colors['flower key color'])
        # flower.set_colorkey(colors['flower key color'])
        x0 = 100
        y0 = 100

        centre_x = 20
        centre_y = 8
        draw.ellipse(flower, colors['yellow'], ((x0 - centre_x/2, y0 - centre_y/2), (centre_x, centre_y)))

        number_of_petals = 7
        dist = 4
        petal_x = 22
        petal_dx = 2
        petal_y = 10
        petal_dy = 2
        for angle in [2*math.pi/number_of_petals * n for n in range(number_of_petals)]:
            size_x = petal_x + rand.randint(-petal_dx, petal_dx)
            size_y = petal_y + rand.randint(-petal_dy, petal_dy)
            rect = (int(x0 + (dist + size_x/2) * math.cos(angle)), int(y0 + (dist + size_y/2) * math.sin(angle)), centre_x, centre_y)
            draw.ellipse(flower, colors['white'], rect)
            draw.ellipse(flower, colors['black'], rect, 1)
            angle += 2*math.pi / number_of_petals
        
        flower = pygame.transform.rotozoom(flower, rotation_angle, scale)
        flower.set_colorkey(colors['flower key color'])
        return flower

    test_flower = get_flower(1, 0)
    screen.blit(test_flower, (200, 200))







def draw_scene(screen, colors):
    draw_background(screen, colors)
    draw_bush(screen, colors, 0, 0, 0)


pygame.init()

colors = {
    'yellow': 0xFFFF00,
    'black': 0x0,
    'white': 0xffffff,
    'red': 0xff0000,
    'sky blue': 0xafdde9,
    'grass green': 0xaade87,
    'mountain grey': 0x338293, # TODO: Set appropriate color
    'flower key color': 0xf0f0aa,
}
FPS = 60
screen_size = (500, 800)
screen = pygame.display.set_mode(screen_size)
screen.fill(colors['sky blue'])

draw_scene(screen, colors)
pygame.display.update()
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
