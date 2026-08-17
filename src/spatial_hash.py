import pygame
from particle import Particle


class SpatialHash:
    """
    Uniform grid used to find nearby particles in ~0(1) instead of checking
    every particle against every other particle (0(n^2)). Particles are
    bucketed into cells sized to the SPH smoothing radius, so a particle's
    neighbors are guaranteed to be in its own cell or one of the 8 surrounding it.
    """

    def __init__(self, cell_size: int) -> None:
        self.cell_size: int = cell_size
        self.cells: dict[tuple[int, int], list[Particle]] = {}

    def clear(self) -> None:
        """
        Empty the grid - called once per frame before rebuilding it from
        current particle position.
        """
        self.cells.clear()

    def insert(self, particle: Particle) -> None:
        cell = self.get_cell(particle.position)
        if cell not in self.cells:
            self.cells[cell] = []
        self.cells[cell].append(particle)

    def get_cell(self, position: pygame.Vector2) -> tuple[int, int]:
        """
        Map a world position to its grid cell coordinates.
        """
        return (int(position.x // self.cell_size), int(position.y // self.cell_size))

    def query(self, particle: Particle) -> list[Particle]:
        """
        Return every particle in the 3x3 block of cells around this
        particle's cell (its own cell + 8 neighbors) - a superset of its
        true SPH neighbors, filtered by exact distance later.
        """
        neighbors = []
        cx, cy = self.get_cell(particle.position)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                neighbor_cell = (cx + dx, cy + dy)
                if neighbor_cell in self.cells:
                    neighbors.extend(self.cells[neighbor_cell])
        return neighbors
