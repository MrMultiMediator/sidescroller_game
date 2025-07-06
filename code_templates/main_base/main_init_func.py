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


