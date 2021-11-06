from copy import deepcopy
import random

from app.cell import Cell
from app.palettes import PALETTES
import app.neighborhoods.wrap as wrapping_neighborhood
import app.neighborhoods.nowrap as nowrap_neighborhood


class Board:

    @property
    def max_x_pos(self):
        return int(self.board_width / self.cell_width)

    @property
    def max_y_pos(self):
        return int(self.board_height / self.cell_height)

    @property
    def total_cells(self):
        return self.max_x_pos * self.max_y_pos

    def __init__(self):
        self.tickrate = None
        self.board_width = 480
        self.board_height = 480
        self.cell_width = 30
        self.cell_height = 30
        self.timestep = 1
        self.cells = ()
        self.grid = ()
        self.is_running = False
        self.born_ruleset = {3}
        self.survives_ruleset = {2, 3}
        self.current_rule = self.define_rules(
                (self.born_ruleset, self.survives_ruleset)
                )
        self.neighborhood_func_indices = (0, 1, 2, 3, 4, 5, 6, 7)
        self.current_neighborhood = self.define_neighborhood(
                self.neighborhood_func_indices
                )
        self.current_color = PALETTES['blk']
        self.reset()

    def randomize(self):
        lottery = random.sample(
                self.cells,
                random.randint(1, (self.total_cells - 1)))
        for cell in lottery:
            cell.toggle()

    def generate_cells(self):
        cells = []
        if self.cells:
            del self.cells
        for _ in range(0, self.board_height, self.cell_height):
            for _ in range(0, self.board_width, self.cell_width):
                cells.append(Cell())
        return tuple(cells)

    def get_alive_neighbors(self, index):
        neighbor_indices = self.current_neighborhood(index)
        alive_neighbors = 0
        for i in neighbor_indices:
            try:
                if self.cells[i].state != 0:
                    alive_neighbors += 1
            except IndexError:
                pass
        return alive_neighbors

    def step(self):
        for _ in range(self.timestep):
            cells_future = deepcopy(self.cells)
            for i, cell_future in enumerate(cells_future):
                alive_neighbors = self.get_alive_neighbors(i)
                cell_future.tick(alive_neighbors, self.current_rule)
            self.cells = cells_future

    def run(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def reset(self):
        self.cells = self.generate_cells()

    def define_neighborhood(self, neighborhood_func_indices, wrap=True):
        def neighborhood(index):
            neighbor_functions = wrapping_neighborhood.functions\
                    if wrap else nowrap_neighborhood.functions
            return [neighbor_functions[i](self, index) for i in neighborhood_func_indices]
        return neighborhood

    def define_rules(self, bs_tuple):
        birth_set = bs_tuple[0]
        survive_set = bs_tuple[1]

        def rule(status, alive_neighbors):
            if status:
                if alive_neighbors not in survive_set:
                    return 0
            elif alive_neighbors in birth_set:
                return 1
            return status
        return rule


board = Board()
