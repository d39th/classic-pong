import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
PAD_WIDTH = 10
PAD_HEIGHT = 100
BALL_RADIUS = 10
BALL_SPEED = 5
PAD_SPEED = 5
SCORE_TO_WIN = 5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Initialize paddles and ball
player1_pos = HEIGHT // 2 - PAD_HEIGHT // 2
player2_pos = HEIGHT // 2 - PAD_HEIGHT // 2
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [random.choice([BALL_SPEED, -BALL_SPEED]), random.choice([BALL_SPEED, -BALL_SPEED])]
player1_score = 0
player2_score = 0

# Function to draw paddles
def draw_paddles():
    pygame.draw.rect(screen, WHITE, (0, player1_pos, PAD_WIDTH, PAD_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - PAD_WIDTH, player2_pos, PAD_WIDTH, PAD_HEIGHT))

# Function to draw ball
def draw_ball():
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_RADIUS)

# Function to display scoreboard
def display_score():
    font = pygame.font.Font(None, 36)
    player1_text = font.render(f"Player 1: {player1_score}", True, WHITE)
    player2_text = font.render(f"Player 2: {player2_score}", True, WHITE)
    screen.blit(player1_text, (50, 50))
    screen.blit(player2_text, (WIDTH - 200, 50))

# Function to move the bot (computer player)
def move_bot():
    global player2_pos
    if ball_pos[1] > player2_pos + PAD_HEIGHT // 2:
        player2_pos += PAD_SPEED
    elif ball_pos[1] < player2_pos + PAD_HEIGHT // 2:
        player2_pos -= PAD_SPEED

# Function to check collision with walls
def check_collision_with_walls():
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1

# Function to check collision with paddles
def check_collision_with_paddles():
    global player1_score, player2_score, ball_pos, ball_vel

    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS and player1_pos <= ball_pos[1] <= player1_pos + PAD_HEIGHT:
        ball_vel[0] *= -1
    elif ball_pos[0] <= BALL_RADIUS:
        player2_score += 1
        reset_ball()

    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS and player2_pos <= ball_pos[1] <= player2_pos + PAD_HEIGHT:
        ball_vel[0] *= -1
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        player1_score += 1
        reset_ball()

# Function to reset ball position and velocity
def reset_ball():
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_vel = [random.choice([BALL_SPEED, -BALL_SPEED]), random.choice([BALL_SPEED, -BALL_SPEED])]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the bot
    move_bot()

    # Move paddles based on input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1_pos -= PAD_SPEED
    if keys[pygame.K_s]:
        player1_pos += PAD_SPEED

    # Move ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Clear screen
    screen.fill(BLACK)

    # Draw paddles and ball
    draw_paddles()
    draw_ball()

    # Check collision with walls and paddles
    check_collision_with_walls()
    check_collision_with_paddles()

    # Display scoreboard
    display_score()

    # Check for game over
    if player1_score >= SCORE_TO_WIN or player2_score >= SCORE_TO_WIN:
        player1_score = 0
        player2_score = 0

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
