import pygame
from math import sqrt

class Tower:
    def __init__(self, position):
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class TowerManager:
    def __init__(self, screen, enemy_path):
        self.towers = []  # List of placed towers
        self.the_tower = None  # Tower being placed
        self.enemy_path = enemy_path
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

    def handle_event(self, event) :
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t :
            mouse_position = pygame.mouse.get_pos()
            self.the_tower = Tower(mouse_position)

        elif event.type == pygame.MOUSEBUTTONDOWN and self.the_tower :
            if self.is_tower_placeable(self.the_tower.rect) :
                self.towers.append(self.the_tower.rect)
                self.the_tower = None


    # is the placement valid for this give tower
    def is_tower_placeable(self, tower_rect) :
        for (x,y) in self.enemy_path:
            if self.distance_to_point(tower_rect.center, (x, y)) < 20.0:
                return False

        screen_rect = pygame.Rect(0,0, self.screen_width, self.screen_height)
        return screen_rect.contains(tower_rect)



    # using the distance formula between two points return value
    def distance_to_point(self, pointA, pointB) :
        return sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2 )

    def update(self) :
        if self.the_tower :
            mouse_position = pygame.mouse.get_pos()
            self.the_tower.rect.center = mouse_position

    def render(self, screen) :
        for tower in self.towers :
            tower.draw(screen)

        if self.the_tower:
            self.the_tower.draw(screen)
