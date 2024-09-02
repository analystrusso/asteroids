import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, direction):
        super().__init__(x, y, SHOT_RADIUS)

        self.velocity = direction * PLAYER_SHOOT_SPEED
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color="white", center=(self.radius, self.radius), radius=self.radius, width=2)
        self.rect = self.image.get_rect(center=self.position)

    def get_rect(self):
        return pygame.Rect(self.position.x - self.position.y - self.radius, 2 * self.radius, 2* self.radius)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = self.position