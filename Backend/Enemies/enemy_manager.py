from wave import Wave
import pygame


# Middleman between enemy and game_manager
class EnemyManager:
    def __init__(self, canvas, checkpoints):
        self.wave = Wave(canvas, checkpoints, 5)

    def update(self):
        self.wave.update()

    def render(self, screen):
        self.wave.render(screen)