import pygame


class Enemy:
    def __init__(self, canvas, checkpoints):
        self.canvas = canvas
        self.health = 10
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
        self.curr_checkpoint = 1
        # Moves 1 pixel once every speed frames
        self.speed = 5
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


def generate_wave(num_spawns, canvas, checkpoints):
    wave = []
    for i in range(num_spawns):
        wave.append(Enemy(canvas, checkpoints))
    return wave


# Just used as a translator between GameManager and Enemy
class EnemyManager:
    def __init__(self, canvas, checkpoints):
        # List of enemies in the current wave
        self.enemies = []
        # Used to track how many enemies we've created so far
        self.spawn_counter = 0
        # How many enemies we want to create
        self.spawn_target = 5
        # How long to wait between spawning enemies
        self.timer_target = 750
        # Counter to check if it's time to spawn an enemy yet; start at full
        self.timer_counter = self.timer_target
        self.wave = generate_wave(self.spawn_target, canvas, checkpoints)

    def update(self):
        # If not all have been spawned
        if self.spawn_counter < self.spawn_target:
            # If it's time to spawn a new one, reset timer and do so
            if self.timer_counter == self.timer_target:
                # Pull a new enemy from the wave
                self.enemies.append(self.wave[self.spawn_counter])
                self.spawn_counter += 1
                self.timer_counter = 0
            # Otherwise, increment timer
            self.timer_counter += 1

        # Advance all spawned enemies
        for enemy in self.enemies:
            enemy.advance()

    def render(self, screen):
        # Draw all spawned enemies
        for i in range(self.spawn_counter):
            self.enemies[i].draw()
