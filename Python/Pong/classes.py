import random

import pygame


class Player:
    def __init__(self, x: int, COLOUR: tuple, WIN_HEIGHT: int) -> None:
        self.SIZE = self.WIDTH, self.HEIGHT = 10, 80
        self.drag = 0
        self.pos = pygame.math.Vector2(x, (WIN_HEIGHT - self.HEIGHT) // 2)
        self.dy = 0
        self.surface = pygame.Surface(self.SIZE)
        self.surface.fill(COLOUR)
        self.score = 0

    def update(self, dt: float, WIN_HEIGHT: int) -> None:
        self.pos.y += self.dy * dt
        self.rect = self.surface.get_rect(topleft=(self.pos.x, self.pos.y))
        if self.rect.top < 0:
            self.pos.y = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.pos.y = WIN_HEIGHT - self.HEIGHT

    def draw(self, WIN) -> None:
        WIN.blit(self.surface, self.pos)


class Ball:
    def __init__(self, COLOUR: tuple, WIN_WIDTH: int, WIN_HEIGHT: int) -> None:
        self.SIZE = self.WIDTH, self.HEIGHT = 10, 10
        self.pos = pygame.math.Vector2(
            (WIN_WIDTH - self.WIDTH) // 2, (WIN_HEIGHT - self.HEIGHT) // 2
        )
        self.dx = random.choice([-1, 1]) * random.randrange(10, 15) / 100
        self.dy = random.choice([-1, 1]) * random.randrange(10, 15) / 100
        self.surface = pygame.Surface(self.SIZE)
        self.surface.fill(COLOUR)

    def update(
        self,
        dt: float,
        WIN_WIDTH: int,
        WIN_HEIGHT: int,
        player1: Player,
        player2: Player,
    ) -> None:
        self.pos.x += self.dx * dt
        self.pos.y += self.dy * dt
        self.rect = self.surface.get_rect(topleft=(self.pos.x, self.pos.y))
        if self.rect.top <= 0 or self.rect.bottom >= WIN_HEIGHT:
            self.dy = -self.dy
            self.pos.y += self.dy * dt
        if self.rect.left <= 0:
            player2.score += 1
            self.reset(WIN_WIDTH, WIN_HEIGHT)
        if self.rect.right >= WIN_WIDTH:
            player1.score += 1
            self.reset(WIN_WIDTH, WIN_HEIGHT)
        if self.rect.colliderect(player1.rect):
            self.dx *= -1.05
            self.dy += player1.dy / 10
            self.pos.x += 15
        if self.rect.colliderect(player2.rect):
            self.dx *= -1.05
            self.dy += player2.dy / 10
            self.pos.x -= 10

    def draw(self, WIN) -> None:
        WIN.blit(self.surface, self.pos)

    def reset(self, WIN_WIDTH: int, WIN_HEIGHT: int) -> None:
        self.pos.x = WIN_WIDTH // 2 - self.WIDTH // 2
        self.pos.y = WIN_HEIGHT // 2 - self.HEIGHT // 2
        self.dx = random.choice([-1, 1]) * 15 / 100
        self.dy = random.randrange(-15, 15) / 100


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        BG_COLOUR: tuple,
        FG_COLOUR: tuple,
        FONT: pygame.font.Font,
    ) -> None:
        self.SIZE = self.WIDTH, self.HEIGHT = 400, 75
        self.pos = pygame.math.Vector2(x, y)
        self.BG_COLOUR, self.FG_COLOUR = BG_COLOUR, FG_COLOUR
        self.FONT = FONT
        self.text = text
        self.surface = pygame.Surface(self.SIZE)
        self._secondary_surface = pygame.Surface((self.WIDTH - 10, self.HEIGHT - 10))

    def update(self) -> None:
        if self.mouse_colliding():
            self.surface.fill(self.BG_COLOUR)
            self._secondary_surface.fill(self.FG_COLOUR)
            self._rendered_font = self.FONT.render(self.text, False, self.BG_COLOUR)
        else:
            self.surface.fill(self.FG_COLOUR)
            self._secondary_surface.fill(self.BG_COLOUR)
            self._rendered_font = self.FONT.render(self.text, False, self.FG_COLOUR)

    def draw(self, WIN) -> None:
        self.surface.blit(self._secondary_surface, (5, 5))
        self.surface.blit(
            self._rendered_font,
            self._rendered_font.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2)),
        )
        WIN.blit(self.surface, self.pos)

    def mouse_colliding(self) -> bool:
        return self.surface.get_rect(topleft=self.pos).collidepoint(
            pygame.mouse.get_pos()
        )
