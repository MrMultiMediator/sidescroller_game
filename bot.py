class Bot:
    """Collision rules:
    Character state | Enemy state | Character effect | Enemy effect
    ----------------|-------------|------------------|-------------
     Neutral        |  Neutral    |    Nothing       |   Nothing
     Attacking      |  Neutral    |    Nothing       | Health loss
     Attacking      |  Attacking  |  Health loss     | Health loss
     Neutral        |  Attacking  |  Health loss     |   Nothing
     Shielding      |  Attacking  |  Shield2 loss    | Health loss

    Nothing = Shield recovery. All shields recover over a period of time for both the
    character and the enemies, both shield and shield2. Shield2 is the active shield
    that only the player has. Shield is something that everyone has by default.
    """
    def __init__(self, x, y, gravity, xvel=50, move="null"):
        self.x = x
        self.y = y
        self.gravity = gravity
        self.x_vel = xvel
        self.time = 0
        self.status = "idle"
        self.move = move

    def update(self, window_xvel):
        """Everything that is not the main character (everything of this base class)
        needs to move relative to the main character. This update function needs to be
        informed by how fast the window is moving since the character is always in the
        center of the frame, and they need to be shifted over by that. This is the
        variable 'delta' returned by Player.update, i.e. this value is accessible after
        the player updates."""
        self.time += 1
        self.x += window_xvel

        if self.time > 10000000:
            self.time = 0

        if self.move == "right":
            self.x += x_vel
            
        elif self.move == "left"
            self.x -= x_vel

    def decide(self):
        "Decision to change one's status"
        pass