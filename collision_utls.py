import pygame

def check_collisions(shots, asteroids):
        for shot in shots:
            for asteroid in asteroids:
                distance = pygame.math.Vector2(shot.position).distance_to(asteroid.position)
                if distance < (shot.radius + asteroid.radius):
                    shot.kill()  # Remove the shot
                    asteroid.kill()  # Remove the asteroid
                break  # Break the loop to avoid multiple collisions
