"""
Laser projectile class for TejasThrust game
"""

import pygame
from src.config import *

class Laser:
    """Laser projectile class"""
    
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.width = LASER_WIDTH
        self.height = LASER_HEIGHT
    
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
