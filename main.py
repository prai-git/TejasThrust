"""
TejasThrust (TT) - Single Player Dog Fight Game
A professional web-based fighter plane game for kids aged 5-12
"""

import pygame
import sys
import random
import math
from typing import List, Tuple
from src.plane import PlayerPlane, EnemyPlane, BossPlane
from src.laser import Laser
from src.cloud import Cloud
from src.ui import UI
from src.config import *

class TejasThrust:
    """Main game class for TejasThrust dog fight game"""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Screen setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AMCA - Fighter Plane Game")
        
        # Game clock
        self.clock = pygame.time.Clock()

        # Background music
        pygame.mixer.music.load('assets/sounds/TT.wav')  # Replace with your music file
        pygame.mixer.music.play(-1)  # Play the music in a loop
        
        # Game state
        self.running = True
        self.paused = False
        self.game_over = False
        
        # Score and health
        self.score = 0
        self.player_health = PLAYER_MAX_HEALTH
        self.enemies_killed = 0  # Track how many enemies have been destroyed
        self.boss_active = False  # Flag to track if boss is currently active
        
        # Game objects
        self.player = PlayerPlane(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies: List[EnemyPlane] = []
        self.boss: BossPlane = None  # Boss plane reference
        self.player_lasers: List[Laser] = []
        self.enemy_lasers: List[Laser] = []
        self.clouds: List[Cloud] = []
        
        # UI
        self.ui = UI(self.screen)
        
        # Initialize clouds
        self._init_clouds()
        
        # Last enemy spawn time
        self.last_enemy_spawn = 0
        
        # Load fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        
    def _init_clouds(self):
        """Initialize background clouds"""
        for _ in range(8):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            size = random.randint(50, 150)
            speed = random.uniform(0.2, 0.8)
            self.clouds.append(Cloud(x, y, size, speed))
    
    def spawn_enemy(self):
        """Spawn a new enemy plane"""
        current_time = pygame.time.get_ticks()
        
        # Check if it's time to spawn a boss
        if self.enemies_killed > 0 and self.enemies_killed % BOSS_SPAWN_COUNT == 0 and not self.boss_active:
            # Spawn a boss plane at the top center
            self.boss = BossPlane(SCREEN_WIDTH // 2, 100)
            self.boss_active = True
            return
            
        # Only spawn regular enemies if no boss is active and it's time
        if current_time - self.last_enemy_spawn > ENEMY_SPAWN_INTERVAL and not self.boss_active:
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(-100, -50)
            enemy = EnemyPlane(x, y)
            self.enemies.append(enemy)
            self.last_enemy_spawn = current_time
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Player shoots
                    laser = self.player.shoot()
                    if laser:
                        self.player_lasers.append(laser)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check button clicks
                mouse_pos = pygame.mouse.get_pos()
                
                # Exit button (bottom left)
                exit_rect = pygame.Rect(20, SCREEN_HEIGHT - 60, 80, 40)
                if exit_rect.collidepoint(mouse_pos):
                    self.running = False
                
                # Pause/Resume button (bottom right)
                pause_rect = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 60, 80, 40)
                if pause_rect.collidepoint(mouse_pos):
                    self.paused = not self.paused
    
    def update(self):
        """Update game logic"""
        if self.paused or self.game_over:
            return
        
        # Handle player input
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        
        # Spawn enemies
        self.spawn_enemy()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Remove enemies that are off screen
            if enemy.y > SCREEN_HEIGHT + 50:
                self.enemies.remove(enemy)
            
            # Enemy shooting
            if random.random() < ENEMY_SHOOT_CHANCE:
                laser = enemy.shoot()
                if laser:
                    self.enemy_lasers.append(laser)
        
        # Update boss if active
        if self.boss_active and self.boss:
            self.boss.update()
            
            # Boss shooting (more frequent)
            if random.random() < BOSS_SHOOT_CHANCE:
                laser = self.boss.shoot()
                if laser:
                    self.enemy_lasers.append(laser)
        
        # Update lasers
        for laser in self.player_lasers[:]:
            laser.update()
            if laser.y < -10:
                self.player_lasers.remove(laser)
        
        for laser in self.enemy_lasers[:]:
            laser.update()
            if laser.y > SCREEN_HEIGHT + 10:
                self.enemy_lasers.remove(laser)
        
        # Update clouds
        for cloud in self.clouds:
            cloud.update()
        
        # Check collisions
        self._check_collisions()
        
        # Check game over
        if self.player_health <= 0:
            self.game_over = True
    
    def _check_collisions(self):
        """Check all collision detection"""
        # Player lasers hit enemies
        for laser in self.player_lasers[:]:
            # Check collision with regular enemies
            for enemy in self.enemies[:]:
                if laser.get_rect().colliderect(enemy.get_rect()):
                    if laser in self.player_lasers:  # Avoid processing removed lasers
                        self.player_lasers.remove(laser)
                    enemy.take_damage()
                    
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += 1
                        self.enemies_killed += 1
                    break
            
            # Check collision with boss (if active)
            if self.boss_active and self.boss and laser in self.player_lasers:
                if laser.get_rect().colliderect(self.boss.get_rect()):
                    self.player_lasers.remove(laser)
                    self.boss.take_damage()
                    
                    if self.boss.health <= 0:
                        self.boss = None
                        self.boss_active = False
                        self.score += 5  # Bonus points for defeating boss
                        self.enemies_killed += 1  # Count boss as an enemy for spawning logic
        
        # Enemy lasers hit player
        for laser in self.enemy_lasers[:]:
            if laser.get_rect().colliderect(self.player.get_rect()):
                self.enemy_lasers.remove(laser)
                self.player_health -= laser.damage  # Use the laser's damage value
    
    def draw(self):
        """Draw all game objects"""
        # Sky background
        self.screen.fill(SKY_COLOR)
        
        # Draw clouds
        for cloud in self.clouds:
            cloud.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw boss if active
        if self.boss_active and self.boss:
            self.boss.draw(self.screen)
        
        # Draw lasers
        for laser in self.player_lasers:
            laser.draw(self.screen)
        
        for laser in self.enemy_lasers:
            laser.draw(self.screen)
        
        # Draw UI
        self.ui.draw(self.score, self.player_health, self.paused, self.game_over)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TejasThrust()
    game.run()
