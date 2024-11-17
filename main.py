import pygame
from Backend.game_manager import GameManager

SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 1200, 700, 120

def main():
    pygame.init()


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    game_manager = GameManager(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game_manager.handle_events(event)

        game_manager.update()

        game_manager.render()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()