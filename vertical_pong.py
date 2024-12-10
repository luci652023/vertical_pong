import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Get screen dimensions
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Vertical Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()

# Adjustable speeds
PADDLE_SPEED = 10  # Paddle speed
BALL_SPEED_X = 5  # Initial horizontal ball speed
BALL_SPEED_Y = -5  # Initial vertical ball speed
BALL_SPEED_INCREMENT = 0.5  # Amount to increase ball speed over time

# Paddle properties
PADDLE_WIDTH = WIDTH // 8
PADDLE_HEIGHT = 10

# Ball properties
BALL_SIZE = WIDTH // 40


# Function to calculate font size based on screen height
def get_font_size(screen_height, percentage=0.075):
    return int(screen_height * percentage)


# Adjust font size based on screen height
font_size = get_font_size(HEIGHT)  # Font size is 7.5% of screen height
font = pygame.font.Font(None, font_size)

# High score
high_score = 0


def reset_game():
    """Resets the game to its initial state."""
    global paddle_x, paddle_y, ball_x, ball_y, ball_dx, ball_dy, score, running, current_speed
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    paddle_y = HEIGHT - 30
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
    ball_dy = BALL_SPEED_Y
    score = 0
    current_speed = abs(ball_dx)  # Reset the current ball speed
    running = True


def draw_objects():
    """Draws the paddle, ball, score, and high score."""
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, RED, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw current score
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, font_size))
    screen.blit(score_text, score_text_rect)

    # Draw high score
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    high_score_text_rect = high_score_text.get_rect(center=(WIDTH // 2, font_size * 2))
    screen.blit(high_score_text, high_score_text_rect)

    pygame.display.flip()


def game_over_screen():
    """Displays the 'Game Over' screen and waits for user input to restart or quit."""
    global high_score
    if score > high_score:
        high_score = score  # Update high score

    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    restart_text = font.render("Press R to Restart or ESC to Quit", True, WHITE)
    screen.blit(
        game_over_text,
        (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100),
    )
    screen.blit(
        final_score_text,
        (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 50),
    )
    screen.blit(
        high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2)
    )
    screen.blit(
        restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50)
    )
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# Initialize game state
reset_game()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # Get key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += PADDLE_SPEED

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with walls
    if ball_x <= 0 or ball_x >= WIDTH - BALL_SIZE:
        ball_dx = -ball_dx
    if ball_y <= 0:
        ball_dy = -ball_dy

    # Ball collision with paddle
    if (
        paddle_y < ball_y + BALL_SIZE < paddle_y + PADDLE_HEIGHT
        and paddle_x < ball_x + BALL_SIZE
        and ball_x < paddle_x + PADDLE_WIDTH
    ):
        ball_dy = -ball_dy
        score += 1

        # Increase ball speed slightly
        current_speed = abs(ball_dx) + BALL_SPEED_INCREMENT
        ball_dx = current_speed if ball_dx > 0 else -current_speed
        ball_dy = -current_speed

    # Check if the ball goes off the screen
    if ball_y > HEIGHT:
        running = False

    if not running:
        game_over_screen()

    draw_objects()
    clock.tick(60)
