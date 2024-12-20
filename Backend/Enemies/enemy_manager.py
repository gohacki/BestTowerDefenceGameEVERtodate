from Backend.Enemies.enemy import Enemy

# Just used as a translator between GameManager and Enemy
class EnemyManager:
    def __init__(self, canvas, checkpoints):
        self.canvas = canvas
        self.checkpoints = checkpoints
        # List of enemies currently spawned
        self.enemies = []
        # List of all enemies in the current wave
        self.wave = []
        # The spawn delay for each enemy
        self.spawn_targets = []
        # Delay for next enemy to be spawned
        self.current_spawn_delay = 0
        # Used to track how many enemies we've created so far
        self.spawn_counter = 0
        # Counter to check if it's time to spawn an enemy yet; start at full
        self.enemy_timer = self.current_spawn_delay
        # Tracks which wave we're on
        self.wave_counter = 1
        # How long to wait between waves
        self.wave_delay = 1000
        # Counter to check if the next wave should start yet
        self.wave_timer = self.wave_delay
        # How many waves to spawn
        self.MAX_WAVE = 10
        # Tracks if we're done spawning enemies
        self.waves_completed = False

        self.enemies_to_remove = []

        self.next_id = 0

    # Create a list of enemies for the manager to use
    def generate_wave(self, canvas, checkpoints, round_num):
        wave = []
        spawn_delays = []
        filename = "Backend/Enemies/Waves/wave" + str(round_num) + ".txt"
        infile = open(filename, "r")
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
                enemy = Enemy(canvas, checkpoints, enemy_type, self.next_id)
                wave.append(enemy)
                self.next_id += 1
            else:
                # Grab spawn delay, clean it up, push to spawn_delays
                delay = raw_text[i]
                delay = delay.replace("\n", "")
                delay = int(delay)
                spawn_delays.append(delay)

        return wave, spawn_delays

    # Moves all enemies towards next checkpoints, and sometimes spawns new ones
    # Returns True if an enemy reaches the end of the map
    def update(self):
        # NOTE: THIS FIRST BLOCK OF CODE IS KIND OF HACKY
        # I'M NOT SURE WHAT WILL HAPPEN IF ONE WAVE SPAWNS WHILE ANOTHER IS STILL ON-SCREEN
        # If not all waves have been spawned
        if self.wave_counter < self.MAX_WAVE:
            # If it's time to spawn a new wave, do so and reset timer
            if self.wave_timer == self.wave_delay:
                self.wave, self.spawn_targets = self.generate_wave(self.canvas, self.checkpoints, self.wave_counter)
                self.wave_counter += 1
                self.wave_timer = 0
                # We also need to reset how many enemies have been spawned
                self.spawn_counter = 0
            # Otherwise, increment timer
            self.wave_timer += 1

        # If not all enemies have been spawned
        if self.spawn_counter < len(self.wave):
            # If it's time to spawn a new one, reset timer and do so
            if self.enemy_timer == self.current_spawn_delay:
                # Pull a new enemy from the wave
                self.enemies.append(self.wave[self.spawn_counter])
                # Grab next timer target
                self.current_spawn_delay = self.spawn_targets[self.spawn_counter]
                self.spawn_counter += 1
                self.enemy_timer = 0
            # Otherwise, increment timer
            self.enemy_timer += 1

        # Advance all spawned enemies
        for enemy in self.enemies:
            enemy.advance()
            # Eliminate if it reaches the last checkpoint
            if enemy.has_reached_goal():
                self.enemies.remove(enemy)
                return True

        # Check for game over
        if self.wave_counter >= self.MAX_WAVE:
            if len(self.enemies) == 0:
                self.waves_completed = True

    # Draws all enemies on the screen
    def render(self, screen):
        # Draw all spawned enemies
        for i in range(len(self.enemies)):
            self.enemies[i].draw()

    # Returns a list of dictionaries, which themselves contain next checkpoint, current x and y coordinates plus an id
    def get_positions(self):
        positions = []

        for enemy in self.enemies:
            # Create a dictionary with next checkpoint, current x coordinate, current y coordinate, and an id
            positions.append({"next_checkpoint": enemy.get_next_checkpoint(),
                              "enemy_x": enemy.get_x(),
                              "enemy_y": enemy.get_y(),
                              "enemy_id": enemy.get_id()})

        return positions

    # Processes damage on a given enemy
    # NOTE: returns 0 if enemy does not exist, returns 1 if enemy damaged, returns 2 if enemy killed
    def deal_damage(self, enemy_id, damage):
        # Check to make sure that the enemy we intend to damage actually exists
        found = False
        for index, enemy in enumerate(self.enemies):
            if enemy.get_id() == enemy_id:
                found = True
                enemy_index = index
                break
        if not found:
            return 0
        # Just calling the damage function in Enemy on the intended target
        if self.enemies[enemy_index].process_damage(damage):
            self.enemies_to_remove.append(enemy_id)
            return 2
        else:
            return 1

    def freeze(self, enemy_id, time):
        # Check to make sure that the enemy we intend to freeze actually exists
        found = False
        for index, enemy in enumerate(self.enemies):
            if enemy.get_id() == enemy_id:
                found = True
                enemy_index = index
                break
        if not found:
            return 0
        else:
            # now call the freeze function if the enemy has been found
            self.enemies[enemy_index].freeze(time)

    def get_waves_completed(self):
        return self.waves_completed

    def clear_dead_enemies(self):
        while self.enemies_to_remove:
            enemy_id = self.enemies_to_remove.pop(0)
            for index, enemy in enumerate(self.enemies):
                if enemy.get_id() == enemy_id:
                    self.enemies.pop(index)
                    break
