from pygame import image, Surface
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
    """
    def __init__(
        self,
        x,
        gravity,
        my_dir,
        bg_info,
        y=None,
        xvel=50,
        move: str = "null",
        max_hp=1000.,
        max_shield=1000.
    ):
        with open(__file__.replace(os.path.basename(__file__), "")+f"../{my_dir}/topology.json") as f:
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
        self.max_shield = max_shield
        self.shield = self.max_shield
        self.x_vel = xvel
        self.frame = 1
        self.time = 0
        self.state = "idle"
        self.status = "idle"
        self.move = move
        self.bg_info = bg_info
        self.my_dir = my_dir
        self.imfile = f"{self.my_dir}/{self.status}_{self.frame}.png"
        self.surf = image.load(self.imfile).convert_alpha()
        self.load_images()

    def update(self, window_xvel):
        """Everything that is not the main character (everything of this base class)
        needs to move relative to the main character. This update function needs to be
        informed by how fast the window is moving since the character is always in the
        center of the frame, and they need to be shifted over by that. This is the
        variable 'delta' returned by Player.update, i.e. this value is accessible after
        the player updates."""
        self.time += 1
        self.x += window_xvel

        if self.time > 10000000:
            self.time = 0

    def decide(self):
        "Decision to change one's status"
        pass

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