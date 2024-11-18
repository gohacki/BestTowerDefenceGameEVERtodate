import pygame


class Enemy:

    def __init__(self, canvas, checkpoints, enemy_type):
        self.canvas = canvas
        # List of points on the map that enemies approach
        self.checkpoints = checkpoints
        # Current x position, starts at first checkpoint by default
        self.pos_x = checkpoints[0][0]
        # Current y position, starts at first checkpoint by default
        self.pos_y = checkpoints[0][1]
        # Checkpoint counter, used to track where the enemy is going
        self.curr_checkpoint = 1
        # Used to track when the next movement should occur
        self.counter = 0
        # Tracks if it has reached the last checkpoint
        self.reached_end = False

        match enemy_type:
            # Bog-standard enemy
            case "default":
                self.health = 100
                self.speed = 4
                self.sprite = pygame.image.load("../../Assets/Solid_red.png")
            # Slow but high health
            case "slow":
                self.health = 300
                self.speed = 6
                self.sprite = pygame.image.load("../../Assets/Dark_green.PNG")
            # Fast but low health
            case "fast":
                self.health = 50
                self.speed = 2
                self.sprite = pygame.image.load("../../Assets/Light_blue.png")
            # Pretty good speed and health
            case "strong":
                self.health = 400
                self.speed = 3
                self.sprite = pygame.image.load("../../Assets/Solid_yellow.png")

        # Set sprite as correct size
        self.sprite = pygame.transform.scale(self.sprite, (20, 20))

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

    def get_next_checkpoint(self):
        return self.curr_checkpoint

    # Decrease health attribute, returns True if it dies
    def process_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    # Place the enemy visually on the screen
    def draw(self):
        # Draw sprite on canvas
        self.canvas.blit(self.sprite, (self.pos_x, self.pos_y))

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
                        self.reached_end = True

            # Reset frame counter
            self.counter = 0
    
    def has_reached_goal(self):
        return self.reached_end
