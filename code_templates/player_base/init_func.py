class Player(Sprite):
    def __init__(self, window_width, window_height, bg_info, gravity, xvel=25):
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
        self.frame = 1
        self.time = 0
        self.direction = 'right'
        self.status = 'idle'
        self.bg_info = bg_info
        self.bg_edge = True # Specifies whether the character should move or the background should move
        self.imgdir = "img"
        self.imfile = f"{self.imgdir}/{self.status}_{self.frame}.png"
        self.surf = image.load(self.imfile).convert_alpha()
        self.keys_down = []
        self.load_images()

