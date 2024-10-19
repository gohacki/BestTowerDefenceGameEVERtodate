import pygame
import random

class Map:
    def __init__(self, path, bg_image):
        # the path is defined as a set of boxed checkpoints which are lists of 4 integers the first two represent the
        # min and max x values respectively and the second two represent the min and max y values respectively
        self.path = [[]]
        self.back_ground = pygame.image.load(bg_image).convert()
    def get_checkpoints(self):
        checkpoints = [[]]
        for checkpoint in self.path:
            x = random.randint(checkpoint[1], checkpoint[2])
            y = random.randint(checkpoint[3], checkpoint[4])
            coords = (x, y)
            checkpoints.append(coords)
        return tuple(checkpoints)

    def draw_map(self):
