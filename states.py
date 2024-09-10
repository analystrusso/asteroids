import os
from asteroidfield import *
from main import *
from player import *
from shot import *
from constants import *
import sys


class States:
    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None

    def startup(self):
        pass

    def cleanup(self):
        pass

    def update(self, screen, dt):
        pass

    def get_event(self, event):
        pass

    def setup_states(self, state_dict_settings, param):
        pass

    def main_game_loop(self):
        pass


class Game(States):
    def __init__(self):
        super().__init__()
        pg.init()
        self.next = "menu"
        self.score = 0
        self.score_increment = 100
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.updatable = pg.sprite.Group()
        self.drawable = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.shots = pg.sprite.Group()
        self.player = None
        self.asteroid_field = None
        self.is_initialized = False

    def startup(self):
        """Initialize Game state."""
        if not self.is_initialized:
            pg.font.init()

            Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
            Shot.containers = (self.shots, self.updatable, self.drawable)
            AsteroidField.containers = self.updatable
            self.asteroid_field = AsteroidField()
            Player.containers = (self.updatable, self.drawable)
            self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.is_initialized = True

    def save_state(self):
        """Save the current state of game entities."""
        self.saved_state = {
            'asteroids': [(a.position.x, a.position.y, a.velocity.x, a.velocity.y, a.radius) for a in self.asteroids],
            'shots': [(s.position.x, s.position.y, s.velocity.x, s.velocity.y) for s in self.shots],
            'player': (self.player.position.x, self.player.position.y, self.player.velocity.x, self.player.velocity.y),
            'asteroid_field': self.asteroid_field.get_state()  # Customize based on your needs
        }

    def restore_state(self):
        """Restore the saved state of game entities."""
        if not self.saved_state:
            return

        # Restore asteroids
        self.asteroids.empty()
        for x, y, vx, vy, radius in self.saved_state['asteroids']:
            asteroid = Asteroid(x, y, radius)
            asteroid.set_velocity(
                pg.Vector2(vx, vy))  # Assuming set_velocity is a method to set the asteroid's velocity
            self.asteroids.add(asteroid)

        # Restore shots
        self.shots.empty()
        for x, y, vx, vy in self.saved_state['shots']:
            shot = Shot(x, y)
            shot.set_velocity(pg.Vector2(vx, vy))  # Assuming set_velocity is a method to set the shot's velocity
            self.shots.add(shot)

        # Restore player
        if self.player:
            x, y, vx, vy = self.saved_state['player']
            self.player.position = pg.Vector2(x, y)
            self.player.set_velocity(
                pg.Vector2(vx, vy))  # Assuming set_velocity is a method to set the player's velocity

        # Restore asteroid field state
        if self.asteroid_field:
            self.asteroid_field.set_state(self.saved_state['asteroid_field'])  # Customize based on your needs

    def cleanup(self):
        """Clean up Game state."""
        if self.is_initialized:
            self.save_state()
            self.is_initialized = False
            self.asteroids.empty()  # Clear all asteroids
            self.shots.empty()  # Clear all shots
            self.updatable.empty()  # Clear all updatable objects
            self.drawable.empty()  # Clear all drawable objects

    def resume(self):
        self.restore_state()
        self.is_initialized = True

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:  # Example: press Enter to start the game
                print('Menu State keydown')
                self.done = True
                self.next = "pause"

    def update(self, screen, dt):
        """Update Game state."""
        for obj in self.updatable:
            obj.update(dt)

        for asteroid in self.asteroids:
            if asteroid.collides_with(self.player):
                print("Game over!")
                self.done = True
                self.next = "game_over"
                return

            for shot in self.shots:
                if asteroid.collides_with(shot):
                    self.score += self.score_increment
                    shot.kill()
                    asteroid.split()

        screen.fill((0, 0, 0))

        for obj in self.drawable:
            obj.draw(screen)

        font = pg.font.Font("Major_Mono_Display/MajorMonoDisplay-Regular.ttf", 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))


