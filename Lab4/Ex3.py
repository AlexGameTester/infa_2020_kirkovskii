import pygame
from Ex2 import COLORS
from Ex2 import draw_mountains
from Ex2 import draw_land
from Ex2 import draw_animal
from Ex2 import draw_bush


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

    bush_params = (
        (40, 340, 0.3),
        (180, 410, 0.25),
        (400, 450, 0.4),
        (300, 340, 0.15),
    )
    for param in bush_params:
        draw_bush(screen, *param)

    animal_params = (
        (0, 300, 0.7, False),
        (0, 120, 0.4, False),
        (500, 400, 0.5, True),
    )
    for param in animal_params:
        draw_animal(screen, *param)

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = True
    while finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = False
    pygame.quit()


if __name__ == '__main__':
    main()
