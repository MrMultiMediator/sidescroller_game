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


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    terminate_game_loop = False

    window = Window(800, 600)

    disp = pygame.display.set_mode(((window.width,window.height)))
    surf = pygame.Surface((window.width,window.height))
    bg = Background("img/background.png")

    xvel = 40
    player = Player(window.width, bg.info, xvel=xvel)


    while not terminate_game_loop:
        clock.tick(30)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate_game_loop = True
                break

            if e.type == pygame.KEYDOWN:
                player.frame = 1
                if e.key == pygame.K_a:
                    player.keys_down.append('left')

                elif e.key == pygame.K_d:
                    player.keys_down.append('right')

                elif e.key == pygame.K_RSHIFT or e.key == pygame.K_LSHIFT:
                    if 'shift' not in player.keys_down:
                        player.keys_down.append('shift')

                elif e.key == pygame.K_RCTRL or e.key == pygame.K_LCTRL:
                    if 'ctrl' not in player.keys_down:
                        player.keys_down.append('ctrl')

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_a:
                    player.keys_down.remove('left')
                elif e.key == pygame.K_d:
                    player.keys_down.remove('right')
                elif e.key == pygame.K_RSHIFT or e.key == pygame.K_LSHIFT:
                    if 'shift' in player.keys_down:
                        player.keys_down.remove('shift')
                elif e.key == pygame.K_RCTRL or e.key == pygame.K_LCTRL:
                    if 'ctrl' in player.keys_down:
                        player.keys_down.remove('ctrl')


        surf.fill((0,0,200))
        #surf.blit(bg.surf, (bg.x,0))

        delta = player.update(surf, bg)
        bg.update(surf, delta)
        update_screen(surf, bg, player)

        disp.blit(surf, (0,0))
        pygame.display.update()


