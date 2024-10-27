import pygame
from .Towers.tower import TowerManager
from .Enemies.enemy_manager import EnemyManager
from .Maps.map import MapManager


# Obviously this code does not create a level, so we may want to create the level_manager file too
class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = "start"

        test_map_name = './Assets/map_one'
        self.map_manager = MapManager(screen, test_map_name)
        enemy_path = self.map_manager.get_checkpoints()

        self.tower_manager = TowerManager(screen, enemy_path)
        self.enemy_manager = EnemyManager(screen, enemy_path)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if self.state == "start":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state= "playing"

        elif self.state == "playing":
            self.tower_manager.handle_event(event)

        elif self.state in ("win", "lose"):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def update(self):
        if self.state == "playing":
            # self.enemy_manager.update()
            self.tower_manager.update()

    def render(self):
        if self.state == "start":
            self.render_start_screen()

        elif self.state == "playing":
            self.screen.fill((0, 0, 0))
            self.enemy_manager.update()
            self.map_manager.draw_map()
            self.enemy_manager.render(self.screen)
            self.tower_manager.render(self.screen)
            self.render_ui()

        elif self.state == "win":
            self.render_win_screen()

        elif self.state == "lose":
            self.render_lose_screen()


        pygame.display.flip()

    def render_start_screen(self):

