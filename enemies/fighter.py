from .bot import Bot
from random import random, choice
import sys
import os
from numpy.random import normal

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
        name,
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
        run_vel=32
    ):
        super().__init__(
            name=name,
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
        self.damage = {'jab1': 45, 'uppercut1': 15, 'kick1': 65}
        self.attack_has_dealt_damage = False

    def update(self, window_xvel, player_info):
        # TODO implement a safe stopping distance for an enemy in retreat, or at least a point
        #      where they switch to walking if they're far enough away.
        super().update(window_xvel)
        self.update_health()
        self.player_info = player_info

        dist_from_player = self.compute_dist_from_player()

        if self.time % self.decision_frequency == 0:
            self.decide()

        if self.state == "attack" and self.status not in self.damage.keys():
            self.run_atk_script()

        if self.state == "retreat":
            self.run_retreat_script()


        if self.direction == "right" or self.direction == "left" and self.status not in self.damage.keys() and (self.x >= self.player_info['x'] + 0.75*self.x_vel or self.x <= self.player_info['x'] - 0.75*self.x_vel):
            if self.status != "walk" and self.status != "run":
                self.status = "walk"
                self.frame = 1
            if self.status == "walk":
                if self.shield > 2.5*self.critical_shield*self.max_shield:
                    self.status = "run"
                    self.x_vel = self.run_vel

            if self.status == "run":
                self.shield -= self.max_shield*0.01

                if self.shield < 1.25*self.critical_shield*self.max_shield:
                    self.status = "walk"
                    self.x_vel = self.walk_vel

        elif self.status == "walk" or self.status == "run":
            self.frame = 1
            self.status = "idle"


        if self.status == "walk" or self.status == "run":
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

    def attacks_in_range(self):
        atks_in_range = []

        for atk in self.damage.keys():
            if self.direction == "right":
                if abs(self.x - self.player_info['x']) < self.r_dist[atk]*self.confident_strike:
                    atks_in_range.append(atk)

            if self.direction == "left":
                if abs(self.x - self.player_info['x']) < self.l_dist[atk]*self.confident_strike:
                    atks_in_range.append(atk)

        return atks_in_range

    def distance_estimate(self, atk):
        """This function emulates that enemies are not all-knowing and computes an
        'estimate' of the distance to the player using the uncertainty and bias."""
        return self.bias + normal(
            loc=abs(self.x - self.player_info['x']),
            scale=self.uncertainty
        )

    def run_atk_script(self):
        if self.x >= self.player_info['x']:
            self.direction = "left"
            #print(self.l_dist) # Striking distance dict from left w/ keys being attacks and values distances.
        else:
            self.direction = "right"
            #print(self.r_dist)

        atks_in_range = self.attacks_in_range()
        if len(atks_in_range) > 0:
            atk = choice(atks_in_range)

            # Compute estimated distance for the attack to decide if we want to do it
            if self.direction == "right":
                distance_goal = abs(self.confident_strike*self.r_dist[atk])
            elif self.direction == "left":
                distance_goal = abs(self.confident_strike*self.l_dist[atk])

            if self.distance_estimate(atk) < distance_goal:
                self.frame = 1
                self.status = atk
                self.attack_has_dealt_damage = False
                #print(f"Striking player with attack {atk}")

    def take_damage(self, amount):
        if self.shield > 0:
            if self.shield >= amount:
                self.shield -= amount
            else:
                amount -= self.shield
                self.shield = 0
                self.hp -= amount
        else:
            self.hp -= amount

        if self.hp <= 0:
            self.hp = 0
            self.status = "fall1"

        # TODO determine which attacks are in range and randomly sample from those to decide your attack

    def run_retreat_script(self):
        if self.x >= self.player_info['x']:
            self.direction = "right"
        else:
            self.direction = "left"