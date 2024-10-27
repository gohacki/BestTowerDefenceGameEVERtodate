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
        self.enemy_path = self.map_manager.get_checkpoints()

        self.tower_manager = TowerManager(self.screen, self.enemy_path, self)
        self.enemy_manager = EnemyManager(self.screen, self.enemy_path, self)
        self.user_health = 100
        self.currency = 500
        self.font = pygame.font.Font(None, 36)

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
            self.enemy_manager.update()
            self.tower_manager.update()
            # Check for win condition
            if not self.enemy_manager.enemies and self.enemy_manager.spawn_counter >= self.enemy_manager.spawn_target:
                self.state = "win"
            # Check for lose condition (e.g., if user health <= 0)
            if self.user_health <= 0:
                self.state = "lose"

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
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Tower Defense Game", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press Enter to Start", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    def render_win_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    def render_lose_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    def render_ui(self):
        # Display User Health
        health_text = self.font.render(f"Health: {self.user_health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))
        # Display Currency
        currency_text = self.font.render(f"Gold: {self.currency}", True, (255, 255, 0))
        self.screen.blit(currency_text, (10, 50))
        # Display Tower Select Instructions
        instructions = self.font.render("Press '1', '2', '3' to select towers", True, (255, 255, 255))
        self.screen.blit(instructions, (10, self.screen.get_height() - 30))

    def reset_game(self):
        self.state = "start"
        # Reinitialize game variables
        self.user_health = 100
        self.currency = 500
        self.enemy_manager = EnemyManager(self.screen, self.enemy_path, self)
        self.tower_manager = TowerManager(self.screen, self.enemy_path, self)
    

