class Cell(object):
    __slots__ = (
            'state',
            'lifetime',
            'previous_lifetime',
            'tk_obj',
            'neighbors',
            'alive_neighbors',
            'colors')

    def __init__(self, x1, y1, x2, y2, colors, canvas):
        self.state = 0
        self.lifetime = 0
        self.previous_lifetime = 0
        self.tk_obj = canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=colors[self.lifetime],
                outline="")
        self.neighbors = []
        self.alive_neighbors = 0
        self.colors = colors

    def __str__(self):
        return(
                """
                state:{self.state}
                lifetime:{self.lifetime}
                previous_lifetime:{self.previous_lifetime}
                tk_obj_id:{self.tk_obj}
                num_neighbors:{len(self.neighbors)}
                """
                )

    def tick(self, rule):
        self.state = rule(self.state, self.alive_neighbors)

        if self.state and self.lifetime <= 5:
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

    def check_neighbors(self):
        self.alive_neighbors = 0
        for neighbor in self.neighbors:
            if neighbor.state != 0:
                self.alive_neighbors += 1

    def update_canvas(self, canvas):
        if canvas.itemcget(self.tk_obj, 'fill') != self.colors[self.lifetime]:
            canvas.itemconfig(self.tk_obj, fill=(self.colors[self.lifetime]))

    def reset(self):
        self.previous_lifetime = self.lifetime
        self.state = 0
        self.lifetime = 0
