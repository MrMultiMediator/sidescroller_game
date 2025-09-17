from background import Background
from player import Player
from enemies.fighter import Fighter
import pygame
import sys

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height


def update_screen(surf, bg, player, enemies):
    surf.blit(bg.surf, (bg.x, 0))
    surf.blit(player.surf, (player.x, player.y))
    surf.blit(player.health_bar.surf, (player.health_bar.x, player.health_bar.y))

    for enemy in enemies:
        surf.blit(enemy.surf, (enemy.x, enemy.y))

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

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    terminate_game_loop = False

    window = Window(800, 600)

    disp = pygame.display.set_mode(((window.width,window.height)))
    surf = pygame.Surface((window.width,window.height))
    bg = Background("img/background.png")

    xvel = 40
    player = Player(window.width, window.height, bg.info, gravity, xvel=xvel)

    enemies = [
        Fighter(700, player.gravity, "img/enemies/e1", bg.info),
        Fighter(1700, player.gravity, "img/enemies/e1", bg.info),
        Fighter(2700, player.gravity, "img/enemies/e1", bg.info),
        Fighter(3700, player.gravity, "img/enemies/e1", bg.info),
        Fighter(4700, player.gravity, "img/enemies/e1", bg.info)
    ]

    for enemy in enemies:
        player.new_enemy(enemy)

    while not terminate_game_loop:
        clock.tick(30)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate_game_loop = True
                break

            if player.status == "fall1":
                continue

            if e.type == pygame.KEYDOWN and e.key in used_keys:
                player.frame = 1
                if e.key == pygame.K_a:
                    if "left" not in player.keys_down:
                        player.keys_down.append('left')

                elif e.key == pygame.K_d:
                    if "right" not in player.keys_down:
                        player.keys_down.append('right')

                elif e.key == pygame.K_RSHIFT or e.key == pygame.K_LSHIFT:
                    if 'shift' not in player.keys_down:
                        player.keys_down.append('shift')

                elif e.key == pygame.K_RCTRL or e.key == pygame.K_LCTRL:
                    if 'ctrl' not in player.keys_down:
                        player.keys_down.append('ctrl')

                elif e.key == pygame.K_j:
                    if 'j' not in player.keys_down:
                        player.keys_down.append('j')

                elif e.key == pygame.K_k:
                    if 'k' not in player.keys_down:
                        player.keys_down.append('k')

                elif e.key == pygame.K_l:
                    if 'l' not in player.keys_down:
                        player.keys_down.append('l')

            if e.type == pygame.KEYUP and e.key in used_keys:
                player.frame = 1
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
                elif e.key == pygame.K_j:
                    if 'j' in player.keys_down:
                        player.keys_down.remove('j')

                        if 'ctrl' in player.keys_down:
                            player.frame = 6
                            player.status = "kneel"
                            
                elif e.key == pygame.K_k:
                    if 'k' in player.keys_down:
                        player.keys_down.remove('k')
                elif e.key == pygame.K_l:
                    if 'l' in player.keys_down:
                        player.keys_down.remove('l')
                elif e.key == pygame.K_SPACE:
                    if player.status != "jump":
                        player.status = "jump"
                        player.y_vel = player.jump_strength


        surf.fill((0,0,200))
        #surf.blit(bg.surf, (bg.x,0))

        delta = player.update(bg)
        player_info = player.get_info()
        bg.update(surf, delta)
        for enemy in enemies:
            enemy.update(delta, player_info)

        # --- Collision and Damage Logic ---
        p_mask = pygame.mask.from_surface(player.surf)
        for e_index, enemy in enumerate(enemies):
            e_mask = pygame.mask.from_surface(enemy.surf)

            offset_x = player.x - enemy.x
            offset_y = player.y - enemy.y

            if e_mask.overlap(p_mask, (offset_x, offset_y)):
                # Player attacks enemy
                if str(player.status) in player.damage.keys() and not player.attack_has_dealt_damage[enemy.name]:
                    enemy.take_damage(player.damage[str(player.status)])
                    player.attack_has_dealt_damage[enemy.name] = True
                    #print(f"Player hit {type(enemy).__name__}_{e_index} with {player.status}, shield = {enemy.shield}, hp = {enemy.hp}")

                # Enemy attacks player
                if enemy.status in enemy.damage and not enemy.attack_has_dealt_damage:
                    player.take_damage(enemy.damage[str(enemy.status)])
                    enemy.attack_has_dealt_damage = True

                    #print(f"{enemy.hp}, {enemy.shield}, {player.status in player.damage.keys()}, {not player.attack_has_dealt_damage[enemy.name]}")
                    #print(f"{type(enemy).__name__} {e_index} hit player with {enemy.status}")

        update_screen(surf, bg, player, enemies)

        disp.blit(surf, (0,0))
        pygame.display.update()


