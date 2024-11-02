from .enemy import Enemy


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
        self.spawn_target = 15
        # How long to wait between spawning enemies
        self.timer_target = 750
        # Counter to check if it's time to spawn an enemy yet; start at full
        self.timer_counter = self.timer_target
        self.wave = generate_wave(self.spawn_target, canvas, checkpoints)

    # Moves all enemies towards next checkpoints, and sometimes spawns new ones
    # Returns True if an enemy reaches the end of the map
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
            # I added 
            if enemy.has_reached_goal():
                self.enemies.remove(enemy)
                return True

    # Draws all enemies on the screen
    def render(self, screen):
        # Draw all spawned enemies
        for i in range(len(self.enemies)):
            self.enemies[i].draw()

    # todo: print results to csv for testing
    # Returns a list of dictionaries, which themselves contain next checkpoint, current x and y coordinates plus an id
    def get_positions(self):
        positions = []

        for index, enemy in enumerate(self.enemies):
            # Create a dictionary with next checkpoint, current x coordinate, current y coordinate, and an id
            positions.append({"next_checkpoint": enemy.get_next_checkpoint(),
                              "enemy_x": enemy.get_x(),
                              "enemy_y": enemy.get_y(),
                              "enemy_id": index})

        return positions

    # Processes damage on a given enemy NOTE: returns 0 if enemy does not exist, returns 1 if enemy damaged,
    # returns 2 if enemy killed
    def deal_damage(self, id, damage):
        # Check to make sure that the enemy we intend to damage actually exists
        if id >= len(self.enemies):
            return 0
        # Just calling the damage function in Enemy on the intended target
        if self.enemies[id].process_damage(damage):
            # If it dies, remove it from the list
            self.enemies.remove(self.enemies[id])
            return 2
        else:
            return 1
