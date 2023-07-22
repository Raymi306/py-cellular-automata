MAX_LIFETIME = 5


class Cell(object):
    __slots__ = (
        'state',
        'lifetime',
    )

    def __init__(self):
        self.state = 0
        self.lifetime = 0

    def __str__(self):
        return(f'state: {self.state}, lifetime: {self.lifetime}')

    def tick(self, alive_neighbors, rule):
        self.state = rule(self.state, alive_neighbors)
        if self.state and self.lifetime <= MAX_LIFETIME:
            self.lifetime += 1
        elif not self.state:
            self.lifetime = 0

    def toggle(self):
        if self.state:
            self.state = 0
            self.lifetime = 0
        else:
            self.state = 1
            self.lifetime = 1

    def reset(self):
        self.state = 0
        self.lifetime = 0
