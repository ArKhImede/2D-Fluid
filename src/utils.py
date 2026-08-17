import pygame
import random
from config import *


def spawn_random_pos() -> pygame.Vector2:
    """
    Uniform random position anywhere within the screen bounds - used to
    scatter particles at simulation start.
    """
    rand_x = random.randint(0, SCREEN_WIDTH)
    rand_y = random.randint(0, SCREEN_HEIGHT)
    return pygame.Vector2(rand_x, rand_y)
