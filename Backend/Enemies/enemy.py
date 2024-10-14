import pygame


class Enemy:
    def __init__(self, canvas, checkpoints):
        self.canvas = canvas
        self.checkpoints = checkpoints
        self.pos_x = checkpoints[0][0]
        self.pos_y = checkpoints[0][1]
        self.sprite = pygame.Rect(checkpoints[0][0], checkpoints[0][1], 20, 20)
        self.color = (200, 0, 0)
        self.curr_checkpoint = 1
        self.speed = .3

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

    def draw(self):
        pygame.draw.rect(self.canvas, self.color, self.sprite)

    def advance(self):
        check_x = self.checkpoints[self.curr_checkpoint][0]
        check_y = self.checkpoints[self.curr_checkpoint][1]
        margin = self.speed/100
        
        # Left of checkpoint
        if self.pos_x < check_x:
            found_direction = True
            # Up and to left of checkpoint
            if self.pos_y < check_y:
                self.pos_x += self.speed
                self.pos_y += self.speed
            # Down and to left of checkpoint
            elif self.pos_y > check_y:
                self.pos_x += self.speed
                self.pos_y -= self.speed
            # Left and in line with checkpoint
            if check_y - margin < self.pos_y < check_y + margin:
                self.pos_x += self.speed

        # Right of checkpoint
        elif self.pos_x > check_x:
            # Up and to right of checkpoint
            if self.pos_y < check_y:
                self.pos_x -= self.speed
                self.pos_y += self.speed
            # Down and to right of checkpoint
            elif self.pos_y > check_y:
                self.pos_x -= self.speed
                self.pos_y -= self.speed
            # Right and in line with checkpoint
            if check_y - margin < self.pos_y < check_y + margin:
                self.pos_x -= self.speed

        # In line with checkpoint
        if check_x - margin < self.pos_x < check_x + margin:
            # Up and in line with checkpoint
            if self.pos_y < check_y:
                self.pos_y += self.speed
            # Down and in line with checkpoint
            elif self.pos_y > check_y:
                self.pos_y -= self.speed
            # Perfectly in line with checkpoint
            if check_y - self.speed < self.pos_y < check_y + self.speed:
                self.curr_checkpoint += 1
                if self.curr_checkpoint == len(self.checkpoints):
                    self.curr_checkpoint -= 1

        self.sprite = pygame.Rect(self.pos_x, self.pos_y, 20, 20)
