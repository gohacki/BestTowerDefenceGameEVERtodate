# File: Backend/UI/ui_manager.py

import pygame

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.pause_button_rect = pygame.Rect(10, 90, 100, 40)  # x, y, width, height
        self.pause_button_text = self.font.render("Pause", True, (255, 255, 255))

        # useful to display notifications for the user
        self.notification = ""
        self.notification_time = 0

        # create a dictionary for the tower selection process and image loading
        self.tower_images = {
            1: pygame.transform.scale(pygame.image.load("Assets/allison_tower.jpg"), (40,40)),
            2: pygame.transform.scale(pygame.image.load("Assets/eve_tower.jpeg"), (40, 40)),
            3: pygame.transform.scale(pygame.image.load("Assets/jasper_tower.jpeg"), (40, 40)),
            4: pygame.transform.scale(pygame.image.load("Assets/miro_tower.jpeg"), (40, 40)),
            5: pygame.transform.scale(pygame.image.load("Assets/jason_tower.jpeg"), (40, 40))
        }

        self.create_tower_buttons()
        self.selected_tower = None  # selected tower for upgrades
        self.upgrade_menu_position = (0, 0)

        # create upgrade buttons
        self.upgrade_button_size = (100, 50)
        self.upgrade_buttons = {
            "damage/speed": pygame.Rect(0, 0, *self.upgrade_button_size),
            "range": pygame.Rect(0, 0, *self.upgrade_button_size)
        }

    # create the tower selection buttons
    def create_tower_buttons(self):
        self.button_size = (50, 50)
        margin = 60
        y_position = self.screen.get_height() - self.button_size[1] - 60

        self.tower_buttons = []
        num_buttons = 5
        total_width = num_buttons * self.button_size[0] + (num_buttons - 1) * margin

        # center the buttons horizontally on the screen
        start_x = (self.screen.get_width() - total_width) // 2
        for i in range(num_buttons):
            x_position = start_x + i * (self.button_size[0] + margin) - 200
            rect = pygame.Rect(x_position, y_position, *self.button_size)
            self.tower_buttons.append((rect, i + 1))

    # render the tower selection UI
    def render_tower_selection_ui(self):
        for rect, tower_type in self.tower_buttons:
            # set each tower to be its corresponding image
            image = self.tower_images[tower_type]
            image_rect = image.get_rect(center=rect.center)
            self.screen.blit(image, image_rect)

            # display the names of each tower
            names = ["Allison", "Eve", "Jasper", "Miro", "Jason"]
            tower_label = self.font.render(f"{names[tower_type-1]}", True, (255, 255, 255))
            label_rect = tower_label.get_rect(center=(rect.centerx, rect.bottom + 15))
            self.screen.blit(tower_label, label_rect)

            # display the price of each tower
            price = ["đ 100", "đ 200", "đ 300", "đ 400", "đ 3000"]
            tower_cost = self.font.render(f"{price[tower_type - 1]}", True, (255, 255, 0))
            cost_rect = tower_cost.get_rect(center=(rect.centerx, rect.bottom + 38))
            self.screen.blit(tower_cost, cost_rect)

    # render the main UI elements
    def render_ui(self, user_health, currency, paused):
        # Display health
        health_text = self.font.render(f"Health: {user_health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))
        # Display gold currency
        currency_text = self.font.render(f"Golden Dabloon: đ{currency}", True, (255, 255, 0))
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
        label = self.font.render("Resume" if paused else "Pause", True, (255, 255, 255))
        label_rect = label.get_rect(center=self.pause_button_rect.center)
        self.screen.blit(label, label_rect)

    # render the start screen
    def render_start_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Best Tower Defense Game Ever To Date", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press Enter to Start Please", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    # render the win screen
    def render_win_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    # render the lose screen
    def render_lose_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        font = pygame.font.Font(None, 36)
        instructions = font.render("Press R to Restart", True, (255, 255, 255))
        self.screen.blit(instructions, (self.screen.get_width() // 2 - instructions.get_width() // 2, 300))

    # render the pause menu
    def render_pause_menu(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # semi-transparent overlay
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, (255, 255, 255))
        self.screen.blit(text, (
            self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height()))
        font_small = pygame.font.Font(None, 36)
        instructions = font_small.render("Press 'P' to Resume", True, (255, 255, 255))
        self.screen.blit(instructions, (
            self.screen.get_width() // 2 - instructions.get_width() // 2, self.screen.get_height() // 2 + 20))

    # render the upgrade menu
    def render_upgrade_menu(self, selected_tower):
        if not selected_tower:
            return

        menu_x, menu_y = self.upgrade_menu_position

        menu_width = 220
        menu_height = 100
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, (50, 50, 50), menu_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), menu_rect, 2)

        self.upgrade_buttons["damage/speed"].topleft = (menu_x + 10, menu_y + 10)
        self.upgrade_buttons["range"].topleft = (menu_x + 120, menu_y + 10)

        pygame.draw.rect(self.screen, (0, 0, 255), self.upgrade_buttons["damage/speed"])
        text_a = self.font_small.render("Speed", True, (255, 255, 255))
        text_rect_a = text_a.get_rect(center=self.upgrade_buttons["damage/speed"].center)
        self.screen.blit(text_a, text_rect_a)

        pygame.draw.rect(self.screen, (255, 0, 0), self.upgrade_buttons["range"])
        text_b = self.font_small.render("Range", True, (255, 255, 255))
        text_rect_b = text_b.get_rect(center=self.upgrade_buttons["range"].center)
        self.screen.blit(text_b, text_rect_b)

        level_a = selected_tower.upgrades.get("damage/speed", 0)
        level_a_text = self.font_small.render(f"Level A: {level_a}", True, (255, 255, 255))
        self.screen.blit(level_a_text, (menu_x + 10, menu_y + 70))

        level_b = selected_tower.upgrades.get("range", 0)
        level_b_text = self.font_small.render(f"Level B: {level_b}", True, (255, 255, 255))
        self.screen.blit(level_b_text, (menu_x + 120, menu_y + 70))

    # set a notification message
    def set_notification(self, message):
        self.notification = message
        self.notification_time = pygame.time.get_ticks()

    # set the position for the upgrade menu
    def set_upgrade_menu_position(self, position):
        self.upgrade_menu_position = position

    # set the selected tower
    def set_selected_tower(self, tower):
        self.selected_tower = tower
        if tower:
            self.set_upgrade_menu_position((tower.position[0] + 50, tower.position[1] - 50))
        else:
            self.set_upgrade_menu_position((0, 0))