import pygame


class Enemy:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.sprite = pygame.Rect(0, 0, 20, 20)
        self.color = (200, 0, 0)

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, self.sprite)

    def advance(self):
        self.pos_x = self.pos_x + .1
        self.pos_y = self.pos_y + .1
        self.sprite = pygame.Rect(self.pos_x, self.pos_y, 20, 20)
