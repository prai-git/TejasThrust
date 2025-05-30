"""
Plane classes for TejasThrust game
"""

import pygame
import math
import random
from src.config import *
from src.laser import Laser

class Plane:
    """Base plane class"""
    
    def __init__(self, x, y, color, health=1):
        self.x = x
        self.y = y
        self.color = color
        self.health = health
        self.max_health = health
        self.width = PLANE_WIDTH
        self.height = PLANE_HEIGHT
        self.last_shot = 0
        self.shoot_cooldown = 500  # milliseconds
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, 
                          self.width, self.height)
    
    def take_damage(self):
        """Take damage"""
        self.health -= 1
    
    def draw(self, screen):
        """Draw the plane with a simple, kid-friendly design"""
        # Draw main fuselage (rectangle body)
        fuselage_width = self.width // 3
        fuselage_height = self.height // 1.5
        fuselage_rect = pygame.Rect(
            self.x - fuselage_width // 2,
            self.y - fuselage_height // 2,
            fuselage_width,
            fuselage_height
            )
        pygame.draw.rect(screen, self.color, fuselage_rect)

        # Draw left wing (triangle)
        left_wing_points = [
        (self.x - fuselage_width // 2, self.y - fuselage_height // 4), # wing root
        (self.x - self.width // 2, self.y), # wing tip
        (self.x - fuselage_width // 2, self.y + fuselage_height // 4) # wing back
        ]
        pygame.draw.polygon(screen, self.color, left_wing_points)
        # Draw right wing (triangle)
        right_wing_points = [
        (self.x + fuselage_width // 2, self.y - fuselage_height // 4), # wing root
        (self.x + self.width // 2, self.y), # wing tip
        (self.x + fuselage_width // 2, self.y + fuselage_height // 4) # wing back
        ]
        pygame.draw.polygon(screen, self.color, right_wing_points)
        # Draw nose (triangle)
        nose_points = [
            (self.x - fuselage_width // 2, self.y - fuselage_height // 2), # left corner
            (self.x, self.y - fuselage_height), # tip
            (self.x + fuselage_width // 2, self.y - fuselage_height // 2) # right corner
            ]
        pygame.draw.polygon(screen, self.color, nose_points)

        # Draw tail (triangle)
        tail_points = [
            (self.x - fuselage_width // 2, self.y + fuselage_height // 2), # left corner
            (self.x, self.y + fuselage_height), # tip
            (self.x + fuselage_width // 2, self.y + fuselage_height // 2) # right corner
        ]
        pygame.draw.polygon(screen, self.color, tail_points)

        # Draw cockpit (small darker circle on top)
        cockpit_color = tuple(max(0, c - 50) for c in self.color) # Darker shade
        cockpit_pos = (self.x, self.y - fuselage_height // 4)
        cockpit_radius = fuselage_width // 3
        pygame.draw.circle(screen, cockpit_color, cockpit_pos, cockpit_radius)

        # Draw health bar for enemies
        if hasattr(self, 'show_health') and self.show_health and self.health < self.max_health:
            self._draw_health_bar(screen)
    
    def _draw_health_bar(self, screen):
        """Draw health bar above plane"""
        bar_width = 40
        bar_height = 6
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.height // 2 - 15
        
        # Background
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_width = int((self.health / self.max_health) * bar_width)
        if health_width > 0:
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class PlayerPlane(Plane):
    """Player controlled plane"""
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_COLOR, PLAYER_MAX_HEALTH)
        self.speed = PLAYER_SPEED
        self.shoot_cooldown = 200  # Faster shooting for player
    
    def update(self, keys):
        """Update player plane based on key input"""
        # Movement with arrow keys
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed
        
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707
        
        # Update position with screen boundaries
        self.x = max(self.width // 2, min(SCREEN_WIDTH - self.width // 2, self.x + dx))
        self.y = max(self.height // 2, min(SCREEN_HEIGHT - self.height // 2, self.y + dy))
    
    def shoot(self):
        """Shoot a laser"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_cooldown:
            self.last_shot = current_time
            return Laser(self.x, self.y - self.height // 2, -LASER_SPEED, LASER_COLOR)
        return None

class EnemyPlane(Plane):
    """Computer controlled enemy plane"""
    
    def __init__(self, x, y):
        super().__init__(x, y, ENEMY_COLOR, ENEMY_HEALTH)
        self.speed = ENEMY_SPEED
        self.show_health = True
        self.direction_x = random.choice([-1, 1])
        self.direction_y = 1
        self.change_direction_timer = 0
        self.shoot_cooldown = 1000  # Slower shooting for enemies
    
    def update(self):
        """Update enemy plane AI movement"""
        # Change direction occasionally for evasive maneuvers
        self.change_direction_timer += 1
        if self.change_direction_timer > random.randint(60, 120):  # 1-2 seconds at 60 FPS
            self.direction_x = random.choice([-1, 0, 1])
            self.change_direction_timer = 0
        
        # Move down and sideways
        self.x += self.direction_x * self.speed * 0.5
        self.y += self.direction_y * self.speed
        
        # Keep within screen bounds (horizontally)
        if self.x <= self.width // 2:
            self.direction_x = 1
        elif self.x >= SCREEN_WIDTH - self.width // 2:
            self.direction_x = -1
    
    def shoot(self):
        """Shoot a laser towards player general area"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_cooldown:
            self.last_shot = current_time
            return Laser(self.x, self.y + self.height // 2, ENEMY_LASER_SPEED, RED)
        return None

class BossPlane(Plane):
    """Powerful boss plane that appears after killing multiple enemies"""
    
    def __init__(self, x, y):
        super().__init__(x, y, BOSS_COLOR, BOSS_HEALTH)
        self.width = BOSS_WIDTH
        self.height = BOSS_HEIGHT
        self.speed = BOSS_SPEED
        self.show_health = True
        self.direction_x = random.choice([-1, 1])
        self.direction_y = 0  # Boss stays at relatively same height
        self.change_direction_timer = 0
        self.shoot_cooldown = 800  # Faster shooting than regular enemies
    
    def update(self):
        """Update boss plane AI movement - more sophisticated than regular enemies"""
        # Change direction occasionally for evasive maneuvers
        self.change_direction_timer += 1
        if self.change_direction_timer > random.randint(30, 90):  # More frequent direction changes
            self.direction_x = random.choice([-1, 0, 1])
            # Occasionally move slightly up or down
            self.direction_y = random.choice([-0.5, 0, 0.5])
            self.change_direction_timer = 0
        
        # Move sideways and occasionally up/down
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        
        # Keep within screen bounds (horizontally)
        if self.x <= self.width // 2:
            self.direction_x = 1
        elif self.x >= SCREEN_WIDTH - self.width // 2:
            self.direction_x = -1
            
        # Keep within the top portion of the screen (vertically)
        if self.y <= self.height:
            self.direction_y = 0.5
        elif self.y >= SCREEN_HEIGHT // 3:
            self.direction_y = -0.5
    
    def shoot(self):
        """Shoot a more powerful laser towards player"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_cooldown:
            self.last_shot = current_time
            return Laser(self.x, self.y + self.height // 2, BOSS_LASER_SPEED, RED, damage=BOSS_LASER_DAMAGE)
        return None
    
    def draw(self, screen):
        """Draw the boss plane with a more imposing, kid-friendly design"""
        # Draw main fuselage (rectangle body) - larger than regular planes
        fuselage_width = self.width // 3
        fuselage_height = self.height // 1.5
        fuselage_rect = pygame.Rect(
            self.x - fuselage_width // 2,
            self.y - fuselage_height // 2,
            fuselage_width,
            fuselage_height
            )
        pygame.draw.rect(screen, self.color, fuselage_rect)

        # Draw left wing (triangle) - larger
        left_wing_points = [
        (self.x - fuselage_width // 2, self.y - fuselage_height // 4), # wing root
        (self.x - self.width // 2, self.y), # wing tip
        (self.x - fuselage_width // 2, self.y + fuselage_height // 4) # wing back
        ]
        pygame.draw.polygon(screen, self.color, left_wing_points)
        
        # Draw right wing (triangle) - larger
        right_wing_points = [
        (self.x + fuselage_width // 2, self.y - fuselage_height // 4), # wing root
        (self.x + self.width // 2, self.y), # wing tip
        (self.x + fuselage_width // 2, self.y + fuselage_height // 4) # wing back
        ]
        pygame.draw.polygon(screen, self.color, right_wing_points)
        
        # Draw nose (triangle) - more aggressive angle
        nose_points = [
            (self.x - fuselage_width // 2, self.y - fuselage_height // 2), # left corner
            (self.x, self.y - fuselage_height), # tip
            (self.x + fuselage_width // 2, self.y - fuselage_height // 2) # right corner
            ]
        pygame.draw.polygon(screen, self.color, nose_points)

        # Draw tail (triangle) - larger
        tail_points = [
            (self.x - fuselage_width // 2, self.y + fuselage_height // 2), # left corner
            (self.x, self.y + fuselage_height), # tip
            (self.x + fuselage_width // 2, self.y + fuselage_height // 2) # right corner
        ]
        pygame.draw.polygon(screen, self.color, tail_points)

        # Draw cockpit (small darker circle on top)
        cockpit_color = tuple(max(0, c - 50) for c in self.color) # Darker shade
        cockpit_pos = (self.x, self.y - fuselage_height // 4)
        cockpit_radius = fuselage_width // 3
        pygame.draw.circle(screen, cockpit_color, cockpit_pos, cockpit_radius)
        
        # Add extra details for boss plane
        # Wing tips
        pygame.draw.circle(screen, BLACK, (int(self.x - self.width // 2), int(self.y)), 5)
        pygame.draw.circle(screen, BLACK, (int(self.x + self.width // 2), int(self.y)), 5)
        
        # Draw health bar for boss
        self._draw_health_bar(screen)
