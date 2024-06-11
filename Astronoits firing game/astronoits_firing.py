import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the screen
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid Avoid")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the game clock
clock = pygame.time.Clock()
FPS = 60

# Load and resize images
player_img = pygame.image.load()
player_img = pygame.transform.scale(player_img, (100, 100))  # Resizing player image

enemy_img = pygame.image.load()
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  # Resizing enemy image

background_img = pygame.image.load()
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Resizing background image

bullet_img = pygame.image.load()
bullet_img = pygame.transform.scale(bullet_img, (30, 30))  # Resizing bullet image

planet_img = pygame.image.load()
planet_img = pygame.transform.scale(planet_img, (200, 200))  # Resizing planet image

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self, planet):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(midbottom=planet.rect.midtop)
        self.speed = 8

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if pressed_keys[K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(40, 460), random.randint(-100, 0)))
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.center = (random.randint(30, 460), random.randint(-100, 0))
            self.speed = random.randint(3, 5)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(midtop=player.rect.midtop)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = planet_img
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create planet instance
planet = Planet()
all_sprites.add(planet)

# Create player instance
player = Player(planet)
all_sprites.add(player)

# Set up font for displaying score
font = pygame.font.Font(None, 36)

# Main game loop
running = True
score = 0
enemy_spawn_timer = 0  # Initialize enemy spawn timer
enemy_spawn_interval = random.randint(60, 120)  # Initial interval for enemy spawning
game_over = False

while running:
    clock.tick(FPS)
    window.fill(BLACK)
    window.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if not game_over:
        # Update enemies
        enemies.update()

        # Check for collisions between enemies and player
        if pygame.sprite.spritecollide(player, enemies, False):
            game_over = True

        # Update player
        player.update()

        # Check for bullet firing
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            bullet = Bullet(player)
            bullets.add(bullet)
            all_sprites.add(bullet)

        # Update bullets
        bullets.update()

        # Check for collisions between enemies and bullets
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
            score += 1

        # Spawn enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
            enemy_spawn_timer = 0
            enemy_spawn_interval = random.randint(60, 120)  # Randomize next spawn interval

    # Draw all sprites
    all_sprites.draw(window)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

    # Display game over message if game is over
    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        window.blit(game_over_text, (WINDOW_WIDTH // 1 - 100, WINDOW_HEIGHT // 1.0))

    pygame.display.flip()

pygame.quit()
