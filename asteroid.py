import pygame
import random
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, "white", (radius, radius), radius, 2)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20, 50)
            vector_1 = self.velocity.rotate(random_angle)
            vector_2 = self.velocity.rotate(-random_angle)
            new_velocity = self.velocity * ASTEROID_SPLIT_FACTOR
            new_asteroid_radius = self.radius - ASTEROID_MIN_RADIUS

            new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)
            new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_asteroid_radius)

            new_asteroid_1.set_velocity(vector_1)
            new_asteroid_2.set_velocity(vector_2)

            for group in Asteroid.containers:
                group.add(new_asteroid_1)
                group.add(new_asteroid_2)


    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
        # Call the base class update if needed, typically for sprite management
        super().update(dt)