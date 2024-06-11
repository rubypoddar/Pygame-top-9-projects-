import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planetary Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load background image
background_image = pygame.image.load()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load images
planet_images = {
    "sun": pygame.image.load(),
    "moon": pygame.image.load(),
    "mercury": pygame.image.load(),
    "venus": pygame.image.load(),
    "earth": pygame.image.load(),
    "mars": pygame.image.load(),
    "jupiter": pygame.image.load(),
    "saturn": pygame.image.load(),
    "uranus": pygame.image.load(),
    "neptune": pygame.image.load(),
    "pluto": pygame.image.load()
}

# Resize images
for key in planet_images:
    if key == "moon":
        planet_images[key] = pygame.transform.scale(planet_images[key], (50, 50))
    else:
        planet_images[key] = pygame.transform.scale(planet_images[key], (50, 50))

# Orbital parameters
planet_params = {
    "mercury": {"distance": 70, "speed": 0.01},
    "venus": {"distance": 120, "speed": 0.008},
    "earth": {"distance": 200, "speed": 0.007},
    "mars": {"distance": 250, "speed": 0.006},
    "jupiter": {"distance": 300, "speed": 0.004},
    "saturn": {"distance": 350, "speed": 0.003},
    "uranus": {"distance": 400, "speed": 0.002},
    "neptune": {"distance": 450, "speed": 0.001},
    "pluto": {"distance": 430, "speed": 0.0005}
}

# Text rendering function
def draw_text(surface, text, pos, color=WHITE, font_size=24):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

# Main game loop
def main():
    clock = pygame.time.Clock()
    running = True
    angle = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background_image, (0, 0))

        # Draw green circles connecting all the planets
        for planet, params in planet_params.items():
            distance = params["distance"]
            pygame.draw.circle(screen, GREEN, (WIDTH // 2, HEIGHT // 2), distance, 1)

        # Draw the sun
        sun_rect = planet_images["sun"].get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(planet_images["sun"], sun_rect)

        # Draw planets and lines connecting them to the sun
        for planet, params in planet_params.items():
            distance = params["distance"]
            speed = params["speed"]
            x = WIDTH // 2 + distance * math.cos(angle * speed)
            y = HEIGHT // 2 + distance * math.sin(angle * speed)
            planet_rect = planet_images[planet].get_rect(center=(x, y))
            screen.blit(planet_images[planet], planet_rect)
            pygame.draw.line(screen, WHITE, (WIDTH // 2, HEIGHT // 2), (x, y))

        angle += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
