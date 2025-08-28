from .bot import Bot
from random import random
import sys
import os

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
        decision_frequency: int=5,
        confident_strike=0.85,
        uncertainty=10,
        bias=0,
        atk_strengths: dict = {
            "jab1": 5,
            "kick1": 10,
            "uppercut1": 5
        },
        strength=1.,
        walk_vel=25,
        run_vel=40
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
        self.strength = strength

        # Add various attack strengths to the atk_surface topology sub-dictionary
        for key, value in atk_strengths.items():
            self.topology["atk_surf"][key]["strength"] = value

        self.walk_vel = walk_vel
        self.run_vel = run_vel
        self.damage = {'jab1': 15, 'uppercut1': 5, 'kick1': 25}

    def update(self, window_xvel, player_info):
        # TODO implement a safe stopping distance for an enemy in retreat, or at least a point
        #      where they switch to walking if they're far enough away.
        super().update(window_xvel)
        self.update_health()
        self.player_info = player_info

        dist_from_player = self.compute_dist_from_player()

        if self.time % self.decision_frequency == 0:
            self.decide()

        if self.state == "attack":
            self.run_atk_script()

        if self.state == "retreat":
            self.run_retreat_script()


        if self.direction == "right" or self.direction == "left" and (self.x >= self.player_info['x'] + 0.6*self.x_vel or self.x <= self.player_info['x'] - 0.6*self.x_vel):
            if self.status != "walk" and self.status != "run":
                self.status = "walk"
            if self.status == "walk":
                if self.shield > 2.5*self.critical_shield*self.max_shield:
                    print(f'running {self.shield}')
                    self.status = "run"
                    self.x_vel = self.run_vel

            if self.status == "run":
                self.shield -= self.max_shield*0.01

                if self.shield < 1.25*self.critical_shield*self.max_shield:
                    print(f'walking {self.shield}')
                    self.status = "walk"
                    self.x_vel = self.walk_vel


            if self.direction == "right":
                self.x += self.x_vel
                
            elif self.direction == "left":
                self.x -= self.x_vel

        self.post_update()

    def update_health(self):
        # Every 1/10th of a second, recharge shields by 2%
        if self.time % 3 == 0:
            if self.shield < self.max_shield:
                self.shield += self.max_shield*0.02

            if self.shield > self.max_shield:
                self.shield = self.max_shield

    def decide(self):
        if self.state == "attack":
            if random() <= self.p_a_r():
                self.state = "retreat"
                return

        elif self.state == "retreat":
            if random() <= self.p_r_a():
                self.state = "attack"

    def compute_dist_from_player(self):
        return self.x - self.player_info['x']


    def run_atk_script(self):
        if self.x >= self.player_info['x']:
            self.direction = "left"
            #print(self.l_dist) # Striking distance dict from left w/ keys being attacks and values distances.
        else:
            self.direction = "right"
            #print(self.r_dist)

        # TODO determine which attacks are in range and randomly sample from those to decide your attack

    def run_retreat_script(self):
        if self.x >= self.player_info['x']:
            self.direction = "right"
        else:
            self.direction = "left"