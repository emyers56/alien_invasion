import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """A class to represent a single exploded alien ship"""
    def __init__(self, ai_game, center_pos):
        """Initialize the explosion by inheriting attributes/methods from the alien class"""
        super().__init__()
        self.settings = ai_game.settings       
        self.num_frames = 16
        self.current_frame = 0
        self.frames = []
        for i in range(self.num_frames):
            image = pygame.image.load(f'images/explosion_animation/explosion_{i}.png').convert_alpha()
            self.frames.append(image)
        self.image = self.frames[self.current_frame] 
        self.rect = self.image.get_rect(center=center_pos)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        """Update the explosion by stepping through the animation"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.settings.frame_rate:
            # Refresh last update
            self.last_update = now
            self.current_frame += 1
            if self.current_frame == len(self.frames):
                # End animation
                self.kill()
            else:
                self.image = self.frames[self.current_frame]
