import pygame
from config import *


class Particle:
    """
    A single fluid particle: tracks its own kinematics and SPH properties
    (density, pressure), and knows how to draw itself.
    """

    def __init__(self, position: pygame.Vector2) -> None:
        self.position: pygame.Vector2 = position
        self.velocity: pygame.Vector2 = pygame.Vector2(0.0, 0.0)
        self.force: pygame.Vector2 = pygame.Vector2(
            0.0, 0.0
        )  # accumulated this frame, reset after integrate()
        self.mass: float = PARTICLE_MASS
        self.radius: int = PARTICLE_RADIUS
        self.max_speed: float = MAX_SPEED
        self.density: float = 0.0  # set each frame by Physics.compute_density
        self.pressure: float = 0.0  # set each frame by Physics.compute_pressure

    def apply_force(self, force: pygame.Vector2):
        """
        Accumulate a force to be resolved on the next integrate() call.
        """
        self.force += force

    def integrate(self, dt: float) -> None:
        """
        Semi-implicit Euler step: turn accumulated force into velocity and
        position, then clear the force accumulator for the next frame.
        """
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        self.force = pygame.Vector2(0.0, 0.0)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Color the particle by speed: blue (slow) -> yellow (medium) -> red (fast).
        """
        speed: float = self.velocity.length()
        speed_norm: float = min(speed / self.max_speed, 1.0)
        color: pygame.Color = pygame.Color(0, 0, 0)

        if speed_norm < 0.5:
            # lower half of the range: blend SLOW -> MEDIUM
            t = speed_norm / 0.5
            color = pygame.Color.lerp(
                pygame.Color(PARTICLE_COLORS["SLOW"]),
                pygame.Color(PARTICLE_COLORS["MEDIUM"]),
                t,
            )
        elif speed_norm >= 0.5:
            # upper half of the range: blend MEDIUM -> FAST
            t = (speed_norm - 0.5) / 0.5
            color = pygame.Color.lerp(
                pygame.Color(PARTICLE_COLORS["MEDIUM"]),
                pygame.Color(PARTICLE_COLORS["FAST"]),
                t,
            )

        pygame.draw.circle(surface, color, self.position, self.radius)
