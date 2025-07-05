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