class GameOver(States):
    def __init__(self):
        super().__init__()
        self.next = "menu"
        self.font = self.load_font("Major_Mono_Display/MajorMonoDisplay-Regular.ttf", 36)
        self.final_score = 0

    def load_font(self, font_path, size):
        if not os.path.isfile(font_path):
            print(f"Font file not found: {font_path}")
            return None
        try:
            return pg.font.Font(font_path, size)
        except Exception as e:
            print(f"Error loading font: {e}")
            return None

    def set_score(self, score):
        self.final_score = score

    def startup(self):
        print('starting Menu state stuff')

    def cleanup(self):
        pass

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.font:  # Check if font is initialized
            text = self.font.render("Game Over", True, (255, 255, 255))
            score_text = self.font.render(f"Score: {self.final_score}", True, (255, 255, 255))
            screen.blit(text, (50, 100))
            screen.blit(score_text, (50, 150))
        else:
            print("Font not initialized.")


class Menu(States):
    def __init__(self):
        super().__init__()
        self.next = "game"
        self.font = self.load_font("Major_Mono_Display/MajorMonoDisplay-Regular.ttf", 36)

    def load_font(self, font_path, size):
        if not os.path.isfile(font_path):
            print(f"Font file not found: {font_path}")
            return None
        try:
            return pg.font.Font(font_path, size)
        except Exception as e:
            print(f"Error loading font: {e}")
            return None

    def startup(self):
        print('starting Menu state stuff')

    def cleanup(self):
        pass

    def update(self, screen, dt):
        self.draw(screen)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:  # Example: press Enter to start the game
                print('Menu State keydown')
                self.done = True
                self.next = "game"

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.font:  # Check if font is initialized
            text = self.font.render("Press Enter to Start", True, (255, 255, 255))
            screen.blit(text, (50, 100))
        else:
            print("Font not initialized.")


class Pause(States):
    def __init__(self):
        super().__init__()
        self.next = "game"
        self.font = self.load_font("Major_Mono_Display/MajorMonoDisplay-Regular.ttf", 36)

    def load_font(self, font_path, size):
        if not os.path.isfile(font_path):
            print(f"Font file not found: {font_path}")
            return None
        try:
            return pg.font.Font(font_path, size)
        except Exception as e:
            print(f"Error loading font: {e}")
            return None

    def startup(self):
        print('starting Menu state stuff')

    def cleanup(self):
        pass

    def update(self, screen, dt):
        self.draw(screen)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:  # Example: press Enter to start the game
                print('Pause State keydown')
                self.done = True
                self.next = "game"

    def draw(self, screen):
        screen.fill((0, 0, 0))
        if self.font:  # Check if font is initialized
            text = self.font.render("Press Enter to Resume", True, (255, 255, 255))
            screen.blit(text, (50, 100))
        else:
            print("Font not initialized.")


class Control:
    def __init__(self, **config):
        pg.init()
        pg.font.init()
        self.state_dict = None
        self.state_name = None
        self.state = None
        self.__dict__.update(config)
        self.done = False
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
        self.fps = settings.get("fps", 60)

    def setup_states(self, state_dict_param, start_state):
        self.state_dict = state_dict_param
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()

    def flip_state(self):
        self.state.done = False
        previous_state_name = self.state_name
        self.state_name = self.state.next
        self.state.cleanup()

        self.state = self.state_dict[self.state_name]

        if not hasattr(self.state, "is_initialized") or not self.state.is_initialized:
            self.state.startup()
            if hasattr(self.state, "is_initialized"):
                self.state.is_initialized = True

        self.state.previous = previous_state_name

        if self.state_name == "game_over":
            game_state = self.state_dict["game"]
            final_score = game_state.score
            self.state.set_score(final_score)
        else:
            self.state = self.state_dict[self.state_name]

    def update(self, dt):
        if self.state.done:
            self.flip_state()
        else:
            self.state.update(self.screen, dt)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)

    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(delta_time)
            try:
                pg.display.update()
            except Exception as e:
                print(f"Error updating display: {e}")
                self.done = True


# Settings for the game
settings = {
    "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
    "fps": 60
}

if __name__ == "__main__":
    app = Control(**settings)
    state_dict = {
        "pause": Pause(),
        "menu": Menu(),
        "game": Game(),
        "game_over": GameOver()
    }

    app.setup_states(state_dict, "menu")
    app.main_game_loop()
    #pg.quit()
    sys.exit()
