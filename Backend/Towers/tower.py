import pygame

class Tower:
    def __init__(self, position):
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class TowerManager:
    def __init__(self, screen):
        self.towers = []  # List of placed towers
        self.selected_tower = None  # Tower being placed