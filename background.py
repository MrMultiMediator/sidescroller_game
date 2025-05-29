import pygame
import json
import os

class Background:
    def __init__(self, filename):
        self.x = 0
        self.repeat = 0
        self.min_repeat = -2
        self.max_repeat = 1
        self.reached_left_end = False
        self.reached_right_end = False
        self.n_imgs = 3 # The number of contiguous bacground images to hold in memory and display


        self.build_surf(filename)

        with open(__file__.replace(os.path.basename(__file__), "")+"/img/bg.json") as f:
            self.info = json.load(f)

    def build_surf(self, filename):
        im_surf = pygame.image.load(filename).convert_alpha()
        self.surf = pygame.Surface((3*im_surf.get_width(), im_surf.get_height()))

        for i in range(self.n_imgs):
            # TODO Generalize for the case where we have other background
            # images and not the same repeated image.
            self.surf.blit(im_surf, (self.x+i*im_surf.get_width(), 0))

        self.im_dims = {'w':im_surf.get_width(), 'h':im_surf.get_height()}

    def update(self, surf, delta):
        self.x += delta

        if self.x > 0:
            if self.repeat > self.min_repeat:
                # TODO Generalize for the case where we have other background
                # images and not the same image repeating. I.e. just shifting
                # the background is acceptable here, but if we have other
                # images, we may need to actually load the next one.
                self.x -= self.im_dims['w']
                self.repeat -= 1
                print(f"repeat = {self.repeat}")
            else:
                self.reached_right_end = True
        if self.x < -1*self.im_dims['w']:
            if self.repeat < self.max_repeat:
                # TODO Generalize for the case where we have other background
                # images and not the same image repeating.
                self.x += self.im_dims['w']
                self.repeat += 1
                print(f"repeat = {self.repeat}")
            else:
                self.reached_left_end = True

        #surf.blit(self.surf, (self.x, 0))
        #if self.x < 0:
        #    pass

