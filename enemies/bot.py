from pygame import image, Surface
from pygame.transform import flip
from random import random
from pprint import pprint
from uuid import uuid4
import json
import os

class Bot:
    """Collision rules:
    Character state | Enemy state | Character effect | Enemy effect
    ----------------|-------------|------------------|-------------
     Neutral        |  Neutral    |    Nothing       |   Nothing
     Attacking      |  Neutral    |    Nothing       | Health loss
     Attacking      |  Attacking  |  Health loss     | Health loss
     Neutral        |  Attacking  |  Health loss     |   Nothing
     Shielding      |  Attacking  |  Shield2 loss    | Health loss

    Nothing = Shield recovery. All shields recover over a period of time for both the
    character and the enemies, both shield and shield2. Shield2 is the active shield
    that only the player has. Shield is something that everyone has by default.

    Introduce Attack States with Different Properties
    Light Attack: Faster, less damage, perhaps safer.
    Heavy Attack: Slower, more damage, potentially leaves the player more vulnerable
      during its wind-up or recovery.
    Special Attacks: Unique effects, perhaps requiring resources or cooldowns.

    critical_*: The probability of changing state from retreat to attack increases as
    the shield and health approach these thresholds. Below these, the probability goes
    to a high 95% and stays there.
    happy_shield: The probability of changing state from retreat to attack goes up as
    the shield goes up toward this threshold.
    """
    def __init__(
        self,
        x,
        gravity,
        my_dir,
        bg_info,
        name=None,
        y=None,
        xvel=50,
        direction: str = "null",
        max_hp=1000.,
        max_shield=1000.,
        critical_health=0.4,
        critical_shield=0.2,
        happy_shield=0.65
    ):
        if name == None:
            self.name = str(uuid4())

        with open(__file__.replace(os.path.basename(__file__), "")+f"../{my_dir}_topology.json") as f:
            self.topology = json.load(f)
        try:
            self.still_coords = {'y': bg_info['floor']-self.topology['bottom']['global']}
        except KeyError:
            self.still_coords = {'y':200}
        self.x = x
        if y is None:
            self.y = self.still_coords['y']
        else:
            self.y = y
        self.gravity = gravity

        self.max_hp = max_hp
        self.hp = self.max_hp
        self.critical_health = critical_health
        self.max_shield = max_shield
        self.shield = self.max_shield
        self.critical_shield = critical_shield
        self.happy_shield = happy_shield

        self.x_vel = xvel
        self.frame = 1
        self.time = 0
        self.state = "attack"
        self.status = "idle"
        self.previous = "idle"
        self.direction = direction
        self.bg_info = bg_info
        self.my_dir = my_dir
        self.imfile = f"{self.my_dir}/{self.status}_{self.frame}.png"
        self.surf = image.load(self.imfile).convert_alpha()
        self.load_images()

        if "atk_surf" in self.topology.keys():
            self.prune_atk_surf(verbosity="high")
            self.compute_striking_distances()

    def exclusion_msg(self, status, target_anim, frame, direction):
        msg = f"Omitting enemy attack {status} facing {direction} against player "
        msg += f"{target_anim} frame {frame} from striking distance computation due to"
        msg += " exclusion specifier."

        return msg

    def prune_atk_surf(self, verbosity="low"):
        """Remove from the dict, attack distances where there is no numerical value,
        and instead an 'exclude' string due to issues with the automated computation.
        """
        for status in self.topology["atk_surf"].keys():
            for target_anim in self.topology["atk_surf"][status]["values"].keys():
                for frame in self.topology["atk_surf"][status]["values"][target_anim].keys():
                    r_atk_dist = self.topology["atk_surf"][status]["values"][target_anim][frame]["right"]
                    l_atk_dist = self.topology["atk_surf"][status]["values"][target_anim][frame]["left"]

                    if isinstance(r_atk_dist, str):
                        if verbosity == "high":
                            print(self.exclusion_msg(status, target_anim, frame, "right"))
                        del self.topology["atk_surf"][status]["values"][target_anim][frame]["right"]

                    if isinstance(l_atk_dist, str):
                        if verbosity == "high":
                            print(self.exclusion_msg(status, target_anim, frame, "left"))
                        del self.topology["atk_surf"][status]["values"][target_anim][frame]["left"]

    def compute_striking_distances(self, verbosity="high"):
        """Exclude from the calculation, attack distances where there is no numerical 
        value, and instead an 'exclude' string due to issues with the automated 
        computation, and where the key-value pair was previously deleted from the 
        topology in the call to self.prune_atk_surf()"""
        self.l_dist = {}
        self.r_dist = {}
        total_weight = {} # Should sum to 1. Now it won't because of the sketchy way of excluding certain frames.

        for status in self.topology["atk_surf"].keys():
            self.l_dist[status] = 0.
            self.r_dist[status] = 0.
            total_weight[status] = 0.

            # Initially, each player status/animation is weighted the same
            weight_per_animation = 1./float(len(self.topology["atk_surf"][status]["values"].keys()))

            for target_anim in self.topology["atk_surf"][status]["values"].keys():
                weight_per_frame = 1./float(len(self.topology["atk_surf"][status]["values"][target_anim].keys()))
                for frame in self.topology["atk_surf"][status]["values"][target_anim].keys():
                    try:
                        self.r_dist[status] += weight_per_animation*weight_per_frame*self.topology["atk_surf"][status]["values"][target_anim][frame]["right"]
                        self.l_dist[status] += weight_per_animation*weight_per_frame*self.topology["atk_surf"][status]["values"][target_anim][frame]["left"]
                    except KeyError:
                        continue

                    total_weight[status] += weight_per_animation*weight_per_frame

        if verbosity == "high":
            print(f"Right striking distance computed as {self.r_dist}")
            print(f"Left striking distance computed as {self.l_dist}")
            print(f"Total weight computed as {total_weight}")

    def update(self, window_xvel):
        """Everything that is not the main character (everything of this base class)
        needs to move relative to the main character. This update function needs to be
        informed by how fast the window is moving since the character is always in the
        center of the frame, and they need to be shifted over by that. This is the
        variable 'delta' returned by Player.update, i.e. this value is accessible after
        the player updates."""
        self.x += window_xvel

        self.time += 1

        if self.time > 10000000:
            self.time = 0

    def post_update(self):
        self.animate()

        #if self.status != "fall1":
        #    self.update_health()

        if self.previous != str(self.status):
            pass
            # self.apply_left_correction()

        self.previous = str(self.status)

    def update_frame(self):
        if str(self.status) not in self.topology["stop"].keys() and str(self.status) != "jump":
            self.frame += 1

            if self.frame > len(self.surfaces[str(self.status)]):
                # print('setting frame to 1')
                self.frame = 1
                # self.status = "idle"

        elif str(self.status) == "jump":
            self.jump_frame_control()

        else:
            # Special code for animations that specify the animation to stop at the end rather than looping.
            # Increase frame until we reach the end
            if self.topology["stop"][str(self.status)] == "end" and self.frame < len(self.surfaces[str(self.status)]):
                self.frame += 1

            if self.topology["stop"][str(self.status)] == "beginning":
                self.frame += 1
                if self.frame == len(self.surfaces[str(self.status)]):
                    #print('setting frame to 1 adlfkjds')
                    self.frame = 1
                    #self.status.status = "done"
                    self.status = "idle"
                #elif self.status.status == "running":
                #    self.frame += 1

        #print(f"Frame is {self.frame} : {str(self.status)} : {self.keys_down}")


    def animate(self):
        self.update_frame()
        self.surf = self.surfaces[str(self.status)][self.frame-1]
        if self.direction == "left":
            self.surf = flip(self.surf, True, False)

    def decide(self):
        "Decision to change one's state"
        if self.state == "attack":
            if random() <= self.p_a_r():
                self.state = "retreat"
                return

        if self.state == "retreat":
            if random() <= self.p_r_a():
                self.state = "attack"

    def p_a_r(self) -> float:
        """Return the probability of changing from attack to retreat state.
        Default equation: P(H) = ((A-H)/B)**2
        P is the probability of changing from attack to retreat.
        H is the shield.
        A is the max shield
        A-B is the critical shield
        B is the max shield minus critical shield"""
        if self.hp > self.critical_health*self.max_hp:
            return 0.

        H = self.shield
        A = self.max_shield
        B = A - self.critical_shield*self.max_shield
        
        if H < self.critical_shield:
            return 0.95

        return 0.95*(((A-H)/B)**2.)

    def p_r_a(self) -> float:
        """Return the probability of changing from retreat to attack state.
        Default equation: P(H) = (H/(A-C))**2
        H is the shield
        A is the max shield
        A-C is the happy sheild
        C is the max shield minus happy shield"""
        H = self.shield
        A = self.max_shield
        C = A - self.happy_shield

        if H > self.happy_shield:
            return 0.95

        return 0.95*((H/(A-C))**2.)

    def load_images(self, ext="png"):
        "Loaded once upon __init__"
        img_json = f"{self.my_dir}/img_js.json"
        self.surfaces = {}
        self.status_fname = {} # Dictionary associating statuses with filenames

        with open(img_json, 'r') as f:
            img_js = json.load(f)

        for animation in img_js.keys():
            self.surfaces[animation] = []

            self.status_fname[animation] = img_js[animation]["filename"]

            for frame in range(img_js[animation]["frames"][0], img_js[animation]["frames"][1]+1):
                filename = f"{self.my_dir}/{self.status_fname[animation]}_{frame}.{ext}"
                self.surfaces[animation].append(image.load(filename).convert_alpha())


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


    def adjust_y_to_bottom(self):
        """If the current status specifies that the y-position of the character needs
        to change due to a changing bottom location then adjust according to the
        specifications of the character status"""
        if str(self.status) in self.topology["bottom"].keys():
            try:
                self.y = self.bg_info['floor']-self.topology['bottom'][str(self.status)]['values'][self.frame-1]
            except Exception as e:
                pass