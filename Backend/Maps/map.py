import pygame
import random
import csv

class Map:
    def __init__(self, canvas, map_name):
        try:
            # the path is defined as a set of boxed checkpoints which are lists of 4 integers the first two represent the
            # min and max x values respectively and the second two represent the min and max y values respectively
            self.path = [[]]
            with open(map_name + "_checkpoints.csv", newline='') as checkpoints:
                csv_contents = csv.reader(checkpoints, delimiter=',')
                for row in csv_contents:
                    box = []
                    for bound in row:
                        box.append(int(bound))
                self.path.append(box)

            self.back_ground = pygame.image.load(map_name + ".png").convert()
            self.canvas = canvas
        except FileNotFoundError:
            # TODO: Decide how to handle file not found currently a message is displayed on the screen
            if not pygame.font.get_init():
                pygame.font.init()
            message_color = (255, 255, 255)
            message = pygame.font.Font.render("Map files could not be found.", 1, color=message_color, background=None)
            pygame.surface.Surface.blit(message, self.canvas, (self.canvas.get_width/2, self.canvas.get_height/2))
        except ValueError:
            if not pygame.font.get_init():
                pygame.font.init()
            message_color = (255, 255, 255)
            message = pygame.font.Font.render("Map files are invalid.", 1, color=message_color, background=None)
            pygame.surface.Surface.blit(message, self.canvas, (self.canvas.get_width/2, self.canvas.get_height/2))

    def get_checkpoints(self):
        checkpoints = [[]]
        for checkpoint in self.path:
            x = random.randint(checkpoint[1], checkpoint[2])
            y = random.randint(checkpoint[3], checkpoint[4])
            coords = (x, y)
            checkpoints.append(coords)
        return tuple(checkpoints)

    def draw_map(self):
        self.canvas.blit(self.back_ground, self.canvas, (0, 0))
