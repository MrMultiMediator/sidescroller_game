        surf.fill((0,0,200))
        #surf.blit(bg.surf, (bg.x,0))

        delta = player.update(bg)
        bg.update(surf, delta)
        update_screen(surf, bg, player)

        disp.blit(surf, (0,0))
        pygame.display.update()


