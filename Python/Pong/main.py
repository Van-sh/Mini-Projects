# Please don't roast my code ;-;
import sys

import pygame

# Importing classes.
from classes import Ball, Button, Player

# Initialising pygame.
pygame.init()

# Initialising colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialising Font
PIXELADE_FONT_50 = pygame.font.Font("./Fonts/PIXELADE.ttf", 50)
PIXELADE_FONT_100 = pygame.font.Font("./Fonts/PIXELADE.ttf", 100)

# Initialising size of the window.
SIZE = WIDTH, HEIGHT = 600, 450
# Initialising the window.
WIN = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pong")
# Creating a clock object.
CLOCK = pygame.time.Clock()
# Initialising FPS
FPS = 60

# Initialising sprites
PONG_TEXT = PIXELADE_FONT_100.render("PONG", False, WHITE)
player1 = Player(20, WHITE, HEIGHT)
player2 = Player(570, WHITE, HEIGHT)
ball = Ball(WHITE, WIDTH, HEIGHT)
play_button = Button(100, 300, "PLAY", BLACK, WHITE, PIXELADE_FONT_50)

game_state = "MENU"

# Main loop.
while True:
    dt = CLOCK.tick(FPS)
    # Event loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == "MENU":
            if play_button.mouse_colliding() and pygame.mouse.get_pressed()[0]:
                game_state = "GAME"
        if game_state == "GAME":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1.dy = -0.3
                if event.key == pygame.K_s:
                    player1.dy = 0.3
                if event.key == pygame.K_UP:
                    player2.dy = -0.3
                if event.key == pygame.K_DOWN:
                    player2.dy = 0.3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player1.dy = 0
                if event.key == pygame.K_s:
                    player1.dy = 0
                if event.key == pygame.K_UP:
                    player2.dy = 0
                if event.key == pygame.K_DOWN:
                    player2.dy = 0

    # Updating sprites.
    if game_state == "MENU":
        play_button.update()
    if game_state == "GAME":
        player1.update(dt, HEIGHT)
        player2.update(dt, HEIGHT)
        ball.update(dt, WIDTH, HEIGHT, player1, player2)

    # Drawing frame.
    WIN.fill(BLACK)
    if game_state == "MENU":
        WIN.blit(PONG_TEXT, PONG_TEXT.get_rect(center=(300, 100)))
        play_button.draw(WIN)
    if game_state == "GAME":
        pygame.draw.rect(WIN, WHITE, pygame.Rect(WIDTH // 2 - 1, 0, 2, HEIGHT))
        player1_score_text = PIXELADE_FONT_100.render(str(player1.score), False, WHITE)
        WIN.blit(
            player1_score_text, player1_score_text.get_rect(midtop=(WIDTH // 4 + 5, 0))
        )
        player2_score_text = PIXELADE_FONT_100.render(str(player2.score), False, WHITE)
        WIN.blit(
            player2_score_text,
            player2_score_text.get_rect(topleft=(WIDTH // 4 * 3 - 15, 0)),
        )
        player1.draw(WIN)
        player2.draw(WIN)
        ball.draw(WIN)
    pygame.display.update()
