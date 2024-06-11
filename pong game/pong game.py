import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong made by Ruby Poddar")

# Load background image
background = pygame.image.load()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load paddle and ball images and resize them
paddle_image = pygame.image.load()
paddle_image = pygame.transform.scale(paddle_image, (120, 120))  # Adjust the size as needed
ball_image = pygame.image.load()
ball_image = pygame.transform.scale(ball_image, (40, 40))  # Adjust the size as needed

# Set up paddles
paddle_width = paddle_image.get_width()
paddle_height = paddle_image.get_height()
paddle_speed = 7

left_paddle = pygame.Rect(50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(screen_width - 50 - paddle_width, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Set up ball
ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)
ball_speed_x = 7
ball_speed_y = 7

# Score variables
left_score = 0
right_score = 0
font = pygame.font.Font(None, 64)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # Control for the left paddle
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < screen_height:
        left_paddle.y += paddle_speed
    # Control for the right paddle
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < screen_height:
        right_paddle.y += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y
    if ball.left <= 0:
        right_score += 1
        ball_speed_x = 7
        ball_speed_y = 7
        ball.x = screen_width // 2 - 15
        ball.y = screen_height // 2 - 15
        if right_score >= 5:
            print("Player 2 wins!")
            left_score = 0
            right_score = 0
    if ball.right >= screen_width:
        left_score += 1
        ball_speed_x = -7
        ball_speed_y = 7
        ball.x = screen_width // 2 - 15
        ball.y = screen_height // 2 - 15
        if left_score >= 5:
            print("Player 1 wins!")
            left_score = 0
            right_score = 0

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x = -ball_speed_x

    # Clear the screen
    screen.blit(background, (0, 0))

    # Draw paddles and ball
    screen.blit(paddle_image, left_paddle)
    screen.blit(paddle_image, right_paddle)
    screen.blit(ball_image, ball)

    # Draw score
    left_text = font.render(str(left_score), True, (255, 255, 255))
    right_text = font.render(str(right_score), True, (255, 255, 255))
    screen.blit(left_text, (screen_width // 4 - 20, 20))
    screen.blit(right_text, (3 * screen_width // 4 - 20, 20))

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(30)
