import pygame
from math import sqrt
# does this work

# Tower Class allowing tower objects to be placed on the screen
class Tower:
    # initialize the tower object -- currently set as green square
    def __init__(self, position, tower_type):
        self.tower_type = tower_type
        self.position = position
        # store a value for home tower position so that you can deselect tower
        self.home_position = position
        # self.image = pygame.Surface((40, 40))
        self.frames_since_attack = 0

        # Based on each tower type assign an image a tower cost, attack rate,range and damage accordingly.
        if tower_type == 1:
            self.image = pygame.image.load("Assets/allison_tower.jpg")
            self.image = pygame.transform.scale(self.image, (40,40))
            self.cost = 100
            self.range = 75
            self.attack_rate = 50
            self.attack_damage = 2
        elif tower_type == 2:
            self.image = pygame.image.load("Assets/eve_tower.jpeg")
            self.image = pygame.transform.scale(self.image, (40,40))
            self.cost = 200
            self.range = 100
            self.attack_rate = 40
            self.attack_damage = 5
        elif tower_type == 3:
            self.image = pygame.image.load("Assets/jasper_tower.jpeg")
            self.image = pygame.transform.scale(self.image, (40,40))
            self.cost = 300
            self.range = 150
            self.attack_rate = 35
            self.attack_damage = 20
        elif tower_type == 4:
            self.image = pygame.image.load("Assets/miro_tower.jpeg")
            self.image = pygame.transform.scale(self.image, (40,40))
            self.cost = 400
            self.range = 200
            self.attack_rate = 35
            self.attack_damage = 25
        elif tower_type == 5:
            self.image = pygame.image.load("Assets/jason_tower.jpeg")
            self.image = pygame.transform.scale(self.image, (40, 40))
            self.cost = 3000
            self.range = 500
            self.attack_rate = 20
            self.attack_damage = 35
        # sets each position centered on the bottom left rectangle
        self.rect = self.image.get_rect(center=position)

        # This labels the given possible updates that the user can enact on a given tower
        self.upgrades = {
            "damage/speed": 0,
            "range": 0
        }

        # only let the levels go up to 5
        self.max_upgrade_level = 5
        # set given costs per each of the updates
        self.upgrade_costs = {
            "damage/speed": 50,
            "range": 75
        }

    # This allows us to upgrade each of the placed towers as needed
    def apply_upgrade(self, upgrade):
        if upgrade not in self.upgrades:
            return False

        if self.upgrades[upgrade] >= self.max_upgrade_level:
            return False

        # if user selects to increase the damage and speed of the tower implement additions
        if upgrade == "damage/speed":
            self.attack_damage += 1
            self.attack_rate = max(5, self.attack_rate - 5)
        # else if the user selects to increase the range, implement that
        elif upgrade == "range":
            self.range += 10
        # store the updated level number as +=1
        self.upgrades[upgrade] += 1
        return True

    # draw depicts the tower on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # returns true if a tower is ready to attack and false otherwise
    def can_attack(self):
        self.frames_since_attack +=1
        if self.frames_since_attack >= self.attack_rate:
            return True
        else:
            return False

    # returns the range, damage, and position of the tower in a dictionary
    def get_attack(self, index):
        return {"range": self.range, "damage": self.attack_damage, "position": self.position, "id": index}

    def reset_attack_cooldown(self):
        self.frames_since_attack = 0

    def get_type(self):
        return self.tower_type
    def get_position(self):
        return self.position


