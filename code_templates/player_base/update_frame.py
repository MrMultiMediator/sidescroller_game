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

