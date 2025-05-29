"""
Cloud class for animated background in TejasThrust game
"""

import pygame
import random
import math
from src.config import *

class Cloud:
    """Animated cloud for background"""
    
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.alpha = random.randint(100, 180)  # Transparency
        self.cloud_surface = self._create_cloud_surface()
    
    def _create_cloud_surface(self):
        """Create a cloud surface with transparency"""
        surface = pygame.Surface((self.size * 2, self.size), pygame.SRCALPHA)
        
        # Create multiple circles to form a cloud shape
        circles = [
            (self.size * 0.3, self.size * 0.5, self.size * 0.3),
            (self.size * 0.7, self.size * 0.4, self.size * 0.25),
            (self.size * 0.9, self.size * 0.6, self.size * 0.2),
            (self.size * 0.5, self.size * 0.3, self.size * 0.2),
            (self.size * 1.2, self.size * 0.5, self.size * 0.25),
            (self.size * 1.5, self.size * 0.4, self.size * 0.2),
        ]
        
        for cx, cy, radius in circles:
            color = (*CLOUD_COLOR, self.alpha)
            pygame.draw.circle(surface, color, (int(cx), int(cy)), int(radius))
        
        return surface
    
    def update(self):
        """Update cloud position"""
        self.y += self.speed
        
        # Reset cloud position when it goes off screen
        if self.y > SCREEN_HEIGHT + self.size:
            self.y = -self.size
            self.x = random.randint(-self.size, SCREEN_WIDTH + self.size)
    
    def draw(self, screen):
        """Draw the cloud"""
        screen.blit(self.cloud_surface, (self.x - self.size, self.y - self.size // 2))
