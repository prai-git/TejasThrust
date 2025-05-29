"""
User Interface class for TejasThrust game
"""

import pygame
from src.config import *

class UI:
    """User interface manager"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_button = pygame.font.Font(None, 18)
        
        # Try to load Comic Sans font
        try:
            self.font_large = pygame.font.SysFont('comicsansms', 48)
            self.font_medium = pygame.font.SysFont('comicsansms', 32)
            self.font_small = pygame.font.SysFont('comicsansms', 24)
            self.font_button = pygame.font.SysFont('comicsansms', 18)
        except:
            # Fallback to default font
            pass
    
    def draw(self, score, health, paused, game_over):
        """Draw all UI elements"""
        self._draw_score(score)
        self._draw_health(health)
        self._draw_buttons(paused)
        
        if paused:
            self._draw_pause_overlay()
        
        if game_over:
            self._draw_game_over(score)
    
    def _draw_score(self, score):
        """Draw score in top right"""
        score_text = self.font_small.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topright = (SCREEN_WIDTH - 20, 20)
        
        # Background for better readability
        bg_rect = score_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
        
        self.screen.blit(score_text, score_rect)
    
    def _draw_health(self, health):
        """Draw health bar in top right"""
        health_text = self.font_small.render(f"Health: {health}", True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.topright = (SCREEN_WIDTH - 20, 60)
        
        # Background
        bg_rect = health_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect)
        
        self.screen.blit(health_text, health_rect)
        
        # Health bar
        bar_width = 200
        bar_height = 20
        bar_x = SCREEN_WIDTH - 210
        bar_y = 100
        
        # Background bar
        pygame.draw.rect(self.screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health bar
        health_percentage = max(0, health / PLAYER_MAX_HEALTH)
        health_width = int(bar_width * health_percentage)
        if health_width > 0:
            color = GREEN if health_percentage > 0.3 else (255, 165, 0) if health_percentage > 0.1 else RED
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    
    def _draw_buttons(self, paused):
        """Draw control buttons"""
        # Exit button (bottom left)
        exit_rect = pygame.Rect(20, SCREEN_HEIGHT - 60, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, RED, exit_rect)
        pygame.draw.rect(self.screen, WHITE, exit_rect, 2)
        
        exit_text = self.font_button.render("EXIT", True, WHITE)
        exit_text_rect = exit_text.get_rect(center=exit_rect.center)
        self.screen.blit(exit_text, exit_text_rect)
        
        # Pause/Resume button (bottom right)
        pause_rect = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 60, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_color = GREEN if paused else (255, 165, 0)  # Orange for pause, green for resume
        pygame.draw.rect(self.screen, button_color, pause_rect)
        pygame.draw.rect(self.screen, WHITE, pause_rect, 2)
        
        pause_text = "RESUME" if paused else "PAUSE"
        pause_surface = self.font_button.render(pause_text, True, WHITE)
        pause_text_rect = pause_surface.get_rect(center=pause_rect.center)
        self.screen.blit(pause_surface, pause_text_rect)
    
    def _draw_pause_overlay(self):
        """Draw pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("GAME PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instruction_text = self.font_medium.render("Click RESUME to continue", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(instruction_text, instruction_rect)
    
    def _draw_game_over(self, score):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Instructions
        instruction_text = self.font_medium.render("Click EXIT to quit", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(instruction_text, instruction_rect)
