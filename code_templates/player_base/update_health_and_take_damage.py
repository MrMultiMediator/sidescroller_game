    def update_health(self):
        # Every 1/10th of a second, recharge shields by 2%
        if self.time % 3 == 0:
            if self.shield < self.max_shield:
                self.shield += self.max_shield*0.02

            if self.shield > self.max_shield:
                self.shield = self.max_shield

        self.health_bar.draw(self.hp, self.shield)

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

