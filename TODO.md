# TODO List

## Code Refactoring
- [ ] **Refactor Threading**: Move `Car.update_animation` logic into the main Ursina `update()` loop to avoid potential threading issues and align with engine best practices.
- [ ] **Input Handling**: Optimize the `input` list management in the `Car` class.
- [ ] **Cleanup**: Remove prototype files (e.g., `fucking_vehicle_steering_type_shi.py`) once all features are fully integrated.

## Features & Gameplay
- [ ] **Environment**: Add roads, buildings, or a track to drive on.
- [ ] **Collision**: Improve collision physics (currently using mesh collider which can be heavy).
- [ ] **Audio**: Add engine sounds, tire screeching, and background music.
- [ ] **UI Polish**: Improve the speedometer visuals and add a lap timer or score.

## Bugs / Issues
- [ ] **UV Mapping**: Ensure all 3D models have correct UV maps (ongoing work with `fix_uv_sides.py`).
- [ ] **Performance**: Monitor FPS when spawning many signs.
