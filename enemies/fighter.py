from .bot import Bot
from random import random

class Fighter(Bot):
    """
    Attack script: Move towards the character until one is close enough, and then attack.
    Retreat script: Move away from the character when shields are low to recover
    """
    def __init__(
        self,
        x,
        gravity,
        my_dir,
        bg_info,
        y=None,
        xvel=50,
        direction: str = "null",
        max_hp=1000.,
        max_shield=1000.,
        critical_health=0.4,
        critical_shield=0.2,
        happy_shield=0.65,
        decision_frequency=10
    ):
        super().__init__(
            x=x,
            gravity=gravity,
            my_dir=my_dir,
            bg_info=bg_info,
            y=y,
            xvel=xvel,
            direction=direction,
            max_hp=max_hp,
            max_shield=max_shield,
            critical_health=critical_health,
            critical_shield=critical_shield,
            happy_shield=happy_shield
        )

        # How often (every this many frames) to decide whether or not to change state
        self.decision_frequency = decision_frequency

    def update(self, window_xvel):
        super().update(window_xvel)

        if self.direction == "right":
            self.x += x_vel
            
        elif self.direction == "left":
            self.x -= x_vel

        if self.time % self.decision_frequency == 0:
            self.decide()

    def decide(self):
        if self.state == "attack":
            if random() <= self.p_a_r():
                self.state = "retreat"

        elif self.state == "retreat":
            if random() <= self.p_r_a():
                self.state = "attack"






