    def update(self, surf, delta):
        self.x += delta

        if self.x > 0:
            if self.repeat > self.min_repeat:
                # TODO Generalize for the case where we have other background
                # images and not the same image repeating. I.e. just shifting
                # the background is acceptable here, but if we have other
                # images, we may need to actually load the next one.
                self.x -= self.im_dims['w']
                self.repeat -= 1
                print(f"repeat = {self.repeat}")
            else:
                self.reached_right_end = True
        if self.x < -1*self.im_dims['w']:
            if self.repeat < self.max_repeat:
                # TODO Generalize for the case where we have other background
                # images and not the same image repeating.
                self.x += self.im_dims['w']
                self.repeat += 1
                print(f"repeat = {self.repeat}")
            else:
                self.reached_left_end = True

        #surf.blit(self.surf, (self.x, 0))
        #if self.x < 0:
        #    pass

