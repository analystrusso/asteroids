import pygame
import random
import math
from constants import *
from circleshape import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        magnitude = random.uniform(1,75)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2.from_polar((magnitude, angle))

    def draw(self, screen):
        pygame.draw.circle(surface=screen, color=ASTEROID_COLOR, center=self.position, radius=self.radius, width=ASTEROID_WIDTH)
    
    def update(self, dt):
        self.position += (self.velocity * dt)