# Drivy 3D

A 3D driving simulation built with Python and the [Ursina Engine](https://www.ursinaengine.org/).

## Features

- **Physics-based Driving**: Car physics including acceleration, friction, and momentum.
- **Interactive UI**: Functional speedometer that responds to the car's speed.
- **Dynamic Environment**: Spawn traffic signs dynamically.
- **Camera Controls**: Toggle between First-Person and Third-Person views, and adjust FOV.

## Controls

| Key | Action |
| :--- | :--- |
| **W** | Accelerate |
| **S** | Brake / Reverse |
| **A** | Turn Left |
| **D** | Turn Right |
| **Space** | Spawn a Traffic Sign |
| **F** | Toggle FOV (Zoom) |
| **V** | Toggle Camera View (First/Third Person) |
| **Q** / **Esc** | Quit Application |

## Installation & Running

1. Ensure you have Python installed (3.14 recommended).
2. Install Ursina:
   ```bash
   pip install ursina
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Assets

- **Car**: 2025 Bugatti Bolide
- **Sign**: Custom "Daddy" sign class with animation.
