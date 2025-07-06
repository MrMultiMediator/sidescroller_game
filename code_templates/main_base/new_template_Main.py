class Main_template:
    def gen_imports_to_used_keys(self):
        self.imports_to_used_keys = f'from background import Background\n'
        self.imports_to_used_keys += f'from player import Player\n'
        self.imports_to_used_keys += f'import pygame\n'
        self.imports_to_used_keys += f'import sys\n'
        self.imports_to_used_keys += f'\n'
        self.imports_to_used_keys += f'class Window:\n'
        self.imports_to_used_keys += f'    def __init__(self, width, height):\n'
        self.imports_to_used_keys += f'        self.width = width\n'
        self.imports_to_used_keys += f'        self.height = height\n'
        self.imports_to_used_keys += f'\n'
        self.imports_to_used_keys += f'\n'
        self.imports_to_used_keys += f'def update_screen(surf, bg, player):\n'
        self.imports_to_used_keys += f'    surf.blit(bg.surf, (bg.x, 0))\n'
        self.imports_to_used_keys += f'    surf.blit(player.surf, (player.x, player.y))\n'
        self.imports_to_used_keys += f'    surf.blit(player.health_bar.surf, (player.health_bar.x, player.health_bar.y))\n'
        self.imports_to_used_keys += f'\n'
        self.imports_to_used_keys += f'gravity = 5 # gravitational acceleration\n'
        self.imports_to_used_keys += f'\n'
        self.imports_to_used_keys += f'used_keys = [\n'
        self.imports_to_used_keys += f'    pygame.K_a,\n'
        self.imports_to_used_keys += f'    pygame.K_d,\n'
        self.imports_to_used_keys += f'    pygame.K_j,\n'
        self.imports_to_used_keys += f'    pygame.K_k,\n'
        self.imports_to_used_keys += f'    pygame.K_l,\n'
        self.imports_to_used_keys += f'    pygame.K_RSHIFT,\n'
        self.imports_to_used_keys += f'    pygame.K_LSHIFT,\n'
        self.imports_to_used_keys += f'    pygame.K_RCTRL,\n'
        self.imports_to_used_keys += f'    pygame.K_LCTRL,\n'
        self.imports_to_used_keys += f'    pygame.K_SPACE\n'
        self.imports_to_used_keys += f']\n'
        self.imports_to_used_keys += f'\n'
        self.imports_to_used_keys += '\n'

    def gen_init_func(self, player_xvel=40, win_width=1920, win_height=1080):
        self.init_func = f"if __name__ == '__main__':\n"
        self.init_func += f'    pygame.init()\n'
        self.init_func += f'    clock = pygame.time.Clock()\n'
        self.init_func += f'    terminate_game_loop = False\n'
        self.init_func += f'\n'
        self.init_func += f'    window = Window({win_width}, {win_height})\n'
        self.init_func += f'\n'
        self.init_func += f'    disp = pygame.display.set_mode(((window.width,window.height)))\n'
        self.init_func += f'    surf = pygame.Surface((window.width,window.height))\n'
        self.init_func += f'    bg = Background("img/background.png")\n'
        self.init_func += f'\n'
        self.init_func += f'    xvel = {player_xvel}\n'
        self.init_func += f'    player = Player(window.width, window.height, bg.info, gravity, xvel=xvel)\n'
        self.init_func += f'\n'
        self.init_func += f'\n'
        self.init_func += '\n'

    def gen_event_controller(self):
        self.event_controller = f'    while not terminate_game_loop:\n'
        self.event_controller += f'        clock.tick(30)\n'
        self.event_controller += f'\n'
        self.event_controller += f'        for e in pygame.event.get():\n'
        self.event_controller += f'            if e.type == pygame.QUIT:\n'
        self.event_controller += f'                terminate_game_loop = True\n'
        self.event_controller += f'                break\n'
        self.event_controller += f'\n'
        self.event_controller += f'            if player.status == "fall1":\n'
        self.event_controller += f'                continue\n'
        self.event_controller += f'\n'
        self.event_controller += f'            if e.type == pygame.KEYDOWN and e.key in used_keys:\n'
        self.event_controller += f'                player.frame = 1\n'
        self.event_controller += f'                if e.key == pygame.K_a:\n'
        self.event_controller += f'                    if "left" not in player.keys_down:\n'
        self.event_controller += f"                        player.keys_down.append('left')\n"
        self.event_controller += f'\n'
        self.event_controller += f'                elif e.key == pygame.K_d:\n'
        self.event_controller += f'                    if "right" not in player.keys_down:\n'
        self.event_controller += f"                        player.keys_down.append('right')\n"
        self.event_controller += f'\n'
        self.event_controller += f'                elif e.key == pygame.K_RSHIFT or e.key == pygame.K_LSHIFT:\n'
        self.event_controller += f"                    if 'shift' not in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.append('shift')\n"
        self.event_controller += f'\n'
        self.event_controller += f'                elif e.key == pygame.K_RCTRL or e.key == pygame.K_LCTRL:\n'
        self.event_controller += f"                    if 'ctrl' not in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.append('ctrl')\n"
        self.event_controller += f'\n'
        self.event_controller += f'                elif e.key == pygame.K_j:\n'
        self.event_controller += f"                    if 'j' not in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.append('j')\n"
        self.event_controller += f'\n'
        self.event_controller += f'                elif e.key == pygame.K_k:\n'
        self.event_controller += f"                    if 'k' not in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.append('k')\n"
        self.event_controller += f'\n'
        self.event_controller += f'                elif e.key == pygame.K_l:\n'
        self.event_controller += f"                    if 'l' not in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.append('l')\n"
        self.event_controller += f'\n'
        self.event_controller += f'            if e.type == pygame.KEYUP and e.key in used_keys:\n'
        self.event_controller += f'                player.frame = 1\n'
        self.event_controller += f'                if e.key == pygame.K_a:\n'
        self.event_controller += f"                    player.keys_down.remove('left')\n"
        self.event_controller += f'                elif e.key == pygame.K_d:\n'
        self.event_controller += f"                    player.keys_down.remove('right')\n"
        self.event_controller += f'                elif e.key == pygame.K_RSHIFT or e.key == pygame.K_LSHIFT:\n'
        self.event_controller += f"                    if 'shift' in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.remove('shift')\n"
        self.event_controller += f'                elif e.key == pygame.K_RCTRL or e.key == pygame.K_LCTRL:\n'
        self.event_controller += f"                    if 'ctrl' in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.remove('ctrl')\n"
        self.event_controller += f'                elif e.key == pygame.K_j:\n'
        self.event_controller += f"                    if 'j' in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.remove('j')\n"
        self.event_controller += f'\n'
        self.event_controller += f"                        if 'ctrl' in player.keys_down:\n"
        self.event_controller += f'                            player.frame = 6\n'
        self.event_controller += f'                            player.status = "kneel"\n'
        self.event_controller += f'\n'
        self.event_controller += f'                elif e.key == pygame.K_k:\n'
        self.event_controller += f"                    if 'k' in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.remove('k')\n"
        self.event_controller += f'                elif e.key == pygame.K_l:\n'
        self.event_controller += f"                    if 'l' in player.keys_down:\n"
        self.event_controller += f"                        player.keys_down.remove('l')\n"
        self.event_controller += f'                elif e.key == pygame.K_SPACE:\n'
        self.event_controller += f'                    if player.status != "jump":\n'
        self.event_controller += f'                        player.status = "jump"\n'
        self.event_controller += f'                        player.y_vel = player.jump_strength\n'
        self.event_controller += f'\n'
        self.event_controller += f'\n'
        self.event_controller += '\n'

    def gen_final_updates(self):
        self.final_updates = f'        surf.fill((0,0,200))\n'
        self.final_updates += f'        #surf.blit(bg.surf, (bg.x,0))\n'
        self.final_updates += f'\n'
        self.final_updates += f'        delta = player.update(bg)\n'
        self.final_updates += f'        bg.update(surf, delta)\n'
        self.final_updates += f'        update_screen(surf, bg, player)\n'
        self.final_updates += f'\n'
        self.final_updates += f'        disp.blit(surf, (0,0))\n'
        self.final_updates += f'        pygame.display.update()\n'
        self.final_updates += f'\n'
        self.final_updates += f'\n'
        self.final_updates += '\n'

    def write_class_to_file(self, filename="main.py", win_width=1920, win_height=1080):
        self.gen_imports_to_used_keys()
        self.gen_init_func(win_width=win_width, win_height=win_height)
        self.gen_event_controller()
        self.gen_final_updates()

        with open(filename, "w") as g:
            g.write(self.imports_to_used_keys)
            g.write(self.init_func)
            g.write(self.event_controller)
            g.write(self.final_updates)
