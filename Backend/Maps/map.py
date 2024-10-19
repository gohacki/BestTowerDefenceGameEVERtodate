import pygame
import random
import csv

MAX_PATH_OFFSET = 20

class MapException(Exception):
    pass


class Map:

    # canvas should be the surface within which to display the map and the map name should be a string
    def __init__(self, canvas, map_name):
        self.path = [[]]
        self.canvas = canvas

        try:
            # the path is defined as a set of boxed checkpoints which are lists of 4 integers the first two represent
            # the min and max x values respectively and the second two represent the min and max y values respectively
            csv_file_name = map_name + "_checkpoints.csv"
            print(csv_file_name)
            with open(csv_file_name, newline='') as checkpoints:
                csv_contents = csv.reader(checkpoints, delimiter=',')
                for row in csv_contents:
                    box = []
                    for bound in row:
                        box.append(int(bound))
                self.path.append(box)

            map_image_file_name = map_name + ".png"
            print(map_image_file_name)
            self.back_ground = pygame.image.load(map_image_file_name).convert()

        except FileNotFoundError:
            # TODO: Decide how to handle file not found
            print("map file not found\n")
            raise MapException
        except ValueError:
            # TODO: Decide how to handle file not found
            print("map file corrupt\n")
            raise MapException

    # this method returns a series of checkpoints forming a path for an enemy to follow. The checkpoints are randomly
    # generated with in a box for each checkpoint
    # returns a tuple of checkpoints which are tuples of int pairs (x, y) representing pixel coordinates on the screen
    def get_checkpoints(self):
        checkpoints = [[]]
        # slightly randomizing the path within a distance of MAX_PATH_OFFSET from the centerline of the path
        rand_offset = MAX_PATH_OFFSET * random.random()
        rand_angle = 360 * random.random()
        offset = pygame.math.Vector2.from_polar((rand_offset, rand_angle))
        x_offset = int(offset[1])
        y_offset = int(offset[2])
        for checkpoint in self.path:
            # randomly generate coords within box
            x = checkpoint[1] + x_offset
            y = checkpoint[2] + y_offset
            coords = (x, y)
            checkpoints.append(coords)
        return tuple(checkpoints)

    # displays the map image
    def draw_map(self):
        pygame.Surface.blit(self.back_ground, self.canvas, (0, 0), area=(self.canvas.get_width, self.canvas.get_height))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    try:
        map_one = Map(screen, 'map_one')
        print("map init complete")
        map_one.draw_map()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            map_one.draw_map()

    except MapException:
        print("Maps not working\n")
