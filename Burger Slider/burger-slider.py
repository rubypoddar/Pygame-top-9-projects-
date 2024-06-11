import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BURGER_IMG_PATH =  (File_Path) 
BACKGROUND_IMG_PATH = (File_Path)
# Colors
WHITE = (255, 255, 255)
BLUE = (73, 99, 204)

# Load images
try:
    burger_image = pygame.image.load(BURGER_IMG_PATH)
    burger_image = pygame.transform.scale(burger_image, (50, 50))
    background_image = pygame.image.load(BACKGROUND_IMG_PATH)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Unable to load image: {e}")
    pygame.quit()
    sys.exit()

# Utility functions
def get_random_int(min, max):
    return random.uniform(min, max)

# Point class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def delta(self, point):
        return self.x - point.x, self.y - point.y

    def distance(self, point):
        dx = point.x - self.x
        dy = point.y - self.y
        return math.sqrt(dx * dx + dy * dy)

    def apply_velocity(self, velocity):
        self.x += velocity.vx
        self.y += velocity.vy

    def angle_radians(self, point):
        y = point.y - self.y
        x = point.x - self.x
        return math.atan2(y, x)

# Velocity class
class Velocity:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def flip_x(self):
        self.vx *= -1

    def flip_y(self):
        self.vy *= -1

    def multiply(self, scalar):
        self.vx *= scalar
        self.vy *= scalar

# Explosion class
class Explosion:
    def __init__(self, power, multiplier, center):
        self.center = center
        self.power = power
        self.color = BLUE
        self.radius = 1
        self.opacity = 0.5
        self.multiplier = multiplier
        self.dead = False

    def update(self):
        self.radius += self.power
        self.power *= 0.95
        if self.power < 0.01:
            self.dead = True

    def draw(self, screen):
        if not self.dead:
            pygame.draw.circle(screen, self.color, (int(self.center.x), int(self.center.y)), int(self.radius * self.multiplier), int(self.radius * self.multiplier // 2))

# Burger class
class Burger:
    def __init__(self, center, radius, velocity):
        self.center = center
        self.radius = radius
        self.velocity = velocity
        self.mass = self.radius * 2
        self.friction = 0.995

    def update_velocity(self, bounds, elements):
        # Boundary collision
        if self.center.x + self.radius >= bounds.width:
            self.center.x = bounds.width - self.radius
            self.velocity.flip_x()
        elif self.center.x - self.radius <= 0:
            self.center.x = self.radius
            self.velocity.flip_x()

        if self.center.y + self.radius >= bounds.height:
            self.center.y = bounds.height - self.radius
            self.velocity.flip_y()
        elif self.center.y - self.radius <= 0:
            self.center.y = self.radius
            self.velocity.flip_y()

        # Element collision
        for element in elements:
            if isinstance(element, Burger) and element != self:
                dx = self.center.x - element.center.x
                dy = self.center.y - element.center.y
                distance = math.sqrt(dx * dx + dy * dy)
                min_distance = element.radius + self.radius

                if distance < min_distance:
                    tangent = math.atan2(dy, dx)
                    spread = min_distance - distance
                    ax = spread * math.cos(tangent)
                    ay = spread * math.sin(tangent)

                    self.center.x += ax
                    self.center.y += ay
                    element.center.x -= ax
                    element.center.y -= ay

                    punch = 2
                    self.velocity.vx += punch * math.cos(tangent)
                    self.velocity.vy += punch * math.sin(tangent)
                    element.velocity.vx -= punch * math.cos(tangent)
                    element.velocity.vy -= punch * math.sin(tangent)

                    break

        self.velocity.multiply(self.friction)

    def update(self, bounds, elements):
        self.center.apply_velocity(self.velocity)
        self.update_velocity(bounds, elements)

    def draw(self, screen):
        screen.blit(burger_image, (self.center.x - self.radius, self.center.y - self.radius))

# Sling class
class Sling:
    def __init__(self):
        self.mouse_down = False
        self.start = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
            self.start = Point(*pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
            if self.start:
                self.add_burger()

    def add_burger(self):
        mouse_pos = Point(*pygame.mouse.get_pos())
        delta = self.start.delta(mouse_pos)
        center = self.start
        radius = min(50, max(20, self.start.distance(mouse_pos) / 4))
        velocity = Velocity(*delta)
        velocity.multiply(0.25)
        burgers.append(Burger(center, radius, velocity))
        explosions.append(Explosion(0.2, radius, center))
        self.start = None

    def draw(self, screen):
        if self.mouse_down and self.start:
            mouse_pos = Point(*pygame.mouse.get_pos())
            pygame.draw.line(screen, WHITE, self.start.position(), mouse_pos.position(), 2)
            radius = self.start.distance(mouse_pos) / 4
            pygame.draw.circle(screen, WHITE, self.start.position(), int(radius), 2)

# Background class
class Background:
    def draw(self, screen):
        screen.blit(background_image, (0, 0))  # Draw the background image
        font = pygame.font.SysFont('futura', 90, italic=True)
        text = font.render('Sliders', True, BLUE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

# Main game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Good Burger: Sliders')
clock = pygame.time.Clock()

bounds = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
background = Background()
sling = Sling()
burgers = []
explosions = []

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        sling.handle_event(event)

    screen.fill(WHITE)
    background.draw(screen)

    for explosion in explosions:
        explosion.update()
        explosion.draw(screen)
    explosions = [e for e in explosions if not e.dead]

    for burger in burgers:
        burger.update(bounds, burgers)
        burger.draw(screen)

    sling.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
