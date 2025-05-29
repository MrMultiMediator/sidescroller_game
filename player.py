from pygame.sprite import Sprite
from pygame.transform import flip
from pygame import image
import json
import os

class Player(Sprite):
    def __init__(self, window_width, bg_info, xvel=25):
        with open(__file__.replace(os.path.basename(__file__), "")+"/img/topology.json") as f:
            self.topology = json.load(f)
        self.window_width = window_width
        try:
            self.still_coords = {'x':bg_info['sf_x']*800, 'y': bg_info['floor']-self.topology['bottom']['global']}
        except KeyError:
            self.still_coords = {'x':800, 'y':200}
        self.x = self.still_coords['x']
        self.y = self.still_coords['y']
        self.x_vel = xvel
        self.frame = 1
        self.direction = 'right'
        self.status = 'idle'
        self.bg_info = bg_info
        self.bg_edge = True # Specifies whether the character should move or the background should move
        self.imgdir = "img"
        self.imfile = f"{self.imgdir}/{self.status}_{self.frame}.png"
        self.surf = image.load(self.imfile).convert_alpha()
        self.keys_down = []
        self.load_images()
        print(self.surfaces)

    def update(self, disp, bg):
        # delta is how much all the objects should shift to keep the frame of
        # reference w/ the player at the center. If delta remains at zero,
        # that means the player has reached the end of the map and must move.
        delta = 0

        #disp.blit(self.surf, self.surf.get_rect())
        #disp.blit(self.surf, (self.x, self.y))

        # Move right
        if "right" in self.keys_down:
            if "left" not in self.keys_down:
                self.direction = "right"
                self.walk_run_setup()

                # If we've right scrolled to the end of the background, stop
                # scrolling the background and start moving the player
                if bg.reached_left_end or bg.reached_right_end:
                    if not self._boundary_reached('right'):
                        self.x += self.x_vel

                    # If we've gotten back to the center, go back to scrolling the background
                    if bg.reached_right_end and self.x >= self.still_coords['x']:
                        diff = self.still_coords['x'] - self.x
                        self.x += diff
                        bg.x += diff

                        bg.reached_right_end = False
                else:
                    delta = -self.x_vel
            else:
                self.status = "idle"

        # Move left
        elif "left" in self.keys_down:
            if "right" not in self.keys_down:
                self.direction = "left"
                self.walk_run_setup()

                # If we've left scrolled to the end of the background, stop
                # scrolling the background and start moving the player
                if bg.reached_left_end or bg.reached_right_end:
                    if not self._boundary_reached('left'):
                        self.x -= self.x_vel

                    # If we've gotten back to the center, go back to scrolling the background
                    if bg.reached_left_end and self.x <= self.still_coords['x']:
                        diff = self.still_coords['x'] - self.x
                        self.x += diff
                        bg.x += diff

                        bg.reached_left_end = False
                else:
                    delta = self.x_vel
            else:
                self.status = "idle"

        # Kneel
        elif "ctrl" in self.keys_down:
            self.status = "kneel"

        if len(self.keys_down) == 0:
            self.status = "idle"

        self.adjust_y_to_bottom()

        self.animate()

        return delta

    def walk_run_setup(self):
        if "shift" in self.keys_down:
            self.status = "run"
            self.x_vel = 40
        else:
            self.status = "walk"
            self.x_vel = 25

    def _boundary_reached(self, direction):
        if direction.lower() == 'left':
            if self.x - self.x_vel < 0:
                return True
            else:
                return False

        elif direction.lower() == 'right':
            if self.x + self.surf.get_width() + self.x_vel > self.window_width:
                return True
            else:
                return False

        else:
            raise ValueError("direction argument must be left or right")
    def update_frame(self):
        if self.status not in self.topology["stop"].keys():
            self.frame += 1
        else:
            # Special code for animations that specify the animation to stop at the end rather than looping.
            # Increase frame until we reach the end
            if self.topology["stop"][self.status] == "end" and self.frame < len(self.surfaces[self.status]):
                self.frame += 1

        if self.frame > len(self.surfaces[self.status]):
            self.frame = 1

        #print(f"Frame is {self.frame} : {self.status} : {self.keys_down}")

    def animate(self):
        self.update_frame()

        self.surf = self.surfaces[self.status][self.frame-1]
        if self.direction == "left":
            self.surf = flip(self.surf, True, False)

    def load_images(self, img_json="img_js.json", ext="png"):
        "Loaded once upon __init__"
        self.surfaces = {}
        self.status_fname = {} # Dictionary associating statuses with filenames

        with open(img_json, 'r') as f:
            img_js = json.load(f)

        for animation in img_js.keys():
            self.surfaces[animation] = []

            self.status_fname[animation] = img_js[animation]["filename"]

            for frame in range(img_js[animation]["frames"][0], img_js[animation]["frames"][1]+1):
                filename = f"{self.imgdir}/{self.status_fname[animation]}_{frame}.{ext}"
                self.surfaces[animation].append(image.load(filename).convert_alpha())

    def adjust_y_to_bottom(self):
        """If the current status specifies that the y-position of the character needs 
        to change due to a changing bottom location then adjust according to the 
        specifications of the character status"""
        if self.status in self.topology["bottom"].keys():
            try:
                self.y = self.bg_info['floor']-self.topology['bottom'][self.status]['values'][self.frame-1]
            except:
                pass
        else:
            self.y = self.bg_info['floor']-self.topology['bottom']['global']
