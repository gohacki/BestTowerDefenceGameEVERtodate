import pygame
from enemy import Enemy


class Wave:
    def __init__(self, canvas, checkpoints, quantity):
        # List of enemies in the current wave
        self.enemies = []
        # Used to track how many enemies we've created so far
        self.spawn_counter = 0
        # How many enemies we want to create
        self.spawn_target = quantity
        # How long to wait between spawning enemies
        self.timer_target = 750
        # Counter to check if it's time to spawn an enemy yet; start at full
        self.timer_counter = self.timer_target

        # Populate list
        for i in range(self.spawn_target):
            self.enemies.append(Enemy(canvas, checkpoints))

    def update(self):
        # If not all have been spawned
        if self.spawn_counter < self.spawn_target:
            # If it's time to spawn a new one, reset timer and allow next spawn
            if self.timer_counter == self.timer_target:
                self.timer_counter = 0
                self.spawn_counter += 1
            # Otherwise, increment timer
            self.timer_counter += 1

        # Advance all spawned enemies
        for i in range(self.spawn_counter):
            self.enemies[i].advance()

    def render(self, screen):
        # Draw all spawned enemies
        for i in range(self.spawn_counter):
            self.enemies[i].draw()