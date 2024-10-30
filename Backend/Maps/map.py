import pygame
import random
import csv

MAX_PATH_OFFSET = 20

# exception for maps to be used for when maps don't load properly
class MapException(Exception):
    pass


class MapManager:

    # canvas should be the surface within which to display the map and the map name should be a string
    def __init__(self, canvas, map_name):
        self.path = list(list())
        self.canvas = canvas
        try:
            # the path is defined as a set of boxed checkpoints which are lists of 4 integers the first two represent
            # the min and max x values respectively and the second two represent the min and max y values respectively
            csv_file_name = map_name + "_checkpoints.csv"
            with open(csv_file_name, newline='') as checkpoints:
                csv_contents = csv.reader(checkpoints, delimiter=',')
                for row in csv_contents:
                    point = []
                    for coord in row:
                        point.append(int(coord))
                    self.path.append(point)

            map_image_file_name = map_name + ".png"
            self.back_ground = pygame.image.load(map_image_file_name).convert()
        # one of the files was not found
        except FileNotFoundError:
            # TODO: Decide how to handle file not found
            print("map file not found\n")
            raise MapException
        # the path couldn't be parsed properly
        except ValueError:
            # TODO: Decide how to handle file not found
            print("map file corrupt\n")
            raise MapException

        # miro
        self.path_surface = pygame.Surface((self.canvas.get_width(), self.canvas.get_height()), pygame.SRCALPHA)
        self.draw_path()
        self.path_mask = pygame.mask.from_surface(self.path_surface)
    
    # miro
    def draw_path(self):
        checkpoints = self.get_checkpoints()
        pygame.draw.lines(self.path_surface, (255, 255, 255), False, checkpoints, MAX_PATH_OFFSET * 2)

    # this method returns a series of checkpoints forming a path for an enemy to follow. The checkpoints are randomly
    # generated with in a circle for each checkpoint
    # returns a tuple of checkpoints which are tuples of int pairs (x, y) representing pixel coordinates on the screen
    def get_checkpoints_randomized(self):
        checkpoints = list(list())
        # slightly randomizing the path within a distance of MAX_PATH_OFFSET from the centerline of the path
        rand_offset = MAX_PATH_OFFSET * random.random()
        rand_angle = 360 * random.random()
        offset = pygame.math.Vector2.from_polar((rand_offset, rand_angle))
        x_offset = int(offset[0])
        y_offset = int(offset[1])

        for checkpoint in self.path:
            x = checkpoint[0] + x_offset
            y = checkpoint[1] + y_offset
            coords = (x, y)
            checkpoints.append(coords)
        return tuple(checkpoints)

    # This method returns a list of checkpoints for the map without randomization
    def get_checkpoints(self):
        checkpoints = list()
        for point in self.path:
            checkpoints.append(tuple(point))
        return tuple(checkpoints)

    # displays the map image
    def draw_map(self):
        self.canvas.blit(self.back_ground, (0, 0))


# used for testing purposes and previewing new maps
if __name__ == '__main__':

    MAP_NAME = 'map_one'

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    pygame.display.set_caption("image")
    running = True

    try:
        map_one = MapManager(screen, MAP_NAME)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            map_one.draw_map()
            pygame.display.flip()


    except MapException:
        print("Maps not working\n")
