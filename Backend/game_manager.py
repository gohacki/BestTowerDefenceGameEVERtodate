import pygame
from .Towers.tower import TowerManager
from .Enemies.enemy_manager import EnemyManager
from .Maps.map import MapManager

ENEMY_KILL_VALUE = 20


# TODO Obviously this code does not create a level, so we may want to create the level_manager file too

# Main class to handle each of the game states and potential interactions
class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = "start"
        self.font = pygame.font.Font(None, 36)
        self.pause_button_rect = pygame.Rect(10, 90, 100, 40)  # x, y, width, height
        self.pause_button_text = self.font.render("Pause", True, (255, 255, 255))

        # useful to display notifications for the user
        self.notification = ""
        self.notification_time = 0

        # load the game map, and get the checkpoints of given display
        test_map_name = './Assets/map_one'
        self.map_manager = MapManager(screen, test_map_name)
        self.enemy_path = self.map_manager.get_checkpoints()

        # initialize the towers and game values that will be displayed
        self.tower_manager = TowerManager(self.screen, self.enemy_path, self, self.map_manager.path_mask)
        self.enemy_manager = EnemyManager(self.screen, self.enemy_path)
        self.user_health = 100
        self.currency = 1000
        

        # create a dictionary for the tower selection process
        self.tower_images = {
            1: pygame.transform.scale(pygame.image.load("Assets/allison_tower.jpg"), (40,40)),
            2: pygame.transform.scale(pygame.image.load("Assets/eve_tower.jpeg"), (40, 40)),
            3: pygame.transform.scale(pygame.image.load("Assets/jasper_tower.jpeg"), (40, 40)),
            4: pygame.transform.scale(pygame.image.load("Assets/miro_tower.jpeg"), (40, 40)),
            5: pygame.transform.scale(pygame.image.load("Assets/jason_tower.jpeg"), (40, 40))
        }

        self.create_tower_buttons()
        self.paused = False

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = "playing"

        elif self.state == "playing":
            # if user pushes the mouse while in the playing state
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                if self.pause_button_rect.collidepoint(mouse_pos):
                    self.paused = not self.paused
                    return
                # check if a tower button was clicked
                for rect, tower_type in self.tower_buttons:
                    if rect.collidepoint(mouse_pos):
                        self.tower_manager.select_tower(tower_type)
                        return  # exit early to avoid unselecting the tower immediately
            self.tower_manager.handle_event(event)

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

            # evaluate to see if the enemies have reached all the way to the goal
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
            elif not self.enemy_manager.enemies and self.enemy_manager.spawn_counter >= self.enemy_manager.spawn_target:
                self.state = "win"

    # render is responsible for the current state of the game that the user is in
    def render(self):
        # based on which state you are in
        if self.state == "start":
            self.render_start_screen()

        # render and display the screen, enemies, towers and the map,
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

    # star screen display and lettering along with instructions
    def render_start_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Best Tower Defense Game Ever To Date", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press Enter to Start Please", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    # win screen display and lettering
    def render_win_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    # loss screen display and lettering
    def render_lose_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    # create the tower selection buttons
    def render_tower_selection_ui(self):
        for rect, tower_type in self.tower_buttons:
            # set each tower to be a its corresponding image
            image = self.tower_images[tower_type]
            image_rect = image.get_rect(center = rect.center)
            self.screen.blit(image, image_rect)


            tower_label = self.font.render(f"Tower {tower_type}", True, (255, 255, 255))
            label_rect = tower_label.get_rect(center=(rect.centerx, rect.bottom + 15))
            self.screen.blit(tower_label, label_rect)

    # position the towers within the screen
    def create_tower_buttons(self):
        self.button_size = (50, 50)
        margin = 60
        y_position = self.screen.get_height() - self.button_size[1] - margin

        self.tower_buttons = []
        num_buttons = 5
        total_width = num_buttons * self.button_size[0] + (num_buttons - 1) * margin

        # center the buttons horizontally on the screen
        start_x = (self.screen.get_width() - total_width) // 2
        for i in range(num_buttons):
            x_position = start_x + i * (self.button_size[0] + margin) - 100
            rect = pygame.Rect(x_position, y_position, *self.button_size)
            self.tower_buttons.append((rect, i + 1))

    # create the pause text and slow of game play
    def render_pause_menu(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # allows you to still see through
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (255, 255, 255))
        self.screen.blit(text, (
            self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height()))
        font_small = pygame.font.Font(None, 36)
        instructions = font_small.render("Press 'P' to Resume", True, (255, 255, 255))
        self.screen.blit(instructions, (
            self.screen.get_width() // 2 - instructions.get_width() // 2, self.screen.get_height() // 2 + 20))

    # displays interactions for the user
    def render_ui(self):
        # Display health
        health_text = self.font.render(f"Health: {self.user_health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))
        # Display gold currency
        currency_text = self.font.render(f"Gold Dabloons: {self.currency}", True, (255, 255, 0))
        self.screen.blit(currency_text, (10, 50))
        self.render_tower_selection_ui()
        if self.notification:
            if pygame.time.get_ticks() - self.notification_time < 2000:
                notification_text = self.font.render(self.notification, True, (255, 0, 0))
                self.screen.blit(notification_text,
                                 (self.screen.get_width() // 2 - notification_text.get_width() // 2, 100))
            else:
                self.notification = ""
        
        pygame.draw.rect(self.screen, (50, 50, 50), self.pause_button_rect)  # Button background
        label = self.font.render("Resume" if self.paused else "Pause", True, (255, 255, 255))
        label_rect = label.get_rect(center=self.pause_button_rect.center)
        self.screen.blit(label, label_rect)

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

    def set_notification(self, message):
        self.notification = message
        self.notification_time = pygame.time.get_ticks()

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
                # I think this is correct
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
                            # TODO: rotate tower to point at enemy
                            self.currency += ENEMY_KILL_VALUE
                        # the tower has now attacked an enemy, move to the next tower
                        break

        self.tower_manager.prepare_attack_animations(bullets)
