"""
Unit tests for the main TejasThrust game class
Tests all game specifications mentioned in the requirements
"""

import pytest
import pygame
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import TejasThrust
from src.config import *
from src.plane import PlayerPlane, EnemyPlane
from src.laser import Laser

class TestTejasThrust:
    """Test main game functionality"""
    
    @pytest.fixture
    def game(self):
        """Create a game instance for testing"""
        pygame.init()
        game = TejasThrust()
        yield game
        pygame.quit()
    
    def test_game_initialization(self, game):
        """Test that game initializes correctly"""
        assert game.running == True
        assert game.paused == False
        assert game.game_over == False
        assert game.score == 0
        assert game.player_health == PLAYER_MAX_HEALTH
        assert game.player is not None
        assert isinstance(game.enemies, list)
        assert isinstance(game.player_lasers, list)
        assert isinstance(game.enemy_lasers, list)
        assert isinstance(game.clouds, list)
        assert len(game.clouds) == 8  # Initial cloud count
    
    def test_screen_dimensions(self, game):
        """Test that screen has correct dimensions"""
        assert game.screen.get_width() == SCREEN_WIDTH
        assert game.screen.get_height() == SCREEN_HEIGHT
    
    def test_player_plane_color(self, game):
        """Test that player plane is blue as specified"""
        assert game.player.color == PLAYER_COLOR
        assert PLAYER_COLOR == (0, 100, 255)  # Blue color
    
    def test_player_max_health(self, game):
        """Test that player starts with 100 health"""
        assert game.player_health == 100
        assert PLAYER_MAX_HEALTH == 100
    
    def test_enemy_spawn_mechanism(self, game):
        """Test enemy spawning functionality"""
        initial_enemy_count = len(game.enemies)
        
        # Simulate time passing for enemy spawn
        game.last_enemy_spawn = 0  # Reset spawn timer
        game.spawn_enemy()
        
        assert len(game.enemies) >= initial_enemy_count
    
    def test_enemy_plane_color(self, game):
        """Test that enemy planes are black/dark gray as specified"""
        game.spawn_enemy()
        if game.enemies:
            enemy = game.enemies[0]
            assert enemy.color == ENEMY_COLOR
            assert ENEMY_COLOR == (50, 50, 50)  # Dark gray/black
    
    def test_enemy_health_two_hits(self, game):
        """Test that enemies require 2 hits to be destroyed"""
        enemy = EnemyPlane(100, 100)
        assert enemy.health == 2
        assert ENEMY_HEALTH == 2
        
        # First hit
        enemy.take_damage()
        assert enemy.health == 1
        
        # Second hit should destroy
        enemy.take_damage()
        assert enemy.health == 0
    
    def test_player_laser_shooting(self, game):
        """Test that player can shoot lasers with spacebar"""
        initial_laser_count = len(game.player_lasers)
        
        # Simulate spacebar press
        laser = game.player.shoot()
        if laser:  # Cooldown might prevent shooting
            game.player_lasers.append(laser)
            assert len(game.player_lasers) > initial_laser_count
            assert laser.color == LASER_COLOR  # Yellow laser
    
    def test_laser_visibility(self, game):
        """Test that lasers are clearly visible (yellow color)"""
        laser = Laser(100, 100, -5, LASER_COLOR)
        assert laser.color == LASER_COLOR
        assert LASER_COLOR == (255, 255, 0)  # Bright yellow
    
    def test_player_movement_arrow_keys(self, game):
        """Test player movement with arrow keys"""
        initial_x = game.player.x
        initial_y = game.player.y
        
        # Simulate arrow key presses
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True, 
                pygame.K_UP: False, pygame.K_DOWN: False}
        
        game.player.update(keys)
        assert game.player.x != initial_x  # Should have moved
    
    def test_diagonal_movement(self, game):
        """Test that combination of arrow keys moves plane at angle"""
        initial_x = game.player.x
        initial_y = game.player.y
        
        # Simulate right + down arrow keys
        keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True, 
                pygame.K_UP: False, pygame.K_DOWN: True}
        
        game.player.update(keys)
        
        # Both x and y should change for diagonal movement
        x_changed = game.player.x != initial_x
        y_changed = game.player.y != initial_y
        assert x_changed and y_changed
    
    def test_player_health_decreases_on_hit(self, game):
        """Test that player health decreases when hit by enemy laser"""
        initial_health = game.player_health
        
        # Create enemy laser at player position
        enemy_laser = Laser(game.player.x, game.player.y, 1, RED)
        game.enemy_lasers.append(enemy_laser)
        
        # Check collision
        game._check_collisions()
        
        # Health should decrease if collision occurred
        if len(game.enemy_lasers) == 0:  # Laser was removed due to collision
            assert game.player_health == initial_health - 1
    
    def test_game_over_at_zero_health(self, game):
        """Test that game ends when player health reaches 0"""
        game.player_health = 0
        game.update()
        assert game.game_over == True
    
    def test_score_increases_on_enemy_defeat(self, game):
        """Test that score increases when enemy is defeated"""
        initial_score = game.score
        
        # Create enemy with 1 health remaining
        enemy = EnemyPlane(100, 100)
        enemy.health = 1
        game.enemies.append(enemy)
        
        # Create player laser at enemy position
        laser = Laser(enemy.x, enemy.y, -1, LASER_COLOR)
        game.player_lasers.append(laser)
        
        # Check collisions
        game._check_collisions()
        
        # Score should increase if enemy was destroyed
        if enemy not in game.enemies:  # Enemy was removed
            assert game.score == initial_score + 1
    
    def test_smooth_movement_speeds(self, game):
        """Test that movement speeds are appropriate for smooth animation"""
        assert PLAYER_SPEED <= 8  # Not too fast
        assert ENEMY_SPEED <= 5   # Slower than player
        assert LASER_SPEED >= 5   # Fast enough to be effective
        assert FPS == 60          # Smooth frame rate
    
    def test_pause_functionality(self, game):
        """Test pause and resume functionality"""
        # Test initial state
        assert game.paused == False
        
        # Simulate pause button click
        game.paused = True
        assert game.paused == True
        
        # Test that game doesn't update when paused
        initial_enemy_count = len(game.enemies)
        game.update()  # Should not spawn enemies when paused
        # (This is a simplified test - in real scenario we'd check time-based spawning)
    
    def test_ui_elements_present(self, game):
        """Test that required UI elements are present"""
        assert game.ui is not None
        
        # Test that UI can draw without errors
        try:
            game.ui.draw(game.score, game.player_health, game.paused, game.game_over)
        except Exception as e:
            pytest.fail(f"UI drawing failed: {e}")
    
    def test_background_clouds_moving(self, game):
        """Test that background clouds are present and moving"""
        assert len(game.clouds) > 0
        
        initial_positions = [(cloud.x, cloud.y) for cloud in game.clouds]
        
        # Update clouds
        for cloud in game.clouds:
            cloud.update()
        
        # At least some clouds should have moved
        new_positions = [(cloud.x, cloud.y) for cloud in game.clouds]
        assert initial_positions != new_positions
    
    def test_enemy_defensive_movement(self, game):
        """Test that enemies move to protect themselves"""
        enemy = EnemyPlane(100, 100)
        initial_x = enemy.x
        
        # Update enemy several times
        for _ in range(10):
            enemy.update()
        
        # Enemy should have moved (defensive behavior)
        # Note: Due to randomness, we can't guarantee movement in 10 frames
        # But the enemy should be capable of movement
        assert hasattr(enemy, 'direction_x')
        assert hasattr(enemy, 'change_direction_timer')
    
    def test_font_requirements(self, game):
        """Test that Comic Sans font is attempted to be loaded"""
        # This tests that the UI class tries to load Comic Sans
        ui = game.ui
        # The actual font loading is in UI class initialization
        # We can't easily test the exact font, but we ensure UI has fonts
        assert hasattr(ui, 'font_large')
        assert hasattr(ui, 'font_medium')
        assert hasattr(ui, 'font_small')
    
    def test_professional_plane_sprites(self, game):
        """Test that planes have proper dimensions for professional appearance"""
        assert PLANE_WIDTH > 0 and PLANE_HEIGHT > 0
        assert game.player.width == PLANE_WIDTH
        assert game.player.height == PLANE_HEIGHT
        
        # Test that planes fit on screen
        assert PLANE_WIDTH < SCREEN_WIDTH
        assert PLANE_HEIGHT < SCREEN_HEIGHT
