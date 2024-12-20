import pygame


class Enemy:

    def __init__(self, canvas, checkpoints, enemy_type, id):
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
        # Just for the freeze mechanic
        self.is_frozen = False
        self.freeze_time = 0
        self.thaw_timer = 0

        self.id = id

        match enemy_type:
            # Bog-standard enemy
            case "default":
                self.health = 200
                self.speed = 3
                self.sprite = pygame.image.load("Assets/Enemy_red.png").convert()
            # Slow but high health
            case "slow":
                self.health = 800
                self.speed = 5
                self.sprite = pygame.image.load("Assets/Enemy_green.PNG").convert()
            # Fast but low health
            case "fast":
                self.health = 100
                self.speed = 1
                self.sprite = pygame.image.load("Assets/Enemy_blue.png").convert()
            # Pretty good speed and health
            case "strong":
                self.health = 600
                self.speed = 2
                self.sprite = pygame.image.load("Assets/Enemy_yellow.png").convert()

        # Set sprite as correct size
        self.sprite = pygame.transform.scale(self.sprite, (35, 25))
        self.rect = self.sprite.get_rect(center=(self.pos_x, self.pos_y))
        self.sprite = self.sprite.convert_alpha(canvas)

    def get_x(self):
        return self.rect.centerx

    def get_y(self):
        return self.rect.centery

    def get_next_checkpoint(self):
        return self.curr_checkpoint

    # Decrease health attribute, returns True if it dies
    def process_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    def freeze(self, time):
        self.is_frozen = True
        self.freeze_time = time

    def get_is_frozen(self):
        return self.is_frozen

    # Place the enemy visually on the screen
    def draw(self):
        # Draw sprite on canvas
        self.canvas.blit(self.sprite, self.rect)

    # Advances 1 pixel towards the next checkpoint once every x times it's called, with x = speed
    def advance(self):
        # Increment frame tracker
        self.counter += 1
        # Handle freeze mechanic; I put it here because it's doing that instead of moving, I suppose
        if self.is_frozen:
            self.freeze_time -= 1
            # If it's ready to thaw out
            if self.freeze_time <= 0:
                self.is_frozen = False

        # If it's time to move
        elif self.counter >= self.speed:
            # X value of next checkpoint
            check_x = self.checkpoints[self.curr_checkpoint][0]
            # Y value of next checkpoint
            check_y = self.checkpoints[self.curr_checkpoint][1]

            # Left of checkpoint
            if self.rect.centerx < check_x:
                self.rect = self.rect.move(1, 0)

            # Right of checkpoint
            if self.rect.centerx > check_x:
                self.rect = self.rect.move(-1, 0)

            # Above checkpoint
            if self.rect.centery < check_y:
                self.rect = self.rect.move(0, 1)

            # Below checkpoint
            if self.rect.centery > check_y:
                self.rect = self.rect.move(0, -1)

            # In line with checkpoint
            if check_x == self.rect.center[0]:
                if check_y == self.rect.center[1]:
                    self.curr_checkpoint += 1
                    # If we reached the last checkpoint, don't advance to next one
                    if self.curr_checkpoint == len(self.checkpoints):
                        self.curr_checkpoint -= 1
                        self.reached_end = True

            # Reset frame counter
            self.counter = 0
    
    def has_reached_goal(self):
        return self.reached_end

    def get_id(self):
        return self.id