# TowerManager Class handles pressing of keys and mouse movement in order to place towers
class TowerManager:
    # initialize towers to be a list of set towers
    def __init__(self, screen, enemy_path, game_manager, path_mask):
        self.towers = []
        self.the_tower = None
        self.selected_tower_type = None
        self.enemy_path = enemy_path
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()  # stores screen size
        self.game_manager = game_manager
        # initialize path that towers cannot be placed on
        self.path_mask = path_mask
        self.bullets_to_render = []
        self.selected_tower = None

    # handle_event responds to user interaction such as pressing keys or moving/clicking the mouse
    def handle_event(self, event):
        # if the escape key is pushed while at a tower
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.the_tower:
                # unselect the current tower
                self.the_tower = None
                self.selected_tower_type = None
        # if the mouse is pressed down enable placement or selection of given tower
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # if user has selected a tower and wants to potentially place it
            if self.the_tower:
                # ensure that the tower can be placed according to bounds of map
                if self.is_tower_placeable(self.the_tower.rect):
                    tower_cost = self.the_tower.cost
                    # ensure user has enough dabloons to place tower
                    if self.game_manager.currency >= tower_cost:
                        self.game_manager.currency -= tower_cost
                        self.towers.append(self.the_tower)
                        # This fixes issue of - tower position only being set when the user first clicked on the tower.
                        self.the_tower.position = self.the_tower.rect.center
                        self.the_tower = None
                        self.selected_tower_type = None
                    else:
                        self.game_manager.set_notification("Not enough gold!")

                else:
                    self.game_manager.set_notification("Cannot place tower here!")

            # if there is no tower being placed, take into account for upgrades
            else:
                mouse_pos = pygame.mouse.get_pos()
                # loop through all the towers
                for tower in self.towers:
                    # if mouse is hovering and selecting a given tower pass into selection funciton
                    if tower.rect.collidepoint(mouse_pos):
                        self.selected_tower = tower
                        self.game_manager.set_selected_tower(tower)
                        return
                self.selected_tower = None
                self.game_manager.set_selected_tower(None)

        # if the tower is selected and you want to drop it off back at home instead of placing it
        elif event.type == pygame.MOUSEBUTTONUP and self.the_tower:
            mouse_position = pygame.mouse.get_pos()
            distance_to_home = sqrt((mouse_position[0] - self.the_tower.home_position[0]) ** 2 +
                                    (mouse_position[1] - self.the_tower.home_position[1]) ** 2)
            if distance_to_home < 20:
                self.the_tower = None
                self.selected_tower_type = None
            else:
                pass


    # is_tower_placeable asks if the tower can be placed at current mouse location given bounds of the path
    def is_tower_placeable(self, tower_rect):
        # check to see if the tower is overlapping the given path
        tower_mask = pygame.mask.from_surface(self.the_tower.image)
        tower_offset = tower_rect.topleft
        if self.path_mask.overlap(tower_mask, tower_offset):
            return False

        # check to see if the tower is overlapping with any other placed towers
        for tower in self.towers:
            if tower.rect.colliderect(tower_rect):
                return False

        # check to ensure that the tower is still on the playable screen
        screen_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        return screen_rect.contains(tower_rect)

    # set a selected tower to be "the_tower"
    def select_tower(self, tower_type):
        self.selected_tower_type = tower_type
        mouse_position = pygame.mouse.get_pos()
        self.the_tower = Tower(mouse_position, tower_type)


    # manage the new tower being placed by following the mouse cursor
    def update(self):
        if self.the_tower:
            mouse_position = pygame.mouse.get_pos()
            self.the_tower.rect.center = mouse_position

    # render is display the placed towers, and the currently being placed tower
    def render(self, screen):
        for tower in self.towers:
            tower.draw(screen)

        # highlight the selected tower and its corresponding range
        if self.selected_tower:
            pygame.draw.circle(screen, (0, 255, 0), self.selected_tower.position, self.selected_tower.range, 2)

        # render the tower that is being placed and its potential conflicts with the path
        if self.the_tower:
            self.the_tower.draw(screen)
            # display range of the tower as translucent either white or red according to validity
            if self.is_tower_placeable(self.the_tower.rect):
                range_color = (255, 255, 255, 100)  # white color when valid

            else:
                range_color = (255, 0, 0, 100)  # red to show it is invalid

            range_surface = pygame.Surface((self.the_tower.range * 2, self.the_tower.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, range_color, (self.the_tower.range, self.the_tower.range), self.the_tower.range)
            screen.blit(range_surface, (self.the_tower.rect.centerx - self.the_tower.range, self.the_tower.rect.centery - self.the_tower.range))

        # this displays bullets from each type of tower according to tower/bullet type
        while self.bullets_to_render:
            bullet = self.bullets_to_render.pop(0)
            bullet_type = self.towers[bullet[1]].get_type()
            if bullet_type == 1:
                pygame.draw.line(screen, (128, 30, 232), self.towers[bullet[1]].get_position(), bullet[0], width = 3)
            elif bullet_type == 2:
                pygame.draw.line(screen, (255, 255, 0), self.towers[bullet[1]].get_position(), bullet[0], width = 4)
            elif bullet_type == 3:
                pygame.draw.line(screen, (255, 0, 0), self.towers[bullet[1]].get_position(), bullet[0], width = 6)
            elif bullet_type == 4:
                pygame.draw.line(screen, (30, 229, 247), self.towers[bullet[1]].get_position(), bullet[0], width= 8)
            elif bullet_type == 5:
                pygame.draw.line(screen, (255, 0, 0), self.towers[bullet[1]].get_position(), bullet[0], width= 11)



    # this function
    def get_attacking_towers(self):
        attacking_towers = []
        for index, tower in enumerate(self.towers):
            if tower.can_attack():
                attacking_towers.append(tower.get_attack(index))
            else:
                attacking_towers.append(False)
        return attacking_towers

    # takes a tower id (the index of the tower in self.towers) and resets it's attack cooldown
    def reset_attack_cooldown(self, tower_id):
        try:
            self.towers[tower_id].reset_attack_cooldown()
            return True
        except IndexError:
            return False

    def prepare_attack_animations(self, bullets):
        self.bullets_to_render = bullets