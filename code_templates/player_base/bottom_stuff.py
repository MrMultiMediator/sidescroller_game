    def adjust_y_to_bottom(self):
        """If the current status specifies that the y-position of the character needs 
        to change due to a changing bottom location then adjust according to the 
        specifications of the character status"""
        if str(self.status) in self.topology["bottom"].keys():
            try:
                self.y = self.bg_info['floor']-self.topology['bottom'][str(self.status)]['values'][self.frame-1]
            except Exception as e:
                pass
        elif str(self.status) != "jump":
            self.y = self.bg_info['floor']-self.topology['bottom']['global']

    def bottom_terminate(self):
        """Terminate an animation, like a jump for example, if the bottom of the
        character reaches the ground at whatever frame they're in."""
        if str(self.status) in self.topology["bottom_terminate"].keys():
            if self.y + self.topology['bottom_terminate'][str(self.status)]['values'][self.frame-1] >= self.bg_info['floor']:
                self.status = "idle"
                self.frame = 1
                self.y = self.still_coords['y']

