MAX_LIFETIME = 5


class Cell(object):
    __slots__ = (
            'state',
            'lifetime',
            'previous_lifetime',
            'colors',
            )

    def __init__(self, colors):
        self.state = 0
        self.lifetime = 0
        self.previous_lifetime = 0

    def __str__(self):
        return(
                f"""
                state:{self.state}
                lifetime:{self.lifetime}
                previous_lifetime:{self.previous_lifetime}
                """
                )

    def tick(self, alive_neighbors, rule):
        self.state = rule(self.state, alive_neighbors)
        if self.state and self.lifetime <= MAX_LIFETIME:
            self.lifetime += 1
        elif not self.state:
            self.lifetime = 0

    def toggle(self):
        self.previous_lifetime = self.lifetime
        if self.state:
            self.state = 0
            self.lifetime = 0
        else:
            self.state = 1
            self.lifetime = 1

    def reset(self):
        self.previous_lifetime = self.lifetime
        self.state = 0
        self.lifetime = 0
