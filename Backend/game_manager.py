import pygame
from .Towers.tower import TowerManager
from .Enemies.enemy import EnemyManager
from .Maps.map import MapManager


# Obviously this code does not create a level, so we may want to create the level_manager file too
class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = "playing"

        test_map_name = './Assets/map_one'
        self.map_manager = MapManager(screen, test_map_name)
        enemy_path = self.map_manager.get_checkpoints()

        self.tower_manager = TowerManager(screen, enemy_path)
        self.enemy_manager = EnemyManager(screen, enemy_path)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if self.state == "playing":
            self.tower_manager.handle_event(event)

    def update(self):
        if self.state == "playing":
            # self.enemy_manager.update()
            self.tower_manager.update()

    def render(self):
        self.screen.fill((0, 0, 0))
        if self.state == "playing":
            self.enemy_manager.update()
            self.map_manager.draw_map()
            self.enemy_manager.render(self.screen)
            self.tower_manager.render(self.screen)


        pygame.display.flip()
