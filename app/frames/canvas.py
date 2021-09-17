import tkinter as tk

from app.board import board


class CanvasFrame(tk.Frame):

    def canvas_click_handler(self, event):
        x, y = (event.x, event.y)
        x_index = 0 if not x else x // board.cell_width
        y_index = 0 if not y else y // board.cell_height
        index = x_index + (y_index * board.max_x_pos)
        cell = board.cells[index]
        print(x, y, x_index, y_index, cell)
        cell.toggle()
        self.draw_one(index)

    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg='#bbbbbb')
        self.canvas.pack(expand=1)
        self.canvas.bind("<Button-1>", self.canvas_click_handler)
        self.cells = []
        self.generate_cell_view()

    def draw_one(self, index):
        cell = board.cells[index]
        color = cell.color
        cell_view = self.cells[index]
        self.canvas.itemconfig(cell_view, fill=color)

    def draw(self):
        col_height = board.max_y_pos
        row_width = board.max_x_pos
        for y in range(0, col_height):
            for x in range(0, row_width):
                index = x + (y * row_width)
                if cell := board.cells[index]:
                    cell_view = self.cells[index]
                    if self.itemcget(cell_view, 'fill') != (color := cell.color):
                        self.itemconfig(cell_view, fill=color)

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
        self.cells = cell_view

    def generate_grid(self):
        grid = []
        color = "white"

        if self.master.gui.side_frame.outline_bool.get():
            state = "normal"
        else:
            state = "hidden"

        if len(board.grid):
            for line in self.grid:
                del(line)

        for y in range(0, board.board_height, board.cell_height):
            grid.append(self.gui.canvas.create_line(0, y, self.board_width, y, fill=color, state=state))

        for x in range(0, board.board_width, board.cell_width):
            grid.append(self.gui.canvas.create_line(x, 0, x, self.board_height, fill=color, state=state))

        return tuple(grid)
