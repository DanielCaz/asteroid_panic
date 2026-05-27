import sys
import pygame


class Game:
    FPS = 60
    SCREEN_SIZE = (480, 680)
    BACKGROUND_COLOR = (0, 0, 0)

    def __init__(self):
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def begin_frame(self):
        self.screen.fill(self.BACKGROUND_COLOR)

    def end_frame(self):
        pygame.display.flip()
        self.clock.tick(self.FPS)

    @staticmethod
    def cleanup():
        pygame.quit()
        sys.exit()


class Spaceship:
    SPEED = 5

    def __init__(self):
        self.image = pygame.Surface((30, 50))  # Placeholder for spaceship image
        self.image.fill((255, 255, 255))  # Fill with white color
        self.rect = self.image.get_rect()
        self.rect.center = (240, 590)  # Start in the center-bottom of the screen

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def handle_input(self, keys):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.SPEED
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.SPEED

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        elif self.rect.right + dx > Game.SCREEN_SIZE[0]:
            dx = Game.SCREEN_SIZE[0] - self.rect.right

        if self.rect.top + dy < 0:
            dy = -self.rect.top
        elif self.rect.bottom + dy > Game.SCREEN_SIZE[1]:
            dy = Game.SCREEN_SIZE[1] - self.rect.bottom

        self.move(dx, dy)


def main():
    pygame.init()

    game = Game()
    spaceship = Spaceship()

    while game.running:
        game.handle_events()

        spaceship.handle_input(pygame.key.get_pressed())

        game.begin_frame()
        spaceship.draw(game.screen)  # Draw the spaceship
        game.end_frame()

    game.cleanup()


if __name__ == "__main__":
    main()
