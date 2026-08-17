import pygame
from particle import Particle
from physics import Physics
from utils import *
from config import *


class Simulation:

    def __init__(self) -> None:
        self.physics: Physics = Physics()
        self.particles: list[Particle] = []
        self.dt: float = DT
        self.fps: int = FPS
        self.current_fps: int = 0
        self.num_particles: int = NUM_PARTICLES
        self.fps_text = None
        self.num_particles_text = None
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 25)
        self.previous_mouse_pos: pygame.Vector2 = pygame.Vector2(
            0, 0
        )  # used to derive mouse "velocity" each frame

    def spawn_particles(self):
        for _ in range(self.num_particles):
            rand_particle_pos = spawn_random_pos()
            particle = Particle(rand_particle_pos)
            self.particles.append(particle)

    def spawn_obstacle(self, surface: pygame.Surface):
        pygame.draw.circle(surface, OBSTACLE_COLOR, OBSTACLE_CENTER, OBSTACLE_RADIUS)

    def create_texts(self, surface: pygame.Surface) -> None:
        fps_text = self.font.render(
            f"FPS: {int(self.current_fps)}", True, FPS_TEXT_COLOR
        )
        surface.blit(fps_text, (20, 20))

        num_particles_text = self.font.render(
            f"Total Particles: {self.num_particles}", True, NUM_PARTICLES_TEXT_COLOR
        )
        surface.blit(num_particles_text, (20, 40))

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("2D Fluid")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.current_fps = clock.get_fps()

            screen.fill(SCREEN_COLOR)
            self.spawn_obstacle(screen)

            # mouse "velocity" = how far the cursor moved since last frame
            current_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            mouse_velocity = current_mouse_pos - self.previous_mouse_pos
            self.previous_mouse_pos = current_mouse_pos

            mouse_down = pygame.mouse.get_pressed()[0]
            self.physics.step(self.particles, self.dt, mouse_down, mouse_velocity)

            for particle in self.particles:
                particle.draw(screen)

            self.create_texts(screen)

            pygame.display.flip()

            clock.tick(self.fps)

        pygame.quit()


sim = Simulation()
sim.spawn_particles()
sim.run()
