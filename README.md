
---

# 🕹️ Terminal Adventure Game

A simple yet engaging terminal-based shooting and survival game built with Python's `curses` module. Navigate the world, collect food, dodge or shoot enemies, and try to survive!

## 📦 Features

- Player movement across a randomly generated terminal map.
- Randomly spawning **foods**, **guns**, and **enemies**.
- Shooting mechanism based on player's direction.
- Score and life tracking.
- Win or lose scenarios.
- Dynamic enemy movement and simple AI.
- Retro ASCII-style display.

## 🎮 Gameplay Overview

You control a player (displayed as `X`) who must:

- **Collect food** (`*`) to gain points.
- **Pick up guns** (`0`) to get more shots.
- **Shoot enemies** (`E`) using direction-based bullets (`o`).
- Avoid enemies or you'll lose lives (`❤`).
- Reach a **score of 1000 to win**, or lose all 3 lives and it's game over.

## ⌨️ Controls

| Key         | Action              |
|-------------|---------------------|
| Arrow Keys  | Move (Up, Down, Left, Right) |
| Space (`␣`) | Fire in current direction |
| Q           | Quit the game       |

## 💻 Requirements

- Python 3.x
- A terminal that supports `curses` (Unix-based systems like macOS or Linux)

> ⚠️ On Windows, you might need to run it using the `Windows Subsystem for Linux (WSL)` or install a curses-compatible package like [`windows-curses`](https://pypi.org/project/windows-curses/).

Install with:

```bash
pip install windows-curses  # Only for Windows
```

## ▶️ How to Run

1. Save the game code in a file, e.g., `main.py`
2. Run the file:

```bash
python main.py
```

3. Use arrow keys to move and spacebar to shoot.
4. Have fun surviving and scoring!

## 🛠️ Code Structure

- `init()` - Initializes the game map and entities.
- `draw()` - Renders the screen.
- `move()`, `move_enemy()`, `move_fire()` - Handles entity movement.
- `check_food()`, `check_gun()` - Logic for collectibles.
- `fire()` - Handles firing bullets.
- `random_place()` - Random empty location generator.
- `in_area()` - Keeps positions within bounds.

## 🧠 Notes

- Enemies move randomly toward the player with low probability.
- Food and gun items respawn when collected or expired.
- Fires destroy enemies and vanish when hitting walls.

## 📜 License

MIT License – feel free to use and modify this for your own projects.

---
