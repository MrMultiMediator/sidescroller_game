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

