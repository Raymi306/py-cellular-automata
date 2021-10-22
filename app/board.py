from copy import deepcopy
from functools import cached_property
import random
import tkinter as tk

from app.cell import Cell
from app.palettes import PALETTES


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
        for _y in range(0, self.board_height, self.cell_height):
            for _x in range(0, self.board_width, self.cell_width):
                cells.append(Cell())
        return tuple(cells)

    def get_alive_neighbors(self, index):
        neighbor_indices = self.current_neighborhood(index)
        alive_neighbors = 0
        for i in neighbor_indices:
            if self.cells[i].state != 0:
                alive_neighbors += 1
        return alive_neighbors

    def step(self):
        for _i in range(self.timestep):
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

    def get_nw(self, index):
        default_case = index - self.max_x_pos - 1

        if index < self.max_x_pos\
                and index % self.max_x_pos != 0:  # top row exclude top left
            return default_case + self.total_cells
        elif index % self.max_x_pos == 0:  # left col
            left_col_case = index - 1
            if left_col_case < 0:  # top left...
                return self.total_cells - 1
            else:
                return left_col_case
        else:
            return default_case

    def get_ne(self, index):
        default_case = index - self.max_x_pos + 1
        # exclude corner
        if index < self.max_x_pos\
                and index % self.max_x_pos != self.max_x_pos - 1:
            return default_case + self.total_cells
        elif index % self.max_x_pos == self.max_x_pos - 1:
            right_col_case = default_case - self.max_x_pos
            if right_col_case < 0:
                return self.total_cells + right_col_case
            else:
                return right_col_case
        else:
            return default_case

    def get_sw(self, index):
        default_case = index + self.max_x_pos - 1
        # bot row exclude bot left
        if index + self.max_x_pos >= self.total_cells\
                and index % self.max_x_pos != 0:
            return default_case - self.total_cells
        elif index % self.max_x_pos == 0:  # left col
            left_col_case = default_case + self.max_x_pos
            if left_col_case >= self.total_cells:
                return self.max_x_pos - 1
            else:
                return left_col_case
        else:
            return default_case

    def get_se(self, index):
        default_case = index + self.max_x_pos + 1

        # bot row exclude bot right
        if index + self.max_x_pos >= self.total_cells\
                and index % self.max_x_pos != self.max_x_pos - 1:
            return default_case - self.total_cells
        elif index % self.max_x_pos == self.max_x_pos - 1:  # right col
            right_col_case = default_case - self.max_x_pos
            if right_col_case >= self.total_cells:
                return 0
            else:
                return right_col_case
        else:
            return default_case

    def get_n(self, index):
        if index >= self.max_x_pos:
            return index - self.max_x_pos
        else:
            return index + self.total_cells - self.max_x_pos

    def get_w(self, index):
        if index - 1 >= 0\
                and (index - 1) % self.max_x_pos != self.max_x_pos - 1:
            return index - 1
        else:
            return index + self.max_x_pos - 1

    def get_e(self, index):
        if (index + 1) % self.max_x_pos != 0\
           and index + 1 < self.total_cells:
            return index + 1
        else:
            return index - self.max_x_pos + 1

    def get_s(self, index):
        if (index + self.max_x_pos) < self.total_cells:
            return index + self.max_x_pos
        else:
            return index - self.total_cells + self.max_x_pos

    neighbor_functions = (
            get_nw, get_n, get_ne, get_w, get_e, get_sw, get_s, get_se
            )

    def define_neighborhood(self, neighborhood_func_indices):
        def neighborhood(index):
            indices = []
            for i in neighborhood_func_indices:
                indices.append(self.neighbor_functions[i](self, index))
            return indices
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
