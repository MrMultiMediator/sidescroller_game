class Main_template:
    def gen_imports_and_Window(self):
        self.imports_window_code = f"from background import Background\n"
        self.imports_window_code += f"from player import Player\n"
        self.imports_window_code += f"import pygame\n"
        self.imports_window_code += f"import sys\n"
        self.imports_window_code += f"\n"
        self.imports_window_code += f"class Window:\n"
        self.imports_window_code += f"    def __init__(self, width, height):\n"
        self.imports_window_code += f"        self.width = width\n"
        self.imports_window_code += f"        self.height = height\n"
        self.imports_window_code += "\n\n"

    def gen_update_screen_func(self):
        self.update_screen_func = f"def update_screen(surf, bg, player):\n"
        self.update_screen_func += f"    surf.blit(bg.surf, (bg.x, 0))\n"
        self.update_screen_func += f"    surf.blit(player.surf, (player.x, player.y))\n"
        self.update_screen_func += "\n\n"

    def gen_init_func(self, player_xvel=40, win_width=1920, win_height=1080):
        self.main_init_func = f"if __name__ == '__main__':\n"
        self.main_init_func += f"    pygame.init()\n"
        self.main_init_func += f"    clock = pygame.time.Clock()\n"
        self.main_init_func += f"    terminate_game_loop = False\n"
        self.main_init_func += f"\n"
        self.main_init_func += f"    window = Window({win_width}, {win_height})\n"
        self.main_init_func += f"\n"
        self.main_init_func += (
            f"    disp = pygame.display.set_mode(((window.width,window.height)))\n"
        )
        self.main_init_func += (
            f"    surf = pygame.Surface((window.width,window.height))\n"
        )
        self.main_init_func += f'    bg = Background("img/background.png")\n'
        self.main_init_func += f"\n"
        self.main_init_func += f"    xvel = {player_xvel}\n"
        self.main_init_func += (
            f"    player = Player(window.width, bg.info, xvel=xvel)\n"
        )
        self.main_init_func += "\n\n"

    def gen_event_controller(self):
        """This could potentially be customized by the user (which keys do what).
        I'd just have to pass in arguments here and put them in the f-strings below"""
        self.event_controller = f"    while not terminate_game_loop:\n"
        self.event_controller += f"        clock.tick(30)\n"
        self.event_controller += f"\n"
        self.event_controller += f"        for e in pygame.event.get():\n"
        self.event_controller += f"            if e.type == pygame.QUIT:\n"
        self.event_controller += f"                terminate_game_loop = True\n"
        self.event_controller += f"                break\n"
        self.event_controller += f"\n"
        self.event_controller += f"            if e.type == pygame.KEYDOWN:\n"
        self.event_controller += f"                player.frame = 1\n"
        self.event_controller += f"                if e.key == pygame.K_a:\n"
        self.event_controller += (
            f"                    player.keys_down.append('left')\n"
        )
        self.event_controller += f"\n"
        self.event_controller += f"                elif e.key == pygame.K_d:\n"
        self.event_controller += (
            f"                    player.keys_down.append('right')\n"
        )
        self.event_controller += f"\n"
        self.event_controller += f"                elif e.key == pygame.K_RSHIFT or e.key == pygame.K_LSHIFT:\n"
        self.event_controller += (
            f"                    if 'shift' not in player.keys_down:\n"
        )
        self.event_controller += (
            f"                        player.keys_down.append('shift')\n"
        )
        self.event_controller += f"\n"
        self.event_controller += f"                elif e.key == pygame.K_RCTRL or e.key == pygame.K_LCTRL:\n"
        self.event_controller += (
            f"                    if 'ctrl' not in player.keys_down:\n"
        )
        self.event_controller += (
            f"                        player.keys_down.append('ctrl')\n"
        )
        self.event_controller += f"\n"
        self.event_controller += f"            if e.type == pygame.KEYUP:\n"
        self.event_controller += f"                if e.key == pygame.K_a:\n"
        self.event_controller += (
            f"                    player.keys_down.remove('left')\n"
        )
        self.event_controller += f"                elif e.key == pygame.K_d:\n"
        self.event_controller += (
            f"                    player.keys_down.remove('right')\n"
        )
        self.event_controller += f"                elif e.key == pygame.K_RSHIFT or e.key == pygame.K_LSHIFT:\n"
        self.event_controller += (
            f"                    if 'shift' in player.keys_down:\n"
        )
        self.event_controller += (
            f"                        player.keys_down.remove('shift')\n"
        )
        self.event_controller += f"                elif e.key == pygame.K_RCTRL or e.key == pygame.K_LCTRL:\n"
        self.event_controller += f"                    if 'ctrl' in player.keys_down:\n"
        self.event_controller += (
            f"                        player.keys_down.remove('ctrl')\n"
        )
        self.event_controller += "\n\n"

    def gen_final_updates(self):
        self.final_updates = f"        surf.fill((0,0,200))\n"
        self.final_updates += f"        #surf.blit(bg.surf, (bg.x,0))\n"
        self.final_updates += f"\n"
        self.final_updates += f"        delta = player.update(surf, bg)\n"
        self.final_updates += f"        bg.update(surf, delta)\n"
        self.final_updates += f"        update_screen(surf, bg, player)\n"
        self.final_updates += f"\n"
        self.final_updates += f"        disp.blit(surf, (0,0))\n"
        self.final_updates += f"        pygame.display.update()\n"
        self.final_updates += "\n\n"

    def write_class_to_file(self, filename="main.py", win_width=1920, win_height=1080):
        self.gen_imports_and_Window()
        self.gen_update_screen_func()
        self.gen_init_func(win_width=win_width, win_height=win_height)
        self.gen_event_controller() 
        self.gen_final_updates()

        with open(filename, "w") as g:
            g.write(self.imports_window_code)
            g.write(self.update_screen_func)
            g.write(self.main_init_func)
            g.write(self.event_controller)
            g.write(self.final_updates)
