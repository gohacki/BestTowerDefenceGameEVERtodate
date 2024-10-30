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

        self.tower_manager = TowerManager(self.screen, self.enemy_path, self, self.map_manager.path_mask)
        self.enemy_manager = EnemyManager(self.screen, self.enemy_path)
        self.user_health = 100
        self.currency = 500
        self.font = pygame.font.Font(None, 36)
        self.create_tower_buttons()
        self.paused = False

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.paused = not self.paused
                return  # Don't process further events when toggling pause
            
        if self.state == "start":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state= "playing"

        elif self.state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # check if a tower button was clicked
                for rect, tower_type in self.tower_buttons:
                    if rect.collidepoint(mouse_pos):
                        self.tower_manager.select_tower(tower_type)
                        return  # exit early to avoid unselecting the tower immediately
            self.tower_manager.handle_event(event)

        elif self.state in ("win", "lose"):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def update(self):
        if self.state == "playing" and not self.paused:
            self.enemy_manager.update()
            self.tower_manager.update()

            enemy_positions = self.enemy_manager.getPositions()
            goal_x, goal_y = self.enemy_path[-1]

            enemies_reached_goal = []

            for pos in enemy_positions:
                enemy_x, enemy_y, enemy_id = pos

                if self.has_enemy_reached_goal(enemy_x, enemy_y, goal_x, goal_y):
                    enemies_reached_goal.append(enemy_id)

            for enemy_id in enemies_reached_goal:
                self.user_health -= 10
                self.enemy_manager.dealDamage(enemy_id, 1000)

            if self.user_health <= 0:
                self.state = "lose"
            elif not self.enemy_manager.enemies and self.enemy_manager.spawn_counter >= self.enemy_manager.spawn_target:
                self.state = "win"

    def render(self):
        if self.state == "start":
            self.render_start_screen()

        elif self.state == "playing":
            self.screen.fill((0, 0, 0))
            self.map_manager.draw_map()
            self.enemy_manager.render(self.screen)
            self.tower_manager.render(self.screen)
            self.render_ui()
            if self.paused:
                self.render_pause_menu()

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

    def render_tower_selection_ui(self):
        for rect, tower_type in self.tower_buttons:

            color = (0, 255, 0) if tower_type == 1 else (0, 0, 255) if tower_type == 2 else (255, 0, 0)
            pygame.draw.rect(self.screen, color, rect)

            tower_label = self.font.render(f"Tower {tower_type}", True, (255, 255, 255))
            label_rect = tower_label.get_rect(center=rect.center)
            self.screen.blit(tower_label, label_rect)

    def create_tower_buttons(self):
        self.button_size = (50, 50)
        margin = 60
        y_position = self.screen.get_height() - self.button_size[1] - margin

        self.tower_buttons = []

        num_buttons = 3
        total_width = num_buttons * self.button_size[0] + (num_buttons - 1) * margin

        start_x = (self.screen.get_width() - total_width) // 2
        for i in range(num_buttons):
            x_position = start_x + i * (self.button_size[0] + margin) - 100
            rect = pygame.Rect(x_position, y_position, *self.button_size)
            self.tower_buttons.append((rect, i + 1))

    def render_pause_menu(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height()))
        font_small = pygame.font.Font(None, 36)
        instructions = font_small.render("Press 'P' to Resume", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, self.screen.get_height() // 2 + 20))

    def render_ui(self):
        # Display health
        health_text = self.font.render(f"Health: {self.user_health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))
        # Display gold
        currency_text = self.font.render(f"Gold: {self.currency}", True, (255, 255, 0))
        self.screen.blit(currency_text, (10, 50))
        
        self.render_tower_selection_ui()

    def has_enemy_reached_goal(self, enemy_x, enemy_y, goal_x, goal_y):
        margin = 5
        if abs(enemy_x - goal_x) <= margin and abs(enemy_y - goal_y) <= margin:
            return True
        return False

    def reset_game(self):
        self.state = "start"
        self.user_health = 100
        self.currency = 500
        self.enemy_manager = EnemyManager(self.screen, self.enemy_path, self)
        self.tower_manager = TowerManager(self.screen, self.enemy_path, self)
    

