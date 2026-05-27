import sys
import pygame


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))  # Fill the screen with black
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 frames per second

        pygame.quit()
        sys.exit()


def main():
    pygame.init()

    game = Game()

    pygame.display.set_caption("Asteroid Panic")

    game.run()


if __name__ == "__main__":
    main()
