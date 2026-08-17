import pygame
from particle import Particle
from config import *
from spatial_hash import SpatialHash


class Physics:
    """
    Owns the SPH (Smoothed Particle Hydrodynamics) simulation step:
    gravity, density/pressure computation, pressure+viscosity forces,
    integration, and collision handling (screen bounds + obstacle).
    """

    def __init__(self) -> None:
        self.gravity: pygame.Vector2 = pygame.Vector2(0.0, GRAVITY)
        self.smoothing_radius: int = SMOOTHING_RADIUS
        self.stiffness: float = STIFFNESS
        self.rest_density: int = REST_DENSITY
        self.damping: float = DAMPING
        self.influence_radius: int = INFLUENCE_RADIUS
        self.viscosity_coeff: float = VISCOSITY_COEFF
        self.mouse_force: float = MOUSE_FORCE
        self.spatial_hash: SpatialHash = SpatialHash(self.smoothing_radius)
        self.game_width: int = SCREEN_WIDTH
        self.game_height: int = SCREEN_HEIGHT

    def apply_gravity(self, particles: list[Particle]) -> None:
        for particle in particles:
            particle.apply_force(particle.mass * self.gravity)

    def handle_boundaries(self, particles: list[Particle]) -> None:
        """
        Clamp particles to the screen and reflect + dampen their velocity
        on the axis they crossed, so they bounce off the edges instead of
        leaving the window.
        """
        for particle in particles:
            if particle.position.x < 0:
                particle.position.x = 0
                particle.velocity.x *= -self.damping
            if particle.position.x > self.game_width:
                particle.position.x = self.game_width
                particle.velocity.x *= -self.damping
            if particle.position.y < 0:
                particle.position.y = 0
                particle.velocity.y *= -self.damping
            if particle.position.y > self.game_height:
                particle.position.y = self.game_height
                particle.velocity.y *= -self.damping

    def rebuild_spatial_hash(self, particles: list[Particle]) -> None:
        """
        Rebuild the neighbor-search grid from current positions. Must be
        called once per frame before any neighbor query.
        """
        self.spatial_hash.clear()

        for particle in particles:
            self.spatial_hash.insert(particle)

    def compute_density(self, particles: list[Particle]) -> None:
        """
        SPH density estimate: each particle's density is a weighted sum
        of nearby particles' mass, using a linear falloff kernel (closer
        neighbors count more).
        """
        for particle in particles:
            self.spatial_hash.insert(particle)

        for particle_i in particles:
            neighbors = self.spatial_hash.query(particle_i)
            density: float = 0.0
            for particle_j in neighbors:
                dist = particle_i.position.distance_to(particle_j.position)
                if dist < self.smoothing_radius:
                    density += particle_j.mass * (1 - dist / self.smoothing_radius)
            particle_i.density = density

    def compute_pressure(self, particles: list[Particle]) -> None:
        """
        Equation of state: pressure grows linearly with how much a
        particle's density exceeds the rest density (like a spring pushing
        back against compression).
        """
        for particle_i in particles:
            pressure: float = self.stiffness * (particle_i.density - self.rest_density)
            particle_i.pressure = pressure

    def compute_pressure_and_viscosity_forces(self, particles: list[Particle]) -> None:
        """
        For each unique neighboring pair (i, j) within the smoothing radius:
        push them apart based on their combined pressure (pressure force), and
        pull their velocities toward each other (viscosity force), applying
        equal-and-opposite forces to conserve momentum.
        """
        for particle in particles:
            self.spatial_hash.insert(particle)

        for i, particle_i in enumerate(particles):
            neighbors = self.spatial_hash.query(particle_i)
            for particle_j in neighbors:
                if particle_j in neighbors:
                    if particle_j is particle_i:
                        continue

                # process each pair once (skip if we'll hit it from the other side)
                if id(particle_j) <= id(particle_i):
                    continue

                offset: pygame.Vector2 = particle_i.position - particle_j.position
                distance: float = offset.length()

                if 0.0 < distance < self.smoothing_radius:
                    direction = offset.normalize()
                    strength = (particle_i.pressure + particle_j.pressure) / 2.0
                    weight = 1 - distance / self.smoothing_radius

                    pressure_force = -direction * strength * weight / particle_i.density
                    vel_diff = particle_j.velocity - particle_i.velocity
                    viscosity_force = (
                        self.viscosity_coeff * vel_diff * weight / particle_i.density
                    )
                    total_force = pressure_force + viscosity_force

                    particle_i.apply_force(total_force)
                    particle_j.apply_force(-total_force)

    def integrate(self, particles: list[Particle], dt: float) -> None:
        for particle in particles:
            particle.integrate(dt)

    def apply_blob_force(
        self, particles: list[Particle], mouse_velocity: pygame.Vector2
    ) -> None:
        """
        While the mouse button is held, push nearby particles in the
        direction the mouse is moving - stronger the closer they are.
        """
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        for particle in particles:
            offset: pygame.Vector2 = particle.position - mouse_pos
            distance: float = offset.length()

            if 0.0 < distance < self.influence_radius:
                strength = 1 - distance / self.influence_radius
                force = mouse_velocity * strength * self.mouse_force
                particle.apply_force(force)

    def obstacle_collision(self, particles: list[Particle]) -> None:
        """
        Push any particle overlapping the static circular obstacle back
        to its surface, and reflect its velocity off the obstacle's
        normal (elastic bounce, then damped).
        """
        for particle in particles:
            offset = particle.position - OBSTACLE_CENTER
            distance = offset.length()
            min_dist = OBSTACLE_RADIUS + particle.radius

            if 0 < distance < min_dist:
                normal = offset.normalize()
                particle.position = OBSTACLE_CENTER + normal * min_dist
                particle.velocity -= 2 * (particle.velocity.dot(normal)) * normal
                particle.velocity *= self.damping

    def step(
        self,
        particles: list[Particle],
        dt: float,
        mouse_pressed,
        mouse_velocity: pygame.Vector2,
    ) -> None:
        """
        Runs one full physics frame, in order:
        1. external forces (gravity, mouse)
        2. rebuild the neighbor grid once for this frame's positions
        3. SPH density -> pressure -> pressure/viscosity forces
        4. integrate forces into motion
        5. resolve collisions (screen bounds, obstacle)
        """
        self.apply_gravity(particles)

        if mouse_pressed:
            self.apply_blob_force(particles, mouse_velocity)

        self.rebuild_spatial_hash(particles)
        self.compute_density(particles)
        self.compute_pressure(particles)
        self.compute_pressure_and_viscosity_forces(particles)
        self.integrate(particles, dt)
        self.handle_boundaries(particles)
        self.obstacle_collision(particles)
