import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Molecule Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
COLORS = [WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE, GRAY]

# Settings
attraction = 0.0005
friction = 0.2
light = True
transparent = False
color_index = 0
color = COLORS[color_index]

# Molecule class
class Molecule:
    def __init__(self, x, y, vx, vy, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color

    def move(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x <= self.radius or self.x >= width - self.radius:
            self.vx *= -1
            self.vx *= friction
        if self.y <= self.radius or self.y >= height - self.radius:
            self.vy *= -1
            self.vy *= friction

    def draw(self):
        if not transparent:
            if light:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            else:
                pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius)

def distance(molecule1, molecule2):
    dx = molecule1.x - molecule2.x
    dy = molecule1.y - molecule2.y
    return math.sqrt(dx ** 2 + dy ** 2)

# Create molecules
molecules = []
num_molecules = 50
for _ in range(num_molecules):
    radius = random.randint(2, 8)
    x = random.randint(radius, width - radius)
    y = random.randint(radius, height - radius)
    vx = random.uniform(-1, 1)
    vy = random.uniform(-1, 1)
    molecules.append(Molecule(x, y, vx, vy, radius, color))

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                radius = random.randint(2, 8)
                angle = random.uniform(0, 2 * math.pi)
                vx = 2 + random.uniform(-1, 1) * math.cos(angle)
                vy = 2 + random.uniform(-1, 1) * math.sin(angle)
                molecules.append(Molecule(mouse_x, mouse_y, vx, vy, radius, color))
            elif event.button == 3:  # Right click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for molecule in molecules:
                    if math.sqrt((molecule.x - mouse_x) ** 2 + (molecule.y - mouse_y) ** 2) <= molecule.radius:
                        molecules.remove(molecule)
                        break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Change color
                color_index = (color_index + 1) % len(COLORS)
                color = COLORS[color_index]
            elif event.key == pygame.K_d:  # Delete all molecules
                molecules = []
            elif event.key == pygame.K_t:  # Toggle transparency
                transparent = not transparent

    screen.fill(BLACK)

    # Move and draw molecules
    for molecule in molecules:
        molecule.move()
        molecule.draw()

    # Draw connections and apply attraction
    for i, molecule1 in enumerate(molecules):
        for j in range(i + 1, len(molecules)):
            molecule2 = molecules[j]
            if distance(molecule1, molecule2) < 100:
                pygame.draw.line(screen, color, (int(molecule1.x), int(molecule1.y)), (int(molecule2.x), int(molecule2.y)), 1)
                
                # Apply attraction force
                attractionX = (molecule1.x - molecule2.x) * attraction
                attractionY = (molecule1.y - molecule2.y) * attraction
                
                molecule1.vx -= attractionX
                molecule1.vy -= attractionY
                
                molecule2.vx += attractionX
                molecule2.vy += attractionY

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
