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

