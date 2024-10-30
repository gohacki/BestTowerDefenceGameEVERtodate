import pygame


class Enemy:
    def __init__(self, canvas, checkpoints):
        self.canvas = canvas
        self.health = 500
        # List of points on the map that enemies approach
        self.checkpoints = checkpoints
        # Current x position, starts at first checkpoint by default
        self.pos_x = checkpoints[0][0]
        # Current y position, starts at first checkpoint by default
        self.pos_y = checkpoints[0][1]
        # The thing to be drawn on canvas; currently a rectangle, to be changed later
        self.sprite = pygame.Rect(checkpoints[0][0], checkpoints[0][1], 20, 20)
        # Color of rectangle
        self.color = (200, 0, 0)
        # Checkpoint counter, used to track where the enemy is going
        # Reducing this from 5 to 1 speeds the enemies up for testing - Miro
        self.curr_checkpoint = 1
        # Moves 1 pixel once every speed frames
        self.speed = 1
        # Used to track when the next movement should occur
        self.counter = 0

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

    # Decrease health attribute, returns True if it dies
    def process_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    # Place the enemy visually on the screen
    def draw(self):
        # Draw sprite on canvas
        pygame.draw.rect(self.canvas, self.color, self.sprite)

    # Advances 1 pixel towards the next checkpoint once every x times it's called, with x = speed
    def advance(self):
        # Increment frame tracker
        self.counter += 1
        # If it's time to move
        if self.counter == self.speed:
            # X value of next checkpoint
            check_x = self.checkpoints[self.curr_checkpoint][0]
            # Y value of next checkpoint
            check_y = self.checkpoints[self.curr_checkpoint][1]

            # Left of checkpoint
            if self.pos_x < check_x:
                self.pos_x += 1

            # Right of checkpoint
            if self.pos_x > check_x:
                self.pos_x -= 1

            # Above checkpoint
            if self.pos_y < check_y:
                self.pos_y += 1

            # Below checkpoint
            if self.pos_y > check_y:
                self.pos_y -= 1

            # In line with checkpoint
            if check_x == self.pos_x:
                if check_y == self.pos_y:
                    self.curr_checkpoint += 1
                    # If we reached the last checkpoint, don't advance to next one
                    if self.curr_checkpoint == len(self.checkpoints):
                        self.curr_checkpoint -= 1

            # Modify sprite
            self.sprite = pygame.Rect(self.pos_x, self.pos_y, 20, 20)
            # Reset frame counter
            self.counter = 0
    
    def has_reached_goal(self):
        goal_x, goal_y = self.checkpoints[-1]
        return self.pos_x == goal_x and self.pos_y == goal_y
