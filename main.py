import sys
import pygame
import random


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


class Asteroid:
    SPEED = 3

    def __init__(self):
        self.image = pygame.Surface((30, 30))  # Placeholder for asteroid image
        self.image.fill((128, 128, 128))  # Fill with gray color
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, Game.SCREEN_SIZE[0] - self.rect.width)
        self.rect.y = -self.rect.height  # Start above the screen

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.SPEED

    def is_off_screen(self):
        return self.rect.top > Game.SCREEN_SIZE[1]


def main():
    pygame.init()

    game = Game()
    spaceship = Spaceship()
    asteroids = []
    spawn_delay_range_ms = (250, 850)
    next_spawn_time = pygame.time.get_ticks() + random.randint(*spawn_delay_range_ms)

    while game.running:
        game.handle_events()
        keys = pygame.key.get_pressed()
        spaceship.handle_input(keys)

        now = pygame.time.get_ticks()
        if now >= next_spawn_time:
            asteroids.append(Asteroid())
            next_spawn_time = now + random.randint(*spawn_delay_range_ms)

        for asteroid in asteroids:
            asteroid.update()

        asteroids = [asteroid for asteroid in asteroids if not asteroid.is_off_screen()]

        game.begin_frame()
        spaceship.draw(game.screen)
        for asteroid in asteroids:
            asteroid.draw(game.screen)
        game.end_frame()


if __name__ == "__main__":
    main()
