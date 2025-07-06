    def build_surf(self, filename):
        im_surf = pygame.image.load(filename).convert_alpha()
        self.surf = pygame.Surface((3*im_surf.get_width(), im_surf.get_height()))

        for i in range(self.n_imgs):
            # TODO Generalize for the case where we have other background
            # images and not the same repeated image.
            self.surf.blit(im_surf, (self.x+i*im_surf.get_width(), 0))

        self.im_dims = {'w':im_surf.get_width(), 'h':im_surf.get_height()}

