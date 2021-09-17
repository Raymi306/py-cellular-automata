from functools import cached_property
import random
import tkinter as tk

from app.cell import Cell


PALETTES = [
        ['', 'black', 'black', 'black', 'black', 'black', 'black'],
        ['', '#ed2b08', '#af0808', '#8c0505', '#4f0505', '#280404', 'black'],
        ['', '#1200ff', '#2e0eba', '#28157c', '#211942', '#130a21', 'black'],
        ['', '#98ff11', '#54cc0a', '#229e06', '#18560a', '#0e3006', 'black'],
        ['', '#b2b1a4', '#b2b1a4', '#b2b1a4', '#b2b1a4', '#b2b1a4', '#b2b1a4'],
        ['', '#e70000', '#ff8c00', '#ffef00', '#00811f', '#0044ff', '#760089']]


class BoardRedux:

    @property
    def max_x_pos(self):
        return int(self.board_width / self.cell_width)

    @property
    def max_y_pos(self):
        return int(self.board_height / self.cell_height)

    @property
    def total_cells(self):
        return self.max_x_pos * self.max_y_pos

    @cached_property
    def tk_str_tickrate(self):
        """cached property so default tk root is available during first access"""
        var = tk.StringVar()
        var.set('100')
        return var

    @property
    def tickrate(self):
        """Any uses of tk_str_tickrate should validate that it is an int"""
        return int(self.tk_str_tickrate.get())

    def __init__(self):
        self.board_width = 640
        self.board_height = 480
        self.cell_width = 16
        self.cell_height = 16
        self.timestep = 1
        self.cells = ()
        self.grid = ()
        self.is_running = False
        self.rules = ({3}, {2, 3})
        self.current_rule = self.define_rules(self.rules)
        self.current_neighborhood = [0, 1, 2, 3, 4, 5, 6, 7]
        self.current_color = PALETTES[0]
        self.reset()

    def randomize(self):
        lottery = random.sample(
                self.cells,
                random.randint(1, (self.total_cells - 1)))
        for cell in lottery:
            cell.toggle()

    def clear(self):
        # TODO why not just reset the whole board..?
        for cell in self.cells:
            cell.reset()
            # update_canvas

    def generate_cells(self):
        cells = []
        if self.cells:
            del self.cells
        for _y in range(0, self.board_height, self.cell_height):
            for _x in range(0, self.board_width, self.cell_width):
                cells.append(Cell(self.current_color))
        return tuple(cells)

    def step(self):
        cells_future = self.cells[:]
        neighborhood = self.current_neighborhood
        for _i in range(self.timestep):
            for cell, cell_future in zip(self.cells, cells_future):
                alive_neighbors = neighborhood # TODO implement
                cell_future.tick(alive_neighbors, self.current_rule)
        self.cells = cells_future

    def run(self):
        self.step()
        #self.gui.current_canvas_callback = self.gui.canvas.after(self.tickrate, self.run)

    def stop(self):
        self.is_running = False
        #self.gui.canvas.after_cancel(self.gui.current_canvas_callback)

    def reset(self):
        #self.gui.canvas.delete('all')
        #self.gui.update_canvas_dim(self.board_width, self.board_height)
        self.cells = self.generate_cells()
        #self.grid = self.generate_grid()
        self.grid = None

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
        def neighborhood(self, index):
            for i in neighborhood_func_indices:
                self.neighbor_functions[i](index)
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


class Board(object):
#---------------------------------------------------------------------------------------------
    def register_gui_callbacks(self):

        def outline_toggle_box_handler():
            if self.gui.outline_bool.get():
                for line in self.grid:
                    self.gui.canvas.itemconfigure(line, state="normal")
            else:
                for line in self.grid:
                    self.gui.canvas.itemconfigure(line, state="hidden")

        def ccs_menu_handler(i):
            for cell in self.cells:
                self.current_color = self.palettes[i]
                cell.colors = self.palettes[i]
                cell.update_canvas(self.gui.canvas)

        def rules_button():

            def apply_callback():

                b = birthe.get().split()
                for i, n in enumerate(b):
                    b[i] = int(n)
                s = survivee.get().split()
                for i, n in enumerate(s):
                    s[i] = int(n)
                l = lb.curselection()[0]
                print(b, s, l)

                self.rules = (set(b), set(s))
                self.current_neighborhood = self.neighborhoods[l]
                self.current_rule = self.define_rules(self.rules)
                self.reset()

            def button_command():
                self.current_neighborhood = []
                for i in range(8):
                    if neighbors_arr[i].cget('state') == 'active':
                        print(str(i))
                        self.current_neighborhood.append(i)
                self.reset()

                born = []
                survives = []

                for i in rborn.curselection():
                    born.append(i + 1)

                for i in rsurvives.curselection():
                    survives.append(i + 1)

                born = set(born)
                survives = set(survives)

                print(born, survives)
                self.rules = (born, survives)
                self.current_rule = self.define_rules(self.rules)

            apply_button.configure(command=button_command)            

        self.gui.side_frame.outline_toggle_box.configure(command=outline_toggle_box_handler)        

        #num_ccs_menu_items = self.gui.ccs_menu.index("last") + 1

        for i in range(self.gui.side_frame.cell_color_selector.menu.index("last") + 1):
            def ccs_menu_lambda(x):
                return lambda: ccs_menu_handler(x)
            self.gui.side_frame.cell_color_selector.menu.entryconfigure(i, command=ccs_menu_lambda(i))

        self.gui.side_frame.rules_button.configure(command=rules_button)


board = BoardRedux()
