from .bot import Bot

class Fighter(Bot):
    """
    Attack script: Move towards the character until one is close enough, and then attack.
    Retreat script: Move away from the character when shields are low to recover
    """

    def update(self, window_xvel):
        super().update(window_xvel)

        if self.move == "right":
            self.x += x_vel
            
        elif self.move == "left":
            self.x -= x_vel

    def decide(self):
        pass