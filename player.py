from pygame.sprite import Sprite
from pygame.transform import flip
from pygame import image, Surface
import pygame
import json
import os

class Action:
    def __init__(self, name, status="running"):
        self.name = name
        self.status = status

    def __repr__(self):
        return self.name


class HealthBar:
    def __init__(self, bg_w, bg_h, max_hp, max_shield):
        "Make the dimensions and placement of the healthbar proportional to the size of the game background"
        self.max_hp = max_hp
        self.max_shield = max_shield
        self.x = bg_w*0.85
        self.y = bg_h*0.05
        self.w = bg_w*0.1
        self.h = bg_h*0.015

        self.surf = Surface((int(self.w), int(self.h)))

    def draw(self, hp, shield):
        ratio = hp / self.max_hp
        ratio_shield = shield / self.max_shield

        pygame.draw.rect(self.surf, "red", (0., 0., self.w, self.h))
        pygame.draw.rect(self.surf, "green", (0., 0., self.w*ratio, self.h))
        pygame.draw.rect(self.surf, "blue", (0., 0., self.w*ratio_shield, self.h))


class Player(Sprite):
    """
    If shield2 goes to zero, the player will be stunned and vulnerable to attack temporarily.
    
    Perfect Guard/Parry: A very brief, well-timed shield could negate all damage,
    perhaps even stun the enemy or open them up for a counterattack. This adds a
    high-skill, high-reward mechanic.
    """
    def __init__(self, window_width, window_height, bg_info, gravity, xvel=25):
        self.imgdir = "img/player"
        with open(__file__.replace(os.path.basename(__file__), "")+"/img/topology.json") as f:
            self.topology = json.load(f)
        self.window_width = window_width
        try:
            self.still_coords = {'x':bg_info['sf_x']*800, 'y': bg_info['floor']-self.topology['bottom']['global']}
        except KeyError:
            self.still_coords = {'x':800, 'y':200}
        self.x = self.still_coords['x']
        self.y = self.still_coords['y']
        self.gravity = gravity
        self.jump_strength = 60
        self.max_hp = 1000.
        self.hp = self.max_hp
        self.max_shield = 1000.
        self.shield = self.max_shield
        self.health_bar = HealthBar(window_width, window_height, self.max_hp, self.max_shield)
        self.x_vel = xvel
        self.y_vel = 0.
        self.shift = 0.
        self.frame = 1
        self.time = 0
        self.direction = 'right'
        self.status = 'idle'
        self.previous = 'idle'
        self.bg_info = bg_info
        self.bg_edge = True # Specifies whether the character should move or the background should move
        self.imfile = f"{self.imgdir}/{self.status}_{self.frame}.png"
        self.surf = image.load(self.imfile).convert_alpha()
        self.keys_down = []
        self.load_images()


    def update(self, bg):
        # delta is how much all the objects should shift to keep the frame of
        # reference w/ the player at the center. If delta remains at zero,
        # that means the player has reached the end of the map and must move.
        delta = 0

        self.time += 1

        #disp.blit(self.surf, self.surf.get_rect())
        #disp.blit(self.surf, (self.x, self.y))

        if "right" not in self.keys_down and "left" not in self.keys_down:
            self.x_vel = 0

        if self.status == "fall1":
            pass
        # Move right
        elif "right" in self.keys_down:
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
                if str(self.status) != "jump":
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
                if str(self.status) != "jump":
                    self.status = "idle"

        elif str(self.status) == "jump":
            self.y -= self.y_vel
            self.y_vel -= self.gravity

        # Kneel
        elif "ctrl" in self.keys_down and "j" not in self.keys_down and "k" not in self.keys_down:
            self.status = "kneel"
            self.take_damage(0.1*self.max_hp)

        elif "j" in self.keys_down:
            if "ctrl" not in self.keys_down and "shift" not in self.keys_down and str(self.status) != "jab1":
                self.status = Action("jab1")

            if "ctrl" not in self.keys_down and "shift" in self.keys_down and str(self.status) != "uppercut1":
                self.status = Action("uppercut1")

            if "ctrl" in self.keys_down and "shift" not in self.keys_down and str(self.status) != "kneel_punch1":
                self.status = Action("kneel_punch1")

        elif "k" in self.keys_down:
            if "ctrl" not in self.keys_down and str(self.status) != "kick1":
                self.status = Action("kick1")

        elif "l" in self.keys_down:
            self.status = "shoot1"

        elif "shift" in self.keys_down and len(self.keys_down) == 1:
            self.status = "idle"

        if len(self.keys_down) == 0 and self.status != "jump" and self.status != "fall1":
            self.status = "idle"

        self.adjust_y_to_bottom()

        self.bottom_terminate()

        self.animate()

        if self.status != "fall1":
            self.update_health()

        if self.previous != str(self.status):
            self.apply_left_correction()

        self.previous = str(self.status)

        return delta


    def walk_run_setup(self):
        if self.status == "jump":
            self.y -= self.y_vel
            self.y_vel -= self.gravity

            if "shift" in self.keys_down:
                self.x_vel = 40
            elif "ctrl" in self.keys_down:
                self.x_vel = 10
            else:
                self.x_vel = 25
        elif "shift" in self.keys_down:
            self.status = "run"
            self.x_vel = 40
        elif "ctrl" in self.keys_down:
            self.status = "kneel_walk"
            self.x_vel = 10
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
        if str(self.status) not in self.topology["stop"].keys() and str(self.status) != "jump":
            self.frame += 1

            if self.frame > len(self.surfaces[str(self.status)]):
                self.frame = 1

        elif str(self.status) == "jump":
            self.jump_frame_control()

        else:
            # Special code for animations that specify the animation to stop at the end rather than looping.
            # Increase frame until we reach the end
            if self.topology["stop"][str(self.status)] == "end" and self.frame < len(self.surfaces[str(self.status)]):
                self.frame += 1

            if self.topology["stop"][str(self.status)] == "beginning":
                if self.frame == len(self.surfaces[str(self.status)]):
                    self.frame = 1
                    self.status.status = "done"
                elif self.status.status == "running":
                    self.frame += 1

        #print(f"Frame is {self.frame} : {str(self.status)} : {self.keys_down}")


    def animate(self):
        self.update_frame()
        self.surf = self.surfaces[str(self.status)][self.frame-1]
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


    def update_health(self):
        # Every 1/10th of a second, recharge shields by 2%
        if self.time % 3 == 0:
            if self.shield < self.max_shield:
                self.shield += self.max_shield*0.02

            if self.shield > self.max_shield:
                self.shield = self.max_shield

        self.health_bar.draw(self.hp, self.shield)

    def take_damage(self, amount):
        if self.shield > 0:
            if self.shield >= amount:
                self.shield -= amount
            else:
                amount -= self.shield
                self.shield = 0
                self.hp -= amount
        else:
            self.hp -= amount

        if self.hp <= 0:
            self.hp = 0
            self.status = "fall1"


    def adjust_y_to_bottom(self):
        """If the current status specifies that the y-position of the character needs
        to change due to a changing bottom location then adjust according to the
        specifications of the character status"""
        if str(self.status) in self.topology["bottom"].keys():
            try:
                self.y = self.bg_info['floor']-self.topology['bottom'][str(self.status)]['values'][self.frame-1]
            except Exception as e:
                pass
        elif str(self.status) != "jump":
            self.y = self.bg_info['floor']-self.topology['bottom']['global']

    def bottom_terminate(self):
        """Terminate an animation, like a jump for example, if the bottom of the
        character reaches the ground at whatever frame they're in."""
        if str(self.status) in self.topology["bottom_terminate"].keys():
            if self.y + self.topology['bottom_terminate'][str(self.status)]['values'][self.frame-1] >= self.bg_info['floor']:
                self.status = "idle"
                self.frame = 1
                self.y = self.still_coords['y']


    def jump_frame_control(self):
        """For jump animation, control how the animation is displayed"""
        if self.y_vel >= 0:
            if self.frame < len(self.surfaces[str(self.status)]):
                self.frame += 1
        else:
            if self.frame > 1:
                self.frame -= 1

    def apply_left_correction(self):
        self.still_coords['x'] -= self.shift
        self.x -= self.shift
        
        if self.direction == "right":
            self.shift = 0
        if self.direction == "left":
            if str(self.status) in self.topology["left_correction"].keys():
                curr = self.topology["left_correction"][str(self.status)]
                idle = self.topology["left_correction"]["idle"]
        
                if idle - curr < 0:
                    self.shift = idle - curr
                else:
                    self.shift = 0
            else:
                self.shift = 0

        self.still_coords['x'] += self.shift
        self.x += self.shift

