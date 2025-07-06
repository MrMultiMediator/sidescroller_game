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

