from common import GameObject, Vector
import pygame.draw as draw
import pygame as pg


class Scoreboard(GameObject):
    """
    Represents a scoreboard that counts different statistics and shows it on screen
    """
    x_pos = 1 / 10
    y_pos = 1 / 5
    # font = pg.font.SysFont('Calibri', 22)

    def __init__(self, game):
        width, height = game.resolution
        super().__init__(Vector(Scoreboard.x_pos * width, Scoreboard.y_pos * height), game)

        self.scoreboard = {'projectiles_shot': 0, 'enemies_destroyed': 0, 'score': 0}

    def projectile_shot(self):
        """
        Called when cannon shots a projectile
        """
        self.scoreboard['projectiles_shot'] += 1

    def enemy_destroyed(self):
        """
        Called when an enemy is destroyed
        """
        self.scoreboard['enemies_destroyed'] += 1

    def update(self):
        pass

    def draw(self, surface):
        pass

    def destroy(self):
        pass

