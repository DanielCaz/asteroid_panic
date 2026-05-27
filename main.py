import random
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
        return self.clock.tick(self.FPS) / 1000

    @staticmethod
    def cleanup():
        pygame.quit()
        sys.exit()


class Spaceship:
    SPEED = 5

    def __init__(self):
        self.image = pygame.Surface((30, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.start_pos = (240, 590)
        self.rect.center = self.start_pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def handle_input(self, keys, can_move=True):
        if not can_move:
            return

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

    def reset(self):
        self.rect.center = self.start_pos


class FuelSystem:
    MAX_FUEL = 100
    DRAIN_PER_SECOND = 5
    REFUEL_AMOUNT = 30

    def __init__(self):
        self.fuel = float(self.MAX_FUEL)
        self.font = pygame.font.SysFont("arial", 22)
        self.bar_position = (16, 16)
        self.bar_size = (180, 18)

    def update(self, dt):
        self.fuel = max(0.0, self.fuel - self.DRAIN_PER_SECOND * dt)

    def refuel(self):
        self.fuel = min(float(self.MAX_FUEL), self.fuel + self.REFUEL_AMOUNT)

    def reset(self):
        self.fuel = float(self.MAX_FUEL)

    def has_fuel(self):
        return self.fuel > 0

    def draw(self, screen):
        x, y = self.bar_position
        width, height = self.bar_size
        ratio = self.fuel / self.MAX_FUEL
        fill_width = int(width * ratio)

        if ratio > 0.5:
            color = (60, 220, 60)
        elif ratio > 0.25:
            color = (245, 185, 50)
        else:
            color = (220, 60, 60)

        pygame.draw.rect(screen, (80, 80, 80), (x, y, width, height))
        pygame.draw.rect(screen, color, (x, y, fill_width, height))
        pygame.draw.rect(screen, (240, 240, 240), (x, y, width, height), 2)

        text = self.font.render(f"Fuel: {int(self.fuel)}", True, (240, 240, 240))
        screen.blit(text, (x, y + height + 6))


class JerryCan:
    SIZE = (20, 28)

    def __init__(self, center_pos, spawn_time, lifetime_ms):
        self.image = pygame.Surface(self.SIZE)
        self.image.fill((210, 35, 35))
        self.rect = self.image.get_rect(center=center_pos)
        self.spawn_time = spawn_time
        self.lifetime_ms = lifetime_ms

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_expired(self, now):
        return now - self.spawn_time >= self.lifetime_ms


class Asteroid:
    SPEED = 3

    def __init__(self):
        self.image = pygame.Surface((40, 40))
        self.image.fill((128, 128, 128))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, Game.SCREEN_SIZE[0] - self.rect.width)
        self.rect.y = -self.rect.height

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.SPEED

    def is_off_screen(self):
        return self.rect.top > Game.SCREEN_SIZE[1]


class AsteroidPanicState:
    ASTEROID_SPAWN_DELAY_RANGE_MS = (250, 850)
    JERRY_CAN_SPAWN_DELAY_RANGE_MS = (2800, 7000)
    JERRY_CAN_LIFETIME_MS = 2400
    JERRY_CAN_POSITIONS = [
        (70, 150),
        (240, 180),
        (410, 150),
        (120, 360),
        (360, 380),
        (240, 520),
    ]

    def __init__(self, now):
        self.spaceship = Spaceship()
        self.fuel_system = FuelSystem()
        self.asteroids = []
        self.jerry_can = None

        self.next_asteroid_spawn_time = self._schedule_next(
            now, self.ASTEROID_SPAWN_DELAY_RANGE_MS
        )
        self.next_jerry_can_spawn_time = self._schedule_next(
            now, self.JERRY_CAN_SPAWN_DELAY_RANGE_MS
        )

    @staticmethod
    def _schedule_next(now, delay_range_ms):
        return now + random.randint(*delay_range_ms)

    def reset_run(self, now):
        self.spaceship.reset()
        self.fuel_system.reset()
        self.asteroids.clear()
        self.jerry_can = None
        self.next_asteroid_spawn_time = self._schedule_next(
            now, self.ASTEROID_SPAWN_DELAY_RANGE_MS
        )
        self.next_jerry_can_spawn_time = self._schedule_next(
            now, self.JERRY_CAN_SPAWN_DELAY_RANGE_MS
        )

    def _spawn_asteroid_if_due(self, now):
        if now < self.next_asteroid_spawn_time:
            return

        self.asteroids.append(Asteroid())
        self.next_asteroid_spawn_time = self._schedule_next(
            now, self.ASTEROID_SPAWN_DELAY_RANGE_MS
        )

    def _spawn_jerry_can_if_due(self, now):
        if self.jerry_can is not None or now < self.next_jerry_can_spawn_time:
            return

        self.jerry_can = JerryCan(
            random.choice(self.JERRY_CAN_POSITIONS),
            now,
            self.JERRY_CAN_LIFETIME_MS,
        )

    def _resolve_jerry_can_interaction(self, now):
        if self.jerry_can is None:
            return

        if self.jerry_can.is_expired(now):
            self.jerry_can = None
            self.next_jerry_can_spawn_time = self._schedule_next(
                now, self.JERRY_CAN_SPAWN_DELAY_RANGE_MS
            )
            return

        if self.spaceship.rect.colliderect(self.jerry_can.rect):
            self.fuel_system.refuel()
            self.jerry_can = None
            self.next_jerry_can_spawn_time = self._schedule_next(
                now, self.JERRY_CAN_SPAWN_DELAY_RANGE_MS
            )

    def _hit_asteroid(self):
        return any(
            self.spaceship.rect.colliderect(asteroid.rect)
            for asteroid in self.asteroids
        )

    def update(self, keys, dt, now):
        self.fuel_system.update(dt)
        if not self.fuel_system.has_fuel():
            self.reset_run(now)
            return

        self.spaceship.handle_input(keys, can_move=True)
        self._spawn_asteroid_if_due(now)
        self._spawn_jerry_can_if_due(now)

        for asteroid in self.asteroids:
            asteroid.update()

        self._resolve_jerry_can_interaction(now)

        if self._hit_asteroid():
            self.reset_run(now)
            return

        self.asteroids = [
            asteroid for asteroid in self.asteroids if not asteroid.is_off_screen()
        ]

    def draw(self, screen):
        self.spaceship.draw(screen)

        for asteroid in self.asteroids:
            asteroid.draw(screen)

        if self.jerry_can:
            self.jerry_can.draw(screen)

        self.fuel_system.draw(screen)


def main():
    pygame.init()

    game = Game()
    state = AsteroidPanicState(pygame.time.get_ticks())
    dt = 1 / Game.FPS

    while game.running:
        game.handle_events()
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        state.update(keys, dt, now)

        game.begin_frame()
        state.draw(game.screen)
        dt = game.end_frame()


if __name__ == "__main__":
    main()
