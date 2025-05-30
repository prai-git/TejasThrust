"""
Laser projectile class for TejasThrust game
"""

import pygame
from src.config import *

class Laser:
    """Laser projectile class"""
    
    def __init__(self, x, y, speed, color, damage=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = LASER_WIDTH
        self.height = LASER_HEIGHT
        self.damage = damage  # Amount of damage this laser does
    
    def update(self):
        """Update laser position"""
        self.y += self.speed
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)
    
    def draw(self, screen):
        """Draw the laser"""
        # Draw laser as a bright rectangle
        rect = self.get_rect()
        pygame.draw.rect(screen, self.color, rect)
        
        # Add glow effect for player lasers
        if self.color == LASER_COLOR:
            glow_rect = pygame.Rect(rect.x - 1, rect.y - 1, rect.width + 2, rect.height + 2)
            pygame.draw.rect(screen, (255, 255, 150), glow_rect, 1)
        
        # Add special effect for boss lasers
        elif self.damage > 1:
            # Make boss lasers thicker and with a trail
            trail_rect = pygame.Rect(rect.x - 1, rect.y - self.speed * 2, 
                                    rect.width + 2, rect.height + self.speed * 2)
            pygame.draw.rect(screen, (255, 100, 100, 128), trail_rect)
            # Add warning outline
            glow_rect = pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4)
            pygame.draw.rect(screen, (255, 200, 200), glow_rect, 1)
