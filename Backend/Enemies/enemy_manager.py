from enemy import Enemy


# Create a list of enemies for the manager to use
def generate_wave(canvas, checkpoints):
    wave = []
    spawn_delays = []
    infile = open("wave.txt", "r")
    # Just grab all the text from our file
    raw_text = infile.readlines()
    infile.close()
    # Loop through every line from the file
    for i in range(0, len(raw_text)):
        # File alternates between enemy type and spawn delay on each line
        if i % 2 == 0:
            # Grab enemy type, clean it up, push to wave
            enemy_type = raw_text[i]
            enemy_type = enemy_type.replace('\n', '')
            enemy = Enemy(canvas, checkpoints, enemy_type)
            wave.append(enemy)
        else:
            # Grab spawn delay, clean it up, push to spawn_delays
            delay = raw_text[i]
            delay = delay.replace("\n", "")
            delay = int(delay)
            spawn_delays.append(delay)

    return wave, spawn_delays


# Just used as a translator between GameManager and Enemy
class EnemyManager:
    def __init__(self, canvas, checkpoints):
        # List of enemies currently spawned
        self.enemies = []
        # List of all enemies in the current wave
        self.wave = []
        # The spawn delay for each enemy
        self.spawn_targets = []
        # Delay for next enemy to be spawned
        self.current_spawn_target = 0
        # Used to track how many enemies we've created so far
        self.spawn_counter = 0
        # Counter to check if it's time to spawn an enemy yet; start at full
        self.timer_counter = self.current_spawn_target
        self.wave, self.spawn_targets = generate_wave(canvas, checkpoints)

    # Moves all enemies towards next checkpoints, and sometimes spawns new ones
    # Returns True if an enemy reaches the end of the map
    def update(self):
        # If not all have been spawned
        if self.spawn_counter < len(self.wave):
            # If it's time to spawn a new one, reset timer and do so
            if self.timer_counter == self.current_spawn_target:
                # Pull a new enemy from the wave
                self.enemies.append(self.wave[self.spawn_counter])
                # Grab next timer target
                self.current_spawn_target = self.spawn_targets[self.spawn_counter]
                self.spawn_counter += 1
                self.timer_counter = 0
            # Otherwise, increment timer
            self.timer_counter += 1

        # Advance all spawned enemies
        for enemy in self.enemies:
            enemy.advance()
            # Eliminate if it reaches the last checkpoint
            if enemy.has_reached_goal():
                self.enemies.remove(enemy)
                return True

    # Draws all enemies on the screen
    def render(self, screen):
        # Draw all spawned enemies
        for i in range(len(self.enemies)):
            self.enemies[i].draw()

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
