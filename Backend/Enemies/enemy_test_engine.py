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
enemy1 = enemy.Enemy()

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    canvas.fill(background)
    pygame.draw.rect(canvas, path, pygame.Rect(30, 0, 60, 400))
    pygame.draw.rect(canvas, path, pygame.Rect(90, 340, 220, 60))
    pygame.draw.rect(canvas, path, pygame.Rect(250, 150, 60, 190))
    pygame.draw.rect(canvas, path, pygame.Rect(300, 150, 250, 60))
    enemy1.draw(canvas)
    enemy1.advance()
    pygame.display.update()

