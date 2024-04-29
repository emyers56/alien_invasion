import pygame

class SoundManager:
    """A class to manage the game's sound FX and music"""

    def __init__(self):
        """Initialize the game's sound manager"""
        pygame.mixer.init()
        self.bullet_sound = pygame.mixer.Sound("sounds/lazer-sound.wav")
        self.alien_explosion_sound = pygame.mixer.Sound("sounds/explosion-sound.wav")
        self.ship_hit_sound = pygame.mixer.Sound("sounds/ship-hit-sound.wav")
        self.level_up_sound = pygame.mixer.Sound("sounds/level-up-sound.wav")
        self.background_music = pygame.mixer.music.load("sounds/retro-music.wav")

    def play_bullet_sound(self):
        """Play the bullet sound"""
        self.bullet_sound.play()

    def play_alien_explosion_sound(self):
        """Play the alien explosion sound"""
        self.alien_explosion_sound.play()

    def play_ship_hit_sound(self):
        """Play the ship hit sound"""
        self.ship_hit_sound.play()

    def play_level_up_sound(self):
        """Play the level up sound"""
        self.level_up_sound.play()

    def start_background_music(self):
        """Start the background music"""
        pygame.mixer.music.play(-1)

    def stop_background_music(self):
        """Stop the background music"""
        pygame.mixer.music.stop()