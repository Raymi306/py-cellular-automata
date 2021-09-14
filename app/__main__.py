import tkinter as tk
from app.board import BoardRedux
from app.gui import Gui

root = tk.Tk()
board = BoardRedux()
gui = Gui(root, board)
root.mainloop()
