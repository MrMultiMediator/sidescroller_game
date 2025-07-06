    def jump_frame_control(self):
        """For jump animation, control how the animation is displayed"""
        if self.y_vel >= 0:
            if self.frame < len(self.surfaces[str(self.status)]):
                self.frame += 1
        else:
            if self.frame > 1:
                self.frame -= 1
