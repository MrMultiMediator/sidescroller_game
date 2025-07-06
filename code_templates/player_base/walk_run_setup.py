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

