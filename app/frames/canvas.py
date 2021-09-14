import tkinter as tk


class CanvasFrame(tk.Frame):

    def canvas_click_handler(self, event):
        tk_obj_id = event.widget.find_closest(event.x, event.y)[0]
        for cell in self.master.board.cells:
            if cell.tk_obj == tk_obj_id:
                cell.toggle()
                break

    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg='#bbbbbb')
        self.canvas.pack(expand=1)
        self.canvas.bind("<Button-1>", self.canvas_click_handler)
