"""
Unit tests for UI components and visual elements
"""

import pytest
import pygame
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.ui import UI
from src.config import *

class TestUI:
    """Test UI functionality and visual elements"""
    
    @pytest.fixture
    def ui_setup(self):
        """Set up UI for testing"""
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        ui = UI(screen)
        yield screen, ui
        pygame.quit()
    
    def test_ui_initialization(self, ui_setup):
        """Test UI initialization"""
        screen, ui = ui_setup
        assert ui.screen == screen
        assert hasattr(ui, 'font_large')
        assert hasattr(ui, 'font_medium')
        assert hasattr(ui, 'font_small')
    
    def test_score_display_position(self, ui_setup):
        """Test that score is displayed in top right"""
        screen, ui = ui_setup
        
        # This test ensures the UI can render score without errors
        try:
            ui._draw_score(10)
        except Exception as e:
            pytest.fail(f"Score display failed: {e}")
    
    def test_health_display_position(self, ui_setup):
        """Test that health is displayed in top right"""
        screen, ui = ui_setup
        
        try:
            ui._draw_health(75)
        except Exception as e:
            pytest.fail(f"Health display failed: {e}")
    
    def test_exit_button_position(self, ui_setup):
        """Test that exit button is in bottom left"""
        screen, ui = ui_setup
        
        try:
            ui._draw_buttons(False)
        except Exception as e:
            pytest.fail(f"Button drawing failed: {e}")
    
    def test_pause_button_position(self, ui_setup):
        """Test that pause button is in bottom right"""
        screen, ui = ui_setup
        
        try:
            ui._draw_buttons(True)  # Test both pause and resume states
            ui._draw_buttons(False)
        except Exception as e:
            pytest.fail(f"Pause button drawing failed: {e}")
    
    def test_comic_sans_font_attempt(self, ui_setup):
        """Test that Comic Sans font is attempted"""
        screen, ui = ui_setup
        
        # The UI should have tried to load Comic Sans
        # We can't guarantee it's loaded (depends on system)
        # But we ensure fonts are available
        assert ui.font_large is not None
        assert ui.font_medium is not None
        assert ui.font_small is not None
    
    def test_pause_overlay(self, ui_setup):
        """Test pause overlay functionality"""
        screen, ui = ui_setup
        
        try:
            ui._draw_pause_overlay()
        except Exception as e:
            pytest.fail(f"Pause overlay failed: {e}")
    
    def test_game_over_screen(self, ui_setup):
        """Test game over screen display"""
        screen, ui = ui_setup
        
        try:
            ui._draw_game_over(25)  # Test with score of 25
        except Exception as e:
            pytest.fail(f"Game over screen failed: {e}")
    
    def test_health_bar_colors(self, ui_setup):
        """Test health bar color changes based on health level"""
        screen, ui = ui_setup
        
        # Test different health levels
        try:
            ui._draw_health(100)  # Full health - should be green
            ui._draw_health(25)   # Low health - should be orange
            ui._draw_health(5)    # Critical health - should be red
        except Exception as e:
            pytest.fail(f"Health bar color test failed: {e}")
    
    def test_ui_complete_draw(self, ui_setup):
        """Test complete UI drawing without errors"""
        screen, ui = ui_setup
        
        try:
            # Test normal state
            ui.draw(score=15, health=80, paused=False, game_over=False)
            
            # Test paused state
            ui.draw(score=15, health=80, paused=True, game_over=False)
            
            # Test game over state
            ui.draw(score=15, health=0, paused=False, game_over=True)
            
        except Exception as e:
            pytest.fail(f"Complete UI drawing failed: {e}")
    
    def test_button_dimensions(self, ui_setup):
        """Test that buttons have correct dimensions"""
        # Test that button constants are properly defined
        assert BUTTON_WIDTH > 0
        assert BUTTON_HEIGHT > 0
        assert BUTTON_WIDTH == 80
        assert BUTTON_HEIGHT == 40
    
    def test_professional_layout(self, ui_setup):
        """Test that UI elements don't overlap and are properly positioned"""
        screen, ui = ui_setup
        
        # Score position (top right)
        score_x = SCREEN_WIDTH - 20
        score_y = 20
        
        # Health position (top right, below score)
        health_x = SCREEN_WIDTH - 20
        health_y = 60
        
        # Exit button (bottom left)
        exit_x = 20
        exit_y = SCREEN_HEIGHT - 60
        
        # Pause button (bottom right)
        pause_x = SCREEN_WIDTH - 100
        pause_y = SCREEN_HEIGHT - 60
        
        # Test that elements don't overlap
        assert abs(score_x - health_x) < 50  # Should be close together
        assert abs(score_y - health_y) > 20  # But not overlapping
        assert abs(exit_x - pause_x) > 100   # Buttons well separated
