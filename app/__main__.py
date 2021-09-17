import tkinter as tk

from app.gui import Gui
from app.board import board as board_state

root = tk.Tk()
gui = Gui(root, board_state)
root.mainloop()
