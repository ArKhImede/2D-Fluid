import pygame

PARTICLE_MASS: float = 1.0
PARTICLE_RADIUS: int = 5

# Color gradient used to shape particles by speed
PARTICLE_COLORS: dict[str, str] = {
    "SLOW": "#195ba6",
    "MEDIUM": "#c4b61f",
    "FAST": "#a5261a",
}

NUM_PARTICLES: int = 300
INFLUENCE_RADIUS: int = 100  # radius of the mouse's "blob" push force
MAX_SPEED: float = (
    300.0  # used only to normalize particle color, not clamped in physics
)

GRAVITY: int = 200
SMOOTHING_RADIUS: int = (
    22  # SPH kernel radius: how far a particle "feels" its neighbors
)
REST_DENSITY: int = 15  # target density a particle relaxes toward
STIFFNESS: float = 8.0  # how strongly each density deviation converts into pressure
DAMPING: float = (
    0.6  # velocity retained (as a fraction) after a boundary/obstacle bounce
)
VISCOSITY_COEFF: float = (
    0.3  # how strongly neighboring particles' velocities pull into alignment
)

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
SCREEN_COLOR: str = "#050e1a"

FPS_TEXT_COLOR: str = "#ffffff"
NUM_PARTICLES_TEXT_COLOR: str = "#ffffff"

DT: float = 0.005  # fixed simulation timestep (seconds)
FPS: int = int(
    1 / DT
)  # frame cap matching the timestep, so motion doesn't speed up/slow down

MOUSE_FORCE: float = 900.0

# static circular obstacle particles collide with
OBSTACLE_CENTER: pygame.Vector2 = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
OBSTACLE_RADIUS: int = 50
OBSTACLE_COLOR: str = "#a69a9c"
