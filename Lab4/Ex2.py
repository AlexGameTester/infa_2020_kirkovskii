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


def draw_animal(screen, colors, x, y, size):
    def draw_neck(surface, x, y):
        def draw_head(x, y):
            def draw_horn(x, y):
                horn_verticies = [(x, y), (x - 22, y - 30), (x + 2, y - 6)]
                draw.polygon(surface, colors['white'], horn_verticies)

            def draw_eye(x, y):
                eye_height = 30
                eye_width = 34
                draw.ellipse(surface, colors['eye purple'], (int(x - eye_width/2), int(y - eye_height/2), eye_width, eye_height))
                pupil_radius = 9
                draw.circle(surface, colors['black'], (x + 3, y), pupil_radius)
                flare_start = (x - 7, y - 6)
                flare_end = (x + 1, y - 3)
                draw.line(surface, colors['white'], flare_start, flare_end, 6)

            # draw_horn = lambda x, y: draw.polygon(screen, colors['white'], )
            head_rect = (x, y, 62, 40)
            draw.ellipse(surface, colors['white'], head_rect)
            
            eye_offset_x, eye_offset_y = 28, 18
            draw_eye(x + eye_offset_x, y + eye_offset_y)

            horn_offset_x, horn_offset_y = 5, 12
            horn_delta_y, horn_delta_x = 6, -6
            draw_horn(x + horn_offset_x, y + horn_offset_y)
            draw_horn(x + horn_offset_x + horn_delta_x, y + horn_offset_y + horn_delta_y)

        neck_height = 190
        neck_width = 40
        draw.ellipse(surface, colors['white'], (x, y, neck_width, neck_height))
        # draw_head(x + neck_width // 2, y - neck_height - 8)
        draw_head(x + 2, y - 8)

    def draw_leg(surface, x, y):
        top_height = 70
        top_rect = (x + 0, y + 0, 40, top_height)
        draw.ellipse(surface, colors['white'], top_rect)

        bot_rect = (x - 2, y + top_height - 4, 44, 80)
        draw.ellipse(surface, colors['white'],bot_rect)

        foot_rect = (x + 9, y + 130, 58, 30)
        draw.ellipse(surface, colors['white'], foot_rect)

    surface = pygame.Surface((600, 800))
    surface.fill(colors['flower key color'])

    draw_leg(surface, 65, 435)
    draw_leg(surface, 105, 450)
    draw_leg(surface, 300, 450)
    draw_leg(surface, 335, 430)
    body_rect = (50, 340, 350, 140)
    draw_neck(surface, 345, 240)
    draw.ellipse(surface, colors['white'], body_rect)

    surface = pygame.transform.scale(surface, (int(600 * size), int(800 * size)))
    surface.set_colorkey(colors['flower key color'])
    screen.blit(surface, (x, y))

def draw_bush(screen, colors, x, y, size):
    def get_flower(scale, rotation_angle=0):
        flower = pygame.Surface((400, 400))
        flower.fill(colors['flower key color'])
        # flower.set_colorkey(colors['flower key color'])
        x0 = 200
        y0 = 200

        centre_x = 60
        centre_y = 24
        # draw.ellipse(flower, colors['yellow'], ((x0 - centre_x/2, y0 - centre_y/2), (centre_x, centre_y)))

        number_of_petals = 7
        dist = 20
        petal_x = 58
        petal_dx = 2
        petal_y = 22
        petal_dy = 2
        for angle in [2*math.pi/number_of_petals * n for n in range(number_of_petals)]:
            size_x = petal_x + rand.randint(-petal_dx, petal_dx)
            size_y = petal_y + rand.randint(-petal_dy, petal_dy)
            rect = (int(x0 + dist * math.cos(angle) - size_x/2), int(y0 + dist * math.sin(angle) - size_y/2), size_x, size_y)
            draw.ellipse(flower, colors['white'], rect)
            draw.ellipse(flower, colors['black'], rect, 1)
            angle += 2*math.pi / number_of_petals
        
        draw.ellipse(flower, colors['yellow'], ((x0 - centre_x/2, y0 - centre_y/2), (centre_x, centre_y)))

        flower = pygame.transform.rotozoom(flower, rotation_angle, scale)
        flower.set_colorkey(colors['flower key color'])
        return flower

    test_flower = get_flower(1, 0)
    screen.blit(test_flower, (200, 200))


def draw_scene(screen, colors):
    draw_background(screen, colors)
    draw_animal(screen, colors, 0, 0, 1)
    # draw_bush(screen, colors, 0, 0, 0)


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
    'eye purple': 0xf0aabc
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
