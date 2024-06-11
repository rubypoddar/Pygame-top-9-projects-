import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Constants
WIN_HEIGHT = 720
WIN_WIDTH = 551
SCROLL_SPEED = 3
BIRD_START_POSITION = (100, 250)
GRAVITY = 0.5
FLAP_STRENGTH = -7
PIPE_FREQUENCY = (180, 250)  # min and max time between pipe spawns
PIPE_GAP = 325  # gap between pipes
FONT_SIZE = 26

# Load and scale images
bird_image = pygame.image.load()
bird_image = pygame.transform.scale(bird_image, (100, 50))  # smaller bird size
skyline_image = pygame.image.load()
skyline_image = pygame.transform.scale(skyline_image, (WIN_WIDTH, WIN_HEIGHT))
pipe_image = pygame.image.load()
pipe_image = pygame.transform.scale(pipe_image, (300, 800))  # adjust pipe size
game_over_image = pygame.image.load()
start_image = pygame.image.load()

# Font
font = pygame.font.SysFont('Segoe', FONT_SIZE)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = bird_image
        self.image = self.original_image
        self.rect = self.image.get_rect(center=BIRD_START_POSITION)
        self.vel = 0
        self.alive = True

    def update(self, user_input):
        if self.alive:
            self.vel += GRAVITY
            self.vel = min(self.vel, 7)
            self.rect.y += int(self.vel)

            if user_input[K_SPACE] and self.rect.y > 0:
                self.vel = FLAP_STRENGTH
            elif user_input[K_UP] and self.rect.y > 0:
                self.vel = FLAP_STRENGTH  # Move bird upward when up key is pressed
            elif user_input[K_DOWN]:
                self.vel += GRAVITY  # Apply gravity when down key is pressed

            # No need to rotate dynamically, use pre-rotated images
            if self.vel >= 0:
                self.image = self.original_image
            else:
                self.image = pygame.transform.flip(self.original_image, False, True)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right <= 0:
            self.kill()

def quit_game():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

def display_score(window, score):
    score_text = font.render(f'Score: {score}', True, pygame.Color(255, 255, 255))
    window.blit(score_text, (20, 20))

def game_over(window):
    window.blit(game_over_image, (WIN_WIDTH // 2 - game_over_image.get_width() // 2,
                                  WIN_HEIGHT // 2 - game_over_image.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def play_game(window):
    global score
    score = 0

    bird = Bird()
    bird_group = pygame.sprite.GroupSingle(bird)

    pipes = pygame.sprite.Group()

    pipe_timer = random.randint(*PIPE_FREQUENCY)

    while True:
        quit_game()
        window.blit(skyline_image, (0, 0))
        pipes.draw(window)
        bird_group.draw(window)
        display_score(window, score)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        if bird.alive:
            pipes.update()
            bird_group.update(pygame.key.get_pressed())

            # Check for collision with pipes
            for pipe in pipes:
                if bird.rect.colliderect(pipe.rect):
                    if pipe.rect.bottom > bird.rect.top and pipe.rect.top < bird.rect.bottom:
                        bird.alive = False

            if pipe_timer <= 0:
                pipe_height = random.randint(-600, -300)
                pipes.add(Pipe(WIN_WIDTH, pipe_height, pipe_image))
                pipes.add(Pipe(WIN_WIDTH, pipe_height + PIPE_GAP + pipe_image.get_height(), pipe_image))
                pipe_timer = random.randint(*PIPE_FREQUENCY)
            pipe_timer -= 1
            
            if bird.rect.top >= WIN_HEIGHT or bird.rect.bottom <= 0:
                bird.alive = False

            for pipe in pipes:
                if pipe.rect.right == bird.rect.left:
                    score += 1

        else:
            game_over(window)
            return

        clock.tick(60)
        pygame.display.update()

def menu(window):
    while True:
        quit_game()
        window.blit(skyline_image, (0, 0))
        window.blit(bird_image, BIRD_START_POSITION)
        window.blit(start_image, (WIN_WIDTH // 2 - start_image.get_width() // 2,
                                  WIN_HEIGHT // 2 - start_image.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    play_game(window)

if __name__ == "__main__":
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird By Ruby Poddar")
    menu(window)
