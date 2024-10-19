import pygame
from math import sqrt


# Tower Class allowing tower objects to be placed on the screen
class Tower:
    # initialize the tower object -- currently set as green square
    def __init__(self, position):
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=position)

    # draw depicts the tower on the screen
    def draw(self, screen):
        screen.blit(self.image, self.rect)

# TowerManager Class handles pressing of keys and mouse movement to place towers
class TowerManager:
    # initialize towers to be a list of set towers
    def __init__(self, screen, enemy_path):
        self.towers = []  # List of placed towers
        self.the_tower = None  # Tower currently being placed
        self.enemy_path = enemy_path
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size() # stores screen size

    # handle_event responds to user interaction such as pressing keys or moving/clicking the mouse
    def handle_event(self, event) :
        # if 't' key is clicked create a tower at current mouse position. Movement is handled in update
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t :
            mouse_position = pygame.mouse.get_pos()
            self.the_tower = Tower(mouse_position)

        # else if the mouse is clicked place down the tower
        elif event.type == pygame.MOUSEBUTTONDOWN and self.the_tower :
            if self.is_tower_placeable(self.the_tower.rect) :
                self.towers.append(self.the_tower)
                self.the_tower = None


    # is_tower_placeable asks if the tower can be placed at current mouse location given bounds of the path
    def is_tower_placeable(self, tower_rect) :
        # returns false to say that tower is too close to enemy path bounds of 20 pixels
        for (x,y) in self.enemy_path:
            if self.distance_to_point(tower_rect.center, (x, y)) < 20.0:
                return False

        screen_rect = pygame.Rect(0,0, self.screen_width, self.screen_height)
        return screen_rect.contains(tower_rect)



    # using the euclidean distance formula between two points return value
    def distance_to_point(self, pointA, pointB) :
        return sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2 )

    # manage the new tower being placed by following the mouse cursor
    def update(self) :
        if self.the_tower :
            mouse_position = pygame.mouse.get_pos()
            self.the_tower.rect.center = mouse_position

    # render is display the placed towers, and the currently being placed tower
    def render(self, screen) :
        for tower in self.towers :
            tower.draw(screen)

        if self.the_tower:
            self.the_tower.draw(screen)
