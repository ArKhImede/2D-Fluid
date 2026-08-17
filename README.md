# 💧 2D Fluid Simulation

A 2D SPH (Smoothed Particle Hydrodynamics) fluid simulation built with `pygame`. Particles interact through density, pressure, and viscosity forces to produce fluid-like motion, while reacting to gravity, a static obstacle, mouse input, and screen boundaries in real time.

## ⚙️ Features

- **SPH fluid dynamics** — each particle computes local density and pressure from nearby particles, producing forces that push the fluid toward a target rest density
- **Viscosity** — neighboring particles' velocities pull toward each other, smoothing out the flow
- **Spatial hashing** — particles are bucketed into a uniform grid so neighbor queries stay fast as particle count grows
- **Mouse interaction** — click and drag to push the fluid around with a "blob" force
- **Obstacle collision** — a static circular obstacle deflects and dampens any particle that touches it
- **Boundary handling** — particles bounce off the edges of the screen with damped velocity
- **Speed visualization** — particles are colored blue → yellow → red as their speed increases

## 🕹️ Demo Controls

| Input | Action |
|---|---|
| `Left Click + Drag` | Push nearby particles in the direction of mouse movement |
| Close window | Quit the simulation |

## 🗂️ Project Structure
```
.
├── main.py             # Entry point — game loop, event handling
├── particle.py          # Particle class (position, velocity, density, pressure, drawing)
├── physics.py            # SPH simulation: density, pressure, viscosity, integration, collisions
├── spatial_hash.py        # Uniform grid for fast neighbor lookups
├── utils.py                 # Helper functions (random spawn position)
└── config.py                  # All tunable constants (physics coefficients, colors, sizes, etc.)
```

## Installation

```
https://github.com/ArKhImede/2D-Fluid.git
```

```
cd 2D-Fluid
```

```
pip install pygame
```

## Usage

Run the simulation with:
```python main.py```

A window will open showing the fluid settling under gravity. Click and drag anywhere on the screen to stir the particles.

## Configuration

All simulation parameters live in `config.py`, including:
- `NUM_PARTICLES`, `PARTICLE_MASS`, `PARTICLE_RADIUS` — particle count and physical size
- `SMOOTHING_RADIUS`, `REST_DENSITY`, `STIFFNESS` — how the fluid resists compression
- `VISCOSITY_COEFF` — how strongly particles' velocities smooth toward their neighbors
- `GRAVITY`, `DAMPING` — external force and energy loss on collision
- `INFLUENCE_RADIUS`, `MOUSE_FORCE` — strength and reach of the mouse interaction
- `OBSTACLE_CENTER`, `OBSTACLE_RADIUS` — position and size of the static obstacle
- `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `DT` — window size and simulation timestep
- Color settings for particles, obstacle, and background

Tweak these values to experiment with different fluid behaviors, from thick and viscous to loose and splashy.

## How It Works

Each frame, `Physics.step()` runs the following pipeline:
1. **External forces** — gravity is applied to every particle, plus a mouse-driven "blob" force while the left button is held
2. **Neighbor search** — all particles are rebucketed into a `SpatialHash` grid sized to the smoothing radius, so each particle only needs to check nearby cells instead of every other particle
3. **Density** — each particle sums a distance-weighted contribution from its neighbors to estimate local fluid density
4. **Pressure** — density above or below the configured rest density is converted into a pressure value via `STIFFNESS`
5. **Pressure & viscosity forces** — each neighboring pair pushes apart based on combined pressure, and pulls their velocities together based on `VISCOSITY_COEFF`, applied as equal-and-opposite forces
6. **Integration** — accumulated forces are converted into velocity and position changes
7. **Collisions** — particles are bounced off the screen boundaries and off the static circular obstacle, both with damped velocity

`Particle.draw()` then colors each particle by its current speed before `main.py` flips the display.

## 🎥 Video

Here is a video showcasing the simulation in action:

https://github.com/user-attachments/assets/024ab9ce-09bd-44e9-8b6a-86105e09b574
