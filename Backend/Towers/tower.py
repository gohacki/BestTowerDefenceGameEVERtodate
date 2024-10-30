import pygame
from math import sqrt


# Tower Class allowing tower objects to be placed on the screen
class Tower:
    # initialize the tower object -- currently set as green square
    def __init__(self, position, tower_type):
        self.tower_type = tower_type
        self.position = position
        self.image = pygame.Surface((40, 40))
        if tower_type == 1:
            self.image.fill((0, 255, 0))
            self.cost = 100
        elif tower_type == 2:
            self.image.fill((0, 0, 255))
            self.cost = 200
        elif tower_type == 3:
            self.image.fill((255, 0, 0))
            self.cost = 300
        self.rect = self.image.get_rect(center=position)

    # draw depicts the tower on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# TowerManager Class handles pressing of keys and mouse movement to place towers
class TowerManager:
    # initialize towers to be a list of set towers
    def __init__(self, screen, enemy_path, game_manager, path_mask):
        self.towers = []
        self.the_tower = None
        self.selected_tower_type = None
        self.enemy_path = enemy_path
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size() # stores screen size
        self.game_manager = game_manager
        # initialize path that towers cannot be placed on
        self.path_mask = path_mask

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
                    self.the_tower = None
                    self.selected_tower_type = None
                else:
                    print("Not enough gold!")
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

    # using the euclidean distance formula between two points return value
    def distance_to_point(self, pointA, pointB) :
        return sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2 )

    # manage the new tower being placed by following the mouse cursor
    def update(self) :
        if self.the_tower:
            mouse_position = pygame.mouse.get_pos()
            self.the_tower.rect.center = mouse_position

    # render is display the placed towers, and the currently being placed tower
    def render(self, screen) :
        for tower in self.towers :
            tower.draw(screen)

        if self.the_tower:
            self.the_tower.draw(screen)
