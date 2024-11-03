import pygame
from enemy_manager import EnemyManager

'''FOR TESTING ENEMY BEHAVIOR ONLY'''

pygame.init()

# CREATING CANVAS
# Note: SLightly different canvas size than real game
canvas = pygame.display.set_mode((1200, 600))
# Colors for background art
background = (19, 133, 16)
path = (131, 101, 57)

# TITLE OF CANVAS
pygame.display.set_caption("My Board")
exit = False

# CREATING ENTITIES
checkpoints = ((50, 0), (50, 400), (800, 400))
test = EnemyManager(canvas, checkpoints)

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    # Draw background art
    canvas.fill(background)
    pygame.draw.rect(canvas, path, pygame.Rect(50, 0, 50, 400))
    pygame.draw.rect(canvas, path, pygame.Rect(50, 400, 800, 50))
    # Call functions from Enemy
    test.update()
    test.render(canvas)
    test.deal_damage(0, 1)

    pygame.display.update()

