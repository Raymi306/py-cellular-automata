import tkinter as tk

from app.frames import BottomFrame, SideFrame, CanvasFrame


class Gui(tk.Frame):

    current_canvas_callback = -1
    toplevel_rules = None

    def __init__(self, parent):
        super().__init__(parent)
        self.master.title("Cellular automata - tkinter test")
        # frame instantiations
        self.side_frame = SideFrame(self)
        self.canvas_frame = CanvasFrame(self)
        self.canvas = self.canvas_frame.canvas
        self.bottom_frame = BottomFrame(self)
        # frame packing
        self.side_frame.pack(side="left", fill="y")
        self.canvas_frame.pack(fill="both", expand="1")
        self.bottom_frame.pack(side="bottom")
        self.pack(expand=1)
        self.reset()

    def reset(self):
        self.update_idletasks()
        w_width = self.master.winfo_reqwidth()
        w_height = self.master.winfo_reqheight()
        self.master.minsize(w_width, w_height)
        print(f"window width/height: {self.master.winfo_width()}/{self.master.winfo_height()}")  # noqa: E501 line length
