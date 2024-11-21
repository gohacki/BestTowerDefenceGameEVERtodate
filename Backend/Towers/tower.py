import pygame
from math import sqrt

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