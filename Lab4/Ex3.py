import pygame
from Ex2 import COLORS
from Ex2 import draw_mountains, draw_land
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

    draw_bush(screen, 40, 340, 0.3)
    draw_bush(screen, 180, 410, 0.25)
    draw_bush(screen, 300, 450, 0.4)
    draw_bush(screen, 220, 430, 0.15)

    draw_animal(screen, 0, 300, 0.7)
    draw_animal(screen, 0, 120, 0.4)
    draw_animal(screen, 200, 400, 0.5, True)

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
