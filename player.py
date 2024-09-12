import pygame as pg
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0

    def draw(self, screen):
        pg.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pg.Vector2(0, 1).rotate(self.rotation)
        right = pg.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pg.key.get_pressed()
        
        if keys[pg.K_w]:
            self.move(dt)
        if keys[pg.K_s]:
            self.move(-dt)
        if keys[pg.K_a]:
            self.rotate(-dt)
        if keys[pg.K_d]:
            self.rotate(dt)
        if keys[pg.K_SPACE]:
            self.shoot()

        self.check_boundaries()
    
    def check_boundaries(self):
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH
        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pg.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pg.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
