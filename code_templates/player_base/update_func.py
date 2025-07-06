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

        return delta

