# TejasThrust (TT) - Fighter Plane Game

A professional single-player dog fight game designed for kids aged 5-12 years. Built with Python and Pygame, featuring smooth animations, engaging gameplay, and kid-friendly controls.

![TejasThrust Logo](./assets/images/logo.png)

## 🎮 Game Features

- **Single Player Action**: Battle against computer-controlled enemy planes
- **Professional UI**: Clean, modern interface with animated clouds background
- **Kid-Friendly Controls**: Simple arrow keys for movement, spacebar to shoot
- **Health System**: Player has 100 health points, enemies require 2 hits to defeat
- **BOSS Planes**: Special red BOSS planes appear after every 50 enemy kills
- **Background Music**: Immersive audio experience during gameplay
- **Smooth Animations**: All movements are fluid and responsive
- **Pause/Resume**: Full game state management with pause functionality
- **Score Tracking**: Real-time score display and final score on game over
- **Comic Sans Font**: Child-friendly typography throughout the game

## 🎯 Game Specifications

### Player Controls
- **Arrow Keys**: Move the blue player plane in 8 directions
- **Space Bar**: Shoot yellow lasers at enemy planes
- **Mouse**: Click buttons for pause/resume and exit

### Gameplay Mechanics
- Player plane is **blue colored**
- Enemy planes are **black/dark gray colored**
- BOSS planes are **red colored** and appear after every 50 enemy kills
- Lasers are **bright yellow** with glow effects
- Enemy planes spawn every 2 seconds and move randomly
- Player health decreases by 1 when hit by enemy lasers
- Player health decreases by 5 when hit by BOSS lasers
- Enemy planes are destroyed after 2 hits
- BOSS planes require 5 hits to defeat
- Score increases by 1 for each enemy plane destroyed
- Score increases by 5 for each BOSS plane destroyed
- Game ends when player health reaches 0

### Visual Features
- Open sky background with **slowly moving clouds**
- Professional 2D plane sprites (triangular design)
- Health bars displayed above damaged enemy planes
- Real-time health and score display in top-right corner
- Exit button in bottom-left corner
- Pause/Resume button in bottom-right corner
- Distinctive larger BOSS planes with more aggressive behavior

### Audio Features
- Background music plays continuously during gameplay
- Music loops seamlessly for uninterrupted experience

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download the game**:
   ```bash
   git clone <repository-url>
   cd TT
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## 🎲 How to Play

1. **Start the game** by running `python main.py`
2. **Move your blue plane** using the arrow keys
3. **Shoot lasers** by pressing the spacebar
4. **Avoid enemy fire** - red lasers from black enemy planes
5. **Destroy enemies** by hitting them twice with your lasers
6. **Watch your health** - displayed in the top-right corner
7. **Pause anytime** by clicking the PAUSE button
8. **Exit the game** by clicking the EXIT button

## 🏗️ Project Structure

```
TT/
├── main.py                 # Main game entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── src/                   # Source code
│   ├── __init__.py
│   ├── config.py          # Game configuration and constants
│   ├── plane.py           # Player and enemy plane classes
│   ├── laser.py           # Laser projectile class
│   ├── cloud.py           # Background cloud animation
│   └── ui.py              # User interface components
├── assets/                # Game assets
│   ├── images/            # Sprite images (placeholder)
│   └── sounds/            # Sound effects (placeholder)
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_game.py       # Main game tests
│   ├── test_planes.py     # Plane class tests
│   └── test_ui.py         # UI component tests
├── .github/               # GitHub configuration
│   └── copilot-instructions.md
└── .vscode/               # VS Code configuration
    └── tasks.json
```

## 🧪 Testing

Run the comprehensive test suite to ensure all game specifications are met:

```bash
# Run all tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src

# Run specific test file
pytest tests/test_game.py -v
```

## 🎨 Customization

### Difficulty Adjustment
The game difficulty can be adjusted by modifying values in `src/config.py`:
- `ENEMY_SPAWN_INTERVAL`: Time between enemy spawns (default: 2000ms)
- `ENEMY_SHOOT_CHANCE`: Probability of enemy shooting per frame (default: 0.005)
- `BOSS_SPAWN_COUNT`: Number of enemies before a boss appears (default: 50)
- `BOSS_HEALTH`: Boss plane health (default: 5)
- `BOSS_LASER_DAMAGE`: Damage dealt by boss lasers (default: 5)
- `PLAYER_SPEED` and `ENEMY_SPEED`: Movement speeds
- `PLAYER_MAX_HEALTH`: Starting player health (default: 100)

### Audio Customization
- Replace `TT.wav` in the `assets/sounds` folder with your own audio file
- Adjust volume settings in the game code

### Visual Customization
- Modify colors in `src/config.py`
- Adjust plane sizes with `PLANE_WIDTH` and `PLANE_HEIGHT`
- Change screen dimensions with `SCREEN_WIDTH` and `SCREEN_HEIGHT`

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Performance Issues**: Lower the FPS in `config.py` if the game runs slowly
3. **Font Issues**: The game automatically falls back to default fonts if Comic Sans is unavailable

### System Requirements
- **Minimum**: Python 3.8, 2GB RAM, DirectX 9.0c compatible graphics
- **Recommended**: Python 3.10+, 4GB RAM, dedicated graphics card

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 🎯 Future Enhancements

- Additional sound effects for shooting and explosions
- Power-ups and special weapons
- Multiple difficulty levels
- High score persistence
- Multiplayer support
- Touch screen controls for tablets
- More BOSS types with unique abilities

## 📞 Support

For questions, bug reports, or feature requests, please open an issue on the project repository.

---

**TejasThrust** - Where young pilots take to the skies! ✈️

## Author

**Praveen Rai & Krishang Rai**
