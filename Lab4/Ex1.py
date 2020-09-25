import pygame
import pygame.draw as draw


def draw_scene(screen, colors, size):
    def draw_eye(pos, radius, inner_radius):
        draw.circle(screen, colors['red'], pos, radius)
        draw.circle(screen, colors['black'], pos, radius, 1)
        draw.circle(screen, colors['black'], pos, inner_radius)

    head_radius = 270
    head_pos = (size // 2, size // 2)
    draw.circle(screen, colors['yellow'], head_pos, head_radius, 0)
    draw.circle(screen, colors['black'], head_pos, head_radius, 1)

    eye_inner_radius = 24
    eyes_distance = 244
    eye_height = 230

    eye_1_pos = (size // 2 - eyes_distance // 2, eye_height)
    eye_1_radius = 54
    draw_eye(eye_1_pos, eye_1_radius, eye_inner_radius)

    eye_2_pos = (size // 2 + eyes_distance // 2, eye_height)
    eye_2_radius = 44
    draw_eye(eye_2_pos, eye_2_radius, eye_inner_radius)

    eyebrow_width = 28

    eyebrow_1_start = (40, 100)
    eyebrow_1_end = (235, 195)
    draw.line(screen, colors['black'], eyebrow_1_start,
              eyebrow_1_end, eyebrow_width)

    eyebrow_2_start = (540, 130)
    eyebrow_2_end = (370, 195)
    draw.line(screen, colors['black'], eyebrow_2_start,
              eyebrow_2_end, eyebrow_width)

    mouth_size = (300, 50)
    mouth_pos = (size // 2 - mouth_size[0] // 2, size // 2 + 100)
    draw.rect(screen, colors['black'], (mouth_pos, mouth_size))


pygame.init()

colors = {
    'yellow': 0xFFFF00,
    'black': 0x0,
    'white': 0xffffff,
    'red': 0xff0000,
}
FPS = 60
screen_size = 600
screen = pygame.display.set_mode((screen_size, screen_size))
screen.fill(colors['white'])

draw_scene(screen, colors, screen_size)
pygame.display.update()
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
