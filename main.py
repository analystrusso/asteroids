import pygame
from constants import *
from circleshape import *
from player import *
from asteroid import *
from asteroidfield import *

def main():
    pygame.init()
    
    # Create groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # Set container groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)

    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    color = "black"
    
    # Create player instance and add to groups
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    updatable.add(player)
    drawable.add(player)

    # Create an AsteroidField instance and add to updatable group
    asteroid_field = AsteroidField()

    # Create the game loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for sprite in updatable:
            sprite.update(dt)

        for asteroid in asteroids:
            if player.check_collision(asteroid):
                print("Game over!")
                pygame.quit()
                exit()
        
        screen.fill(color)
        
        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()