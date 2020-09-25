import pygame
import pygame.draw as draw


def draw_background(screen, colors):
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
        polygon_closing_verticies = [(500, 800), (0, 800)]

        draw.polygon(screen, colors['grass green'],
                     surface_verticies + polygon_closing_verticies)

        draw.aalines(screen, colors['black'], False, surface_verticies)

    draw_mountains()
    draw_surface()


def draw_scene(screen, colors):
    draw_background(screen, colors)


pygame.init()

colors = {
    'yellow': 0xFFFF00,
    'black': 0x0,
    'white': 0xffffff,
    'red': 0xff0000,
    'sky blue': 0xafdde9,
    'grass green': 0xaade87
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
