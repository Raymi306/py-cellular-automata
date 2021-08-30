import tkinter as tk
from app.board import Board
from app.gui import Gui

root = tk.Tk()
gui = Gui(root)
board = Board(gui)
root.mainloop()
