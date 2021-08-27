import tkinter as tk

from app.frames import BottomFrame, SideFrame
from app.board import Board


def entry_int_checker(new_val):
    try:
        int(new_val)
        return True
    except ValueError:
        return False


class Gui(tk.Frame):

    __slots__ = ()
    SIDE_COLUMN_PADDING = 10
    BOTTOM_COLUMN_PADDING = 2
    canvas_color = "#bbbbbb"
    current_canvas_callback = -1
    toplevel_rules = None

    def __init__(self, parent, *args, **kwargs):

        super().__init__(parent)
        self.master.title("Cellular automata - tkinter test")
        # frames
        self.outline_bool = tk.IntVar() # in this scope due to struggle with toggle box
        self.outline_bool.set(1)
        self.side_frame = SideFrame(self, self.outline_bool)
        self.canvas_frame = tk.Frame(self)
        self.bottom_frame = BottomFrame(self)
        self.side_frame.pack(side="left", fill="y")
        self.canvas_frame.pack(fill="both", expand="1")
        self.bottom_frame.pack(side="bottom")

        # canvas frame
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.canvas_color)
        self.canvas.pack(expand=1)

        self.pack(expand=1)
        self.update_idletasks()

        w_width = self.master.winfo_width()
        w_height = self.master.winfo_height()
        self.master.minsize(w_width, w_height)
        print(f"window width/height{(self.master.winfo_width(), self.master.winfo_height())}")

    def update_canvas_dim(self, width, height):
        self.canvas.delete("all")
        self.canvas.configure(width=width, height=height)
        self.update_idletasks()
        w_width = self.master.winfo_reqwidth()
        w_height = self.master.winfo_reqheight()
        self.master.minsize(w_width, w_height)


root = tk.Tk()
gui = Gui(root)
board = Board(gui)
root.mainloop()
