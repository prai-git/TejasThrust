"""
Configuration constants for TejasThrust game
"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
SKY_COLOR = (135, 206, 235)  # Sky blue
PLAYER_COLOR = (0, 100, 255)  # Blue
ENEMY_COLOR = (50, 50, 50)  # Dark gray/black
LASER_COLOR = (255, 255, 0)  # Yellow
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CLOUD_COLOR = (255, 255, 255)

# Game settings
FPS = 60
PLAYER_MAX_HEALTH = 100
ENEMY_HEALTH = 2
PLAYER_SPEED = 5
ENEMY_SPEED = 2
LASER_SPEED = 8
ENEMY_LASER_SPEED = 10

# Spawning
ENEMY_SPAWN_INTERVAL = 1000  # milliseconds
ENEMY_SHOOT_CHANCE = 0.015  # probability per frame

# Burst mode settings for enemy planes
ENEMY_BURST_CHANCE = 0.002  # probability per frame to activate burst mode (0.2%)
ENEMY_BURST_SHOTS = 3  # number of shots in burst sequence

# Plane dimensions
PLANE_WIDTH = 60
PLANE_HEIGHT = 40
LASER_WIDTH = 4
LASER_HEIGHT = 10

# UI settings
FONT_SIZE = 24
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
