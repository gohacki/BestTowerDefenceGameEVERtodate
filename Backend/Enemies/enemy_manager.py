from enemy import Enemy


# Create a list of enemies for the manager to use
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

    def getPositions(self):
        positions = []
        counter = 0
        for enemy in self.enemies:
            # Create a tuple with x coordinate, y coordinate, and an id
            positions.append([enemy.get_x(), enemy.get_y(), counter])
            counter += 1
        return positions
