import tkinter as tk

from app.board import board


class CanvasFrame(tk.Frame):

    def canvas_click_handler(self, event):
        x, y = (event.x, event.y)
        x_index = 0 if not x else x // board.cell_width
        y_index = 0 if not y else y // board.cell_height
        index = x_index + (y_index * board.max_x_pos)
        try:
            cell = board.cells[index]
        except IndexError:
            pass
        else:
            cell.toggle()
            self.draw_one(index)

    def draw_continuous(self, *args):
        if board.is_running:
            self.draw_continuous_callback = \
                self.canvas.after(board.tickrate, self.step_and_draw_loop)
        else:
            self.canvas.after_cancel(self.draw_continuous_callback)

    def __init__(self, parent):
        super().__init__(parent)
        self.draw_continuous_callback = None
        self.canvas = tk.Canvas(self, bg='#bbbbbb')
        self.canvas.pack(expand=1)
        self.canvas.bind('<Button-1>', self.canvas_click_handler)
        self.event_add('<<draw_once>>', [None])
        self.event_add('<<draw_continuous>>', [None])
        self.event_add('<<redraw>>', [None])
        self.bind_all('<<draw_once>>', self.step_and_draw)
        self.bind_all('<<draw_continuous>>', self.draw_continuous)
        self.bind_all('<<redraw>>', self.draw)
        self.cells = []
        self.grid_lines = []
        self.reset()

    def draw_one(self, index):
        colors = board.current_color
        cell = board.cells[index]
        color = colors[cell.lifetime]
        cell_view = self.cells[index]
        self.canvas.itemconfig(cell_view, fill=color)

    def draw(self, *args):
        colors = board.current_color
        col_height = board.max_y_pos
        row_width = board.max_x_pos
        for y in range(0, col_height):
            for x in range(0, row_width):
                index = x + (y * row_width)
                cell = board.cells[index]
                cell_view = self.cells[index]
                color = colors[cell.lifetime]
                self.canvas.itemconfig(cell_view, fill=color)

    def step_and_draw_loop(self, *args):
        self.step_and_draw()
        self.draw_continuous_callback = self.canvas.after(
            board.tickrate,
            self.step_and_draw_loop
        )

    def step_and_draw(self, *args):
        board.step()
        self.draw()

    def draw_grid(self):
        if self.master.side_frame.outline_bool.get():
            state = "normal"
        else:
            state = "hidden"
        for line in self.grid_lines:
            self.canvas.itemconfig(line, state=state)

    def generate_cell_view(self):
        cell_view = []
        if self.cells:
            del self.cells
        width = board.cell_width
        height = board.cell_height
        for y in range(0, board.board_height, height):
            for x in range(0, board.board_width, width):
                cell_view.append(self.canvas.create_rectangle(
                    x, y,
                    x + width, y + height,
                    fill=board.current_color[0],
                    outline='',)
                )
        return cell_view

    def generate_grid(self):
        grid = []
        color = "white"

        if self.master.side_frame.outline_bool.get():
            state = "normal"
        else:
            state = "hidden"

        if len(board.grid):
            del self.grid_lines
            self.grid_lines = []

        for y in range(0, board.board_height, board.cell_height):
            grid.append(self.canvas.create_line(
                0, y,
                board.board_width, y,
                fill=color, state=state)
            )

        for x in range(0, board.board_width, board.cell_width):
            grid.append(self.canvas.create_line(
                x, 0,
                x, board.board_height,
                fill=color, state=state)
            )

        return tuple(grid)

    def update_canvas_dim(self, width, height):
        self.canvas.delete("all")
        self.canvas.configure(width=width, height=height)
        self.update_idletasks()

    def reset(self):
        self.canvas.delete('all')
        self.update_canvas_dim(board.board_width, board.board_height)
        self.cells = self.generate_cell_view()
        self.grid_lines = self.generate_grid()
