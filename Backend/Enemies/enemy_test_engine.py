import pygame
import enemy

'''FOR TESTING ENEMY BEHAVIOR ONLY'''

pygame.init()

# CREATING CANVAS
canvas = pygame.display.set_mode((1200, 600))
background = (19, 133, 16)
path = (131, 101, 57)

# TITLE OF CANVAS
pygame.display.set_caption("My Board")
exit = False

# CREATING ENTITIES
checkpoints = ((50, 0), (50, 400), (800, 400))
enemy1 = enemy.Enemy(canvas, checkpoints)

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    canvas.fill(background)
    pygame.draw.rect(canvas, path, pygame.Rect(50, 0, 50, 400))
    pygame.draw.rect(canvas, path, pygame.Rect(50, 400, 800, 50))

    enemy1.draw()
    enemy1.advance()
    pygame.display.update()

