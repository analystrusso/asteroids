import pygame
from constants import *
from circleshape import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)

        self.position = pygame.Vector2(x, y)
        self.rotation = 0

        self.last_shot_time = 0
        self.shoot_cooldown = SHOOT_COOLDOWN

        self.image = pygame.Surface((2 * PLAYER_RADIUS, 2 * PLAYER_RADIUS), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)

        # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, color="white", points=self.triangle(), width=2)

    def rotate(self, dt):
        self.rotation = (PLAYER_TURN_SPEED * dt) + self.rotation

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            direction = pygame.Vector2(0, 1).rotate(self.rotation)
            new_shot = Shot(self.position.x, self.position.y, direction)
            self.last_shot_time = current_time

    def check_collision(self, other):
        distance = pygame.math.Vector2(self.position).distance_to(other.position)
        return distance < (self.radius + other.radius)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()