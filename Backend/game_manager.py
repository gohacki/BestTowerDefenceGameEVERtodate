# File: Backend/game_manager.py

import pygame
from .Towers.tower_manager import TowerManager
from .Enemies.enemy_manager import EnemyManager
from .Maps.map import MapManager
from .UI.ui_manager import UIManager  # Import the UIManager

ENEMY_KILL_VALUE = 20


# TODO Obviously this code does not create a level, so we may want to create the level_manager file too

# Main class to handle each of the game states and potential interactions
class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = "start"

        # Initialize UIManager
        self.ui_manager = UIManager(screen)

        # load the game map, and get the checkpoints of given display
        test_map_name = './Assets/map_one'
        self.map_manager = MapManager(screen, test_map_name)
        self.enemy_path = self.map_manager.get_checkpoints()

        # initialize the towers and game values that will be displayed
        self.tower_manager = TowerManager(self.screen, self.enemy_path, self, self.map_manager.path_mask)
        self.enemy_manager = EnemyManager(self.screen, self.enemy_path)
        self.user_health = 100
        self.currency = 1000

        # initialize pause state
        self.paused = False

        self.selected_tower = None  # selected tower for upgrades

    # Handle possible user inputs and call to each state of game play
    def handle_events(self, event):
        # if user wishes to quit exit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if user wishes to pause game they can type "p"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.paused = not self.paused
                return  # Don't process further events when toggling pause

        if self.state == "start":
            # if in start screen and user presses enter it will change to playing state
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = "playing"

        elif self.state == "playing":
            # if user pushes the mouse while in the playing state
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check if pause button was clicked
                if self.ui_manager.pause_button_rect.collidepoint(mouse_pos):
                    self.paused = not self.paused
                    return

                # if any tower is selected and then upgrade button is clicked
                if self.selected_tower:
                    for path, button_rect in self.ui_manager.upgrade_buttons.items():
                        if button_rect.collidepoint(mouse_pos):
                            self.handle_upgrade_purchase(path)
                            return

                # check if a tower button was clicked, select it for placement
                for rect, tower_type in self.ui_manager.tower_buttons:
                    if rect.collidepoint(mouse_pos):
                        self.tower_manager.select_tower(tower_type)
                        return  # exit early to avoid unselecting the tower immediately

            # Delegate event handling to TowerManager
            self.tower_manager.handle_event(event)

            # Handle selection of upgrade menu
            if self.selected_tower and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for path, button_rect in self.ui_manager.upgrade_buttons.items():
                    if button_rect.collidepoint(mouse_pos):
                        self.handle_upgrade_purchase(path)
                        return

        # allow user to restart in win and lose states
        elif self.state in ("win", "lose"):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    # update each of the state managing features, and win/loss conditions
    def update(self):
        if self.state == "playing" and not self.paused:
            self.enemy_manager.update()
            self.tower_manager.update()
            self.manage_attacks()
            enemy_positions = self.enemy_manager.get_positions()
            goal_x, goal_y = self.enemy_path[-1]

            # evaluate to see if the enemies have reached all the way to the end goal
            enemies_reached_goal = []
            for pos in enemy_positions:
                enemy_x = pos["enemy_x"]
                enemy_y = pos["enemy_y"]
                enemy_id = pos["enemy_id"]

                if self.has_enemy_reached_goal(enemy_x, enemy_y, goal_x, goal_y):
                    enemies_reached_goal.append(enemy_id)

            # if the enemy has reached the goal reduce user health
            for enemy_id in enemies_reached_goal:
                self.user_health -= 10
                self.enemy_manager.deal_damage(enemy_id, 1000)

            # check to see of the user still has health, and then change state accordingly
            if self.user_health <= 0:
                self.state = "lose"
            elif self.enemy_manager.waves_completed and not self.enemy_manager.enemies:
                self.state = "win"

    # render is responsible for the current state of the game that the user is in
    def render(self):
        # based on which state you are in
        if self.state == "start":
            self.ui_manager.render_start_screen()

        # render and display the screen, enemies, towers and the map,
        elif self.state == "playing":
            self.screen.fill((0, 0, 0))
            self.map_manager.draw_map()
            self.enemy_manager.render(self.screen)
            self.tower_manager.render(self.screen)

            # Render UI
            self.ui_manager.render_ui(self.user_health, self.currency, self.paused)

            if self.paused:
                self.ui_manager.render_pause_menu()

            self.ui_manager.render_upgrade_menu(self.selected_tower)

        elif self.state == "win":
            self.ui_manager.render_win_screen()

        elif self.state == "lose":
            self.ui_manager.render_lose_screen()

        pygame.display.flip()

    # allows currently selected tower to get upgraded
    def set_selected_tower(self, tower):
        self.selected_tower = tower
        self.ui_manager.set_selected_tower(tower)

    # if the user wishes to upgrade a give tower
    def handle_upgrade_purchase(self, path):
        tower = self.selected_tower
        if not tower:
            return
        upgrade_costs = {
            "damage/speed": tower.upgrade_costs.get(path, 50),
            "range": tower.upgrade_costs.get(path, 75)
        }
        cost = upgrade_costs.get(path, 0)
        # if the tower is at the max upgrade level do not let it update anymore
        if tower.upgrades.get(path, 0) >= tower.max_upgrade_level:
            self.ui_manager.set_notification(f"{path.replace('_', ' ').title()} is already at max level!")
            return
        # if the player has enought dabloons to go through with the update
        if self.currency >= cost:
            if tower.apply_upgrade(path):
                self.currency -= cost
                self.ui_manager.set_notification(f"Upgraded {path.replace('_', ' ').title()} for đ{cost}")
            else:
                self.ui_manager.set_notification("Upgrade failed!")
        else:
            self.ui_manager.set_notification("Not enough gold for upgrade!")

    def has_enemy_reached_goal(self, enemy_x, enemy_y, goal_x, goal_y):
        margin = 5
        if abs(enemy_x - goal_x) <= margin and abs(enemy_y - goal_y) <= margin:
            return True
        return False

    def reset_game(self):
        self.state = "start"
        self.user_health = 100
        self.currency = 1000
        self.enemy_manager = EnemyManager(self.screen, self.enemy_path)
        self.tower_manager = TowerManager(self.screen, self.enemy_path, self, self.map_manager.path_mask)
        self.selected_tower = None
        self.ui_manager.set_selected_tower(None)

    # manages the towers attacking enemies and controls tower attacks
    def manage_attacks(self):
        attacking_towers = self.tower_manager.get_attacking_towers()
        enemy_positions = self.enemy_manager.get_positions()
        checkpoints = self.map_manager.get_checkpoints()
        bullets = []
        for enemy in enemy_positions:
            next_checkpoint_coords = checkpoints[enemy["next_checkpoint"]]
            enemy_position = pygame.math.Vector2(enemy["enemy_x"], enemy["enemy_y"])
            enemy["distance_next"] = enemy_position.distance_squared_to(next_checkpoint_coords)

        # sort enemies so that the enemy closest to the end is first
        enemy_positions.sort(key=lambda position: position["distance_next"])
        enemy_positions.sort(key=lambda position: position["next_checkpoint"], reverse=True)

        for tower in attacking_towers:
            if tower:
                # Tower range squared
                tower_range_squared = tower["range"] ** 2
                for index, enemy in enumerate(enemy_positions):
                    enemy_position = pygame.math.Vector2(enemy["enemy_x"], enemy["enemy_y"])
                    distance_to_tower_squared = enemy_position.distance_squared_to(tower["position"])

                    if distance_to_tower_squared <= tower_range_squared \
                            and self.tower_manager.reset_attack_cooldown(tower["id"]):
                        damage_result = self.enemy_manager.deal_damage(enemy["enemy_id"], tower["damage"])
                        bullets.append((enemy_position, tower["id"]))

                        if damage_result == 2:  # the enemy died
                            enemy_positions.pop(index)
                            self.currency += ENEMY_KILL_VALUE
                        # the tower has now attacked an enemy, move to the next tower
                        break

        self.tower_manager.prepare_attack_animations(bullets)