import pygame
from math import sqrt


# Tower Class allowing tower objects to be placed on the screen
class Tower:
    # initialize the tower object -- currently set as green square
    def __init__(self, position, tower_type):
        self.tower_type = tower_type
        self.position = position
        # self.image = pygame.Surface((40, 40))
        self.frames_since_attack = 0
        if tower_type == 1:
            self.image = pygame.image.load("Assets/allison_tower.jpg")
            self.image = pygame.transform.scale(self.image, (40,40))
            self.cost = 100
            self.range = 150
            self.attack_rate = 15
            self.attack_damage = 30
        elif tower_type == 2:
            self.image = pygame.image.load("Assets/eve_tower.jpeg")
            self.image = pygame.transform.scale(self.image, (40,40))
            self.cost = 200
            self.range = 200
            self.attack_rate = 30
            self.attack_damage = 80
        elif tower_type == 3:
            self.image = pygame.image.load("Assets/jasper_tower.jpeg")
            self.image = pygame.transform.scale(self.image, (40,40))
            self.cost = 300
            self.range = 300
            self.attack_rate = 60
            self.attack_damage = 100
        elif tower_type == 4:
            self.image = pygame.image.load("Assets/miro_tower.jpeg")
            self.image = pygame.transform.scale(self.image, (40,40))
            self.cost = 400
            self.range = 400
            self.attack_rate = 100
            self.attack_damage = 130
        elif tower_type == 5:
            self.image = pygame.image.load("Assets/jason_tower.jpeg")
            self.image = pygame.transform.scale(self.image, (40, 40))
            self.cost = 500
            self.range = 500
            self.attack_rate = 3
            self.attack_damage = 200
        # sets position centered on rectangle
        self.rect = self.image.get_rect(center=position)

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


# TowerManager Class handles pressing of keys and mouse movement to place towers
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

    # handle_event responds to user interaction such as pressing keys or moving/clicking the mouse
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.the_tower:
                # Unselect the current tower
                self.the_tower = None
                self.selected_tower_type = None
        elif event.type == pygame.MOUSEBUTTONDOWN and self.the_tower:
            if self.is_tower_placeable(self.the_tower.rect):
                tower_cost = self.the_tower.cost
                if self.game_manager.currency >= tower_cost:
                    self.game_manager.currency -= tower_cost
                    self.towers.append(self.the_tower)
                    # This fixed the issue, tower position was only being set when the user first clicked on the tower.
                    self.the_tower.position = self.the_tower.rect.center
                    self.the_tower = None
                    self.selected_tower_type = None
                else:
                    self.game_manager.set_notification("Not enough gold!")
            else:
                print("Cannot place tower here!")

    # is_tower_placeable asks if the tower can be placed at current mouse location given bounds of the path
    def is_tower_placeable(self, tower_rect):
        # create a mask for the tower
        tower_mask = pygame.mask.from_surface(self.the_tower.image)
        tower_offset = tower_rect.topleft

        # check if tower and path overlap.
        if self.path_mask.overlap(tower_mask, tower_offset):
            return False

        # check if the tower is on the screen
        screen_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        return screen_rect.contains(tower_rect)

    def select_tower(self, tower_type):
        self.selected_tower_type = tower_type
        mouse_position = pygame.mouse.get_pos()
        self.the_tower = Tower(mouse_position, tower_type)

    # using the euclidean distance formula between two points return value -- pygame.math has a function for this
    def distance_to_point(self, pointA, pointB):
        return sqrt((pointA[0] - pointB[0]) ** 2 + (pointA[1] - pointB[1]) ** 2)

    # manage the new tower being placed by following the mouse cursor
    def update(self):
        if self.the_tower:
            mouse_position = pygame.mouse.get_pos()
            self.the_tower.rect.center = mouse_position

    # render is display the placed towers, and the currently being placed tower
    def render(self, screen):
        for tower in self.towers:
            tower.draw(screen)

        if self.the_tower:
            self.the_tower.draw(screen)

            range_color = (255, 255, 255, 100)
            range_surface = pygame.Surface((self.the_tower.range * 2, self.the_tower.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, range_color, (self.the_tower.range, self.the_tower.range), self.the_tower.range)
            screen.blit(range_surface, (self.the_tower.rect.centerx - self.the_tower.range, self.the_tower.rect.centery - self.the_tower.range))

        while self.bullets_to_render:
            bullet = self.bullets_to_render.pop(0)
            bullet_type = self.towers[bullet[1]].get_type()
            if bullet_type == 1:
                pygame.draw.line(screen, (255, 0, 0), self.towers[bullet[1]].get_position(), bullet[0], width=1)
            elif bullet_type == 2:
                pygame.draw.line(screen, (255, 255, 0), self.towers[bullet[1]].get_position(), bullet[0], width=3)
            elif bullet_type == 3:
                pygame.draw.line(screen, (255, 0, 0), self.towers[bullet[1]].get_position(), bullet[0], width=7)
            elif bullet_type == 4:
                pygame.draw.line(screen, (255, 0, 0), self.towers[bullet[1]].get_position(), bullet[0], width=3)
            elif bullet_type == 5:
                pygame.draw.line(screen, (255, 0, 0), self.towers[bullet[1]].get_position(), bullet[0], width=40)



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
