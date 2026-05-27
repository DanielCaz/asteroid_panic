# Asteroid Panic

Asteroid Panic is a simple game where you control a spaceship and try to avoid incoming asteroids. The game is built using Python and the Pygame library.

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) - An extremely fast Python package and project manager, written in Rust.
- Python installed via uv (`uv python install`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DanielCaz/asteroid_panic.git
   ```

2. Navigate to the project directory:

   ```bash
   cd asteroid_panic
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   uv sync
   ```

### Running the Game

To start the game, run the following command in your terminal:

```bash
uv run main.py
```

## Gameplay

- Use WASD to move your spaceship.
- Avoid incoming asteroids that will appear randomly on the screen.
- Collect red jerry cans to refuel your spaceship.
- The game ends when your fuel runs out or you collide with an asteroid.

## Assets

Runtime images live under `assets/images/`, grouped by gameplay role:

- `assets/images/player/`
- `assets/images/obstacles/`
- `assets/images/pickups/`

Editable source art lives under `assets/source/`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
