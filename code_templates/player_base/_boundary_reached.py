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

