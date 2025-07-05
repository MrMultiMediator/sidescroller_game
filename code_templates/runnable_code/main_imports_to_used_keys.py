from background import Background
from player import Player
import pygame
import sys

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height


def update_screen(surf, bg, player):
    surf.blit(bg.surf, (bg.x, 0))
    surf.blit(player.surf, (player.x, player.y))
    surf.blit(player.health_bar.surf, (player.health_bar.x, player.health_bar.y))

gravity = 5 # gravitational acceleration

used_keys = [
    pygame.K_a,
    pygame.K_d,
    pygame.K_j,
    pygame.K_k,
    pygame.K_l,
    pygame.K_RSHIFT,
    pygame.K_LSHIFT,
    pygame.K_RCTRL,
    pygame.K_LCTRL,
    pygame.K_SPACE
]

