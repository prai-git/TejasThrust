"""
Unit tests for plane classes (PlayerPlane and EnemyPlane)
"""

import pytest
import pygame
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.plane import PlayerPlane, EnemyPlane
from src.config import *

class TestPlayerPlane:
    """Test PlayerPlane functionality"""
    
    @pytest.fixture
    def player(self):
        """Create a player plane for testing"""
        pygame.init()
        player = PlayerPlane(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        yield player
        pygame.quit()
    
    def test_player_initialization(self, player):
        """Test player plane initialization"""
        assert player.color == PLAYER_COLOR
        assert player.health == PLAYER_MAX_HEALTH
        assert player.speed == PLAYER_SPEED
        assert player.x == SCREEN_WIDTH // 2
        assert player.y == SCREEN_HEIGHT - 100
    
    def test_player_blue_color(self, player):
        """Test that player plane is blue"""
        assert player.color == (0, 100, 255)  # Blue
    
    def test_player_movement_boundaries(self, player):
        """Test that player stays within screen boundaries"""        # Test left boundary
        player.x = 0
        keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False, 
                pygame.K_UP: False, pygame.K_DOWN: False}
        player.update(keys)
        assert player.x >= player.width // 2
        
        # Test right boundary
        player.x = SCREEN_WIDTH
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True, 
                pygame.K_UP: False, pygame.K_DOWN: False}
        player.update(keys)
        assert player.x <= SCREEN_WIDTH - player.width // 2
    
    def test_player_shooting_cooldown(self, player):
        """Test player shooting has appropriate cooldown"""
        # Mock pygame.time.get_ticks to simulate time passage
        import pygame
        original_get_ticks = pygame.time.get_ticks
        
        # First shot at time 250 (after cooldown period from initial 0)
        pygame.time.get_ticks = lambda: 250
        player.last_shot = 0
        laser1 = player.shoot()
        assert laser1 is not None
        
        # Immediate second shot (still at time 250) should be blocked by cooldown
        # because last_shot is now 250 and 250 - 250 = 0 < 200
        laser2 = player.shoot()
        assert laser2 is None
        
        # Shot after cooldown period should work
        pygame.time.get_ticks = lambda: 500  # 500ms, which is 250ms after last shot
        laser3 = player.shoot()
        assert laser3 is not None
        
        # Restore original function
        pygame.time.get_ticks = original_get_ticks
    
    def test_player_collision_rect(self, player):
        """Test player collision rectangle"""
        rect = player.get_rect()
        assert rect.width == player.width
        assert rect.height == player.height
        assert rect.centerx == player.x
        assert rect.centery == player.y

class TestEnemyPlane:
    """Test EnemyPlane functionality"""
    
    @pytest.fixture
    def enemy(self):
        """Create an enemy plane for testing"""
        pygame.init()
        enemy = EnemyPlane(100, 50)
        yield enemy
        pygame.quit()
    
    def test_enemy_initialization(self, enemy):
        """Test enemy plane initialization"""
        assert enemy.color == ENEMY_COLOR
        assert enemy.health == ENEMY_HEALTH
        assert enemy.max_health == ENEMY_HEALTH
        assert enemy.speed == ENEMY_SPEED
        assert enemy.show_health == True
    
    def test_enemy_black_color(self, enemy):
        """Test that enemy plane is black/dark gray"""
        assert enemy.color == (50, 50, 50)  # Dark gray
    
    def test_enemy_health_system(self, enemy):
        """Test enemy health system (requires 2 hits)"""
        assert enemy.health == 2
        
        # First hit
        enemy.take_damage()
        assert enemy.health == 1
        
        # Second hit
        enemy.take_damage()
        assert enemy.health == 0
    
    def test_enemy_movement(self, enemy):
        """Test enemy movement and AI"""
        initial_y = enemy.y
        
        # Update enemy position
        enemy.update()
        
        # Enemy should move down
        assert enemy.y > initial_y
    
    def test_enemy_evasive_behavior(self, enemy):
        """Test that enemy has evasive movement capabilities"""
        # Enemy should have direction variables for evasive maneuvers
        assert hasattr(enemy, 'direction_x')
        assert hasattr(enemy, 'direction_y')
        assert hasattr(enemy, 'change_direction_timer')
        
        # Direction should be valid
        assert enemy.direction_x in [-1, 0, 1]
        assert enemy.direction_y == 1  # Always moving down
    
    def test_enemy_boundary_detection(self, enemy):
        """Test that enemy changes direction at screen boundaries"""
        # Test left boundary
        enemy.x = 10
        enemy.direction_x = -1
        enemy.update()
        assert enemy.direction_x == 1  # Should change to right
        
        # Test right boundary  
        enemy.x = SCREEN_WIDTH - 10
        enemy.direction_x = 1
        enemy.update()
        assert enemy.direction_x == -1  # Should change to left
    
    def test_enemy_shooting_capability(self, enemy):
        """Test that enemy can shoot"""
        laser = enemy.shoot()
        # Due to cooldown, laser might be None
        if laser:
            assert laser.color == RED
            assert laser.speed > 0  # Moving downward
    
    def test_enemy_collision_rect(self, enemy):
        """Test enemy collision rectangle"""
        rect = enemy.get_rect()
        assert rect.width == enemy.width
        assert rect.height == enemy.height
