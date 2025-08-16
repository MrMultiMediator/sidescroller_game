from .bot import Bot
from random import random

class Fighter(Bot):
    """
    Attack script: Move towards the character until one is close enough, and then attack.
    Retreat script: Move away from the character when shields are low to recover

    confident_strike: How deep within striking distance to be confident we can make a hit
        I.e. if striking distance is 100px and confident strike is 0.85, we have to think
        we are 85px away to feel confident to make a strike.
    uncertainty: Models the enemy not knowing exact distances. They can't be all-knowing.
        This is in units of px. Whatever th real distance form the player is, this is the
        standard deviation in pixels for where the enemy will guess the player is. Basically
        the assumed distance that the enemy will guess will be sampled as a gaussian
        distribution about the actual distance using this value as the standard deviation.
    bias: How much to shift the guassian sampled for the assumed distance away from the
        actual distance. This can be used to make certain fighters consistently overguess
        or underguess.
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
        decision_frequency=10,
        confident_strike=0.85,
        uncertainty=10,
        bias=0
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

        self.decision_frequency = decision_frequency
        self.confident_strike = confident_strike
        self.uncertainty = uncertainty
        self.bias = bias

    def update(self, window_xvel, player_info):
        super().update(window_xvel)

        if self.state == "attack":
            self.run_atk_script()

        if self.state == "retreat":
            self.run_retreat_script()

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
                return

        elif self.state == "retreat":
            if random() <= self.p_r_a():
                self.state = "attack"

    def run_atk_script(self):
        pass

    def run_retreat_script(self):
        pass