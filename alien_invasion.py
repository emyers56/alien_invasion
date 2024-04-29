import sys
import pygame
import time

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from explosion import Explosion
from game_stats import GameStats
from button import Button
from sound_manager import SoundManager
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.bg_image = pygame.image.load('images/space-background.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (self.settings.screen_width, self.settings.screen_height))

        # Uncomment below for Full Screen mode
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game stats and create a scoreboard
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self._create_fleet()

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # Make the Play button
        self.play_button = Button(self, 'Play')

        # Start the sound manager
        self.sounds = SoundManager()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(self.settings.frame_rate)
    
    def _check_events(self):
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN and self.game_active:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings
            self.settings.intialize_dynamic_settings()

            # Reset the game statistics
            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

            # Start the background music
            self.sounds.start_background_music()

    def _check_keydown_events(self, event):
        """Respond to keydown presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            # Play sound
            self.sounds.play_bullet_sound()


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets:
            if bullet.rect.y <= 0:
                self.bullets.remove(bullet)

        # Check for any bullets that have hit aliens
        self._check_bullet_alien_collisions()

    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # Increment the score if there is an alien explosion
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    # Create explosion
                    self._create_explosion(alien.rect.center)

            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

            # Play the alien explosion sound
            self.sounds.play_alien_explosion_sound()  

        # Check if the entire fleet has been destroyed and level up to repopulate the fleet
        if not self.aliens:
            self.sounds.play_level_up_sound()
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level +=1
            self.scoreboard.prep_level()
    
    def _create_alien(self, x_position, y_position):
        """Create an alien at the correct position and add to the fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x, new_alien.rect.y = x_position, y_position
        self.aliens.add(new_alien)

    def _create_explosion(self, center_pos):
        """Create an explosion at the correct position and add to the sprite group"""
        new_explosion = Explosion(self, center_pos)
        self.explosions.add(new_explosion)


    def _check_fleet_edges(self):
        """"Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        
        # Move all aliens in the fleet down
        alien_height = Alien(self).rect.height
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        # Change direction of fleet
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""

        if self.stats.ships_left > 1:
            # Play the ship hit sound
            self.sounds.play_ship_hit_sound()

            # Decrement ships left and update scoreboard
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # Get rid of the any remaining bullets, aliens, and explosions
            self._cleanup_game_elements()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            time.sleep(1.0)
        else:
            # Game over
            self.game_active = False
            pygame.mouse.set_visible(True)
            self.sounds.stop_background_music()

    def _cleanup_game_elements(self):
        """Get rid of any remaining bullets, aliens, and explosions when leveling up or game over"""
        # Get rid of the any remaining bullets, aliens, and explosions
        self.bullets.empty()
        self.aliens.empty()
        self.explosions.empty()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()
        self.explosions.update()

        # Check for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    

    def _create_fleet(self):
        """Create the fleet of aliens"""
        alien_width, alien_height = Alien(self).rect.size
        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished row. Reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _update_screen(self):
        """"Update images on the screen and flip to the new screen"""
        # Redraw the screen

        # Uniform background color
        # self.screen.fill(self.settings.bg_color)

        # Custom background color
        self.screen.blit(self.bg_image, (0, 0))


        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)

        # Draw the score information
        self.scoreboard.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        
        # Make the most recent drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()