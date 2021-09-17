import tkinter as tk

from app.board import board
from app.frames.util import entry_int_checker, clamp_int

class TickrateEntry(tk.Entry):

    def __init__(self, parent):
        super().__init__(
                parent,
                width=4,
                justify="center",
                validate="key",
                vcmd=parent.vcmd,
                textvariable=board.tk_str_tickrate)


class TickrateScale(tk.Scale):

    def __init__(self, parent):
        super().__init__(
                parent,
                from_=500,
                to=1,
                length=80,
                showvalue=0,
                sliderlength=15,
                bd=0,
                variable=board.tk_str_tickrate)


class ApplySettingsButton(tk.Button):

    def __init__(self, parent):
        super().__init__(
                parent,
                text="Apply\nSettings",
                command=None,
                padx=10,
                pady=10)


class CellColorSelector(tk.Menubutton):
    def __init__(self, parent):
        super().__init__(parent, text="Cell Colors", relief="raised")
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Blk")
        self.menu.add_command(label="Red")
        self.menu.add_command(label="Blu")
        self.menu.add_command(label="Grn")
        self.menu.add_command(label="Bkg")
        self.menu.add_command(label="Rbw")
        self["menu"] = self.menu


class SideFrame(tk.Frame):

    def update_tickrate(self, new_tickrate):
        # TODO figure out TK variables
        try:
            new_tickrate = int(new_tickrate)
        except ValueError:
            pass
        new_tickrate = clamp_int(new_tickrate, 1, 9999)
        board.tk_str_tickrate.set(new_tickrate)

    def tickrate_entry_cmd(self):
        return self.update_tickrate(self.tickrate_entry.get())

    def tickrate_scale_cmd(self, e):
        return self.update_tickrate(e)

    def apply_settings_cmd(self):
        board.stop()
        try:
            new_width = int(self.board_width_entry.get())
        except ValueError:
            pass
        else:
            new_width = clamp_int(new_width, 50, 1280)
            board.board_width = new_width
        try:
            new_height = int(self.board_height_entry.get())
        except ValueError:
            pass
        else:
            new_height = clamp_int(new_height, 50, 1024)
            board.board_height = new_height
        try:
            new_cell_w = int(self.gui.side_frame.cell_width_entry.get())
        except ValueError:
            pass
        else:
            new_cell_w = clamp_int(new_cell_w, 1, 1280)
            board.cell_width = new_cell_w
        try:
            new_cell_h = int(self.gui.side_frame.cell_height_entry.get())
        except ValueError:
            pass
        else:
            new_cell_h = clamp_int(new_cell_h, 1, 1024)
            board.cell_height = new_cell_h

        self.board_width_entry.delete(0, tk.END)
        self.board_height_entry.delete(0, tk.END)
        self.cell_width_entry.delete(0, tk.END)
        self.cell_height_entry.delete(0, tk.END)
        self.board_width_entry.insert(0, board.board_width)
        self.board_height_entry.insert(0, self.board_height)
        self.cell_width_entry.insert(0, self.cell_width)
        self.cell_height_entry.insert(0, self.cell_height)
        board.reset()

    def __init__(self, parent, outline_bool):
        super().__init__(parent, padx=10, pady=10)
        self.vcmd = self.register(entry_int_checker), '%S'
        self.outline_bool = outline_bool
        # instantiate
        self._init_board_size_widgets()
        self._init_cell_size_widgets()
        self.tickrate_label = tk.Label(self, text="Tickrate", relief="ridge")
        self.tickrate_entry = TickrateEntry(self)
        self.tickrate_scale = TickrateScale(self)
        self.outline_toggle_box = tk.Checkbutton(
                self,
                text="Cell Outline",
                variable=self.outline_bool,
                relief="raised")
        self.cell_color_selector = CellColorSelector(self)
        self.rules_button = tk.Button(self, text="Rules")
        self.apply_settings_button = ApplySettingsButton(self)
        # configure
        self.board_width_entry.insert(0, board.board_width)
        self.board_height_entry.insert(0, board.board_height)
        self.cell_width_entry.insert(0, board.cell_width)
        self.cell_height_entry.insert(0, board.cell_height)
        self.tickrate_scale.configure(command=self.tickrate_scale_cmd)
        self.tickrate_entry.bind('<Return>', self.tickrate_entry_cmd)
        self.apply_settings_button.configure(command=self.apply_settings_cmd)
        # pack
        self._pack_board_size_widgets()
        self._pack_cell_size_widgets()
        self.tickrate_label.pack()
        self.tickrate_entry.pack()
        self.tickrate_scale.pack(pady=3)
        self.outline_toggle_box.pack()
        self.cell_color_selector.pack(pady=3)
        self.rules_button.pack()
        self.apply_settings_button.pack(side="bottom")

    def _init_board_size_widgets(self):
        self.board_width_label = tk.Label(
                self,
                text="Board Width",
                relief="ridge")
        self.board_width_entry = tk.Entry(
                self,
                width=6,
                justify="center",
                validate="key",
                vcmd=self.vcmd)
        self.board_height_label = tk.Label(
                self,
                text="Board Height",
                relief="ridge")
        self.board_height_entry = tk.Entry(
                self,
                width=6,
                justify="center",
                validate="key",
                vcmd=self.vcmd)

    def _pack_board_size_widgets(self):
        self.board_width_label.pack()
        self.board_width_entry.pack()
        self.board_height_label.pack()
        self.board_height_entry.pack()

    def _init_cell_size_widgets(self):
        self.cell_width_label = tk.Label(
                self,
                text="Cell Width",
                relief="ridge")
        self.cell_width_entry = tk.Entry(
                self,
                width=4,
                justify="center",
                validate="key",
                vcmd=self.vcmd)
        self.cell_height_label = tk.Label(
                self,
                text="Cell Height",
                relief="ridge")
        self.cell_height_entry = tk.Entry(
                self,
                width=4,
                justify="center",
                validate="key",
                vcmd=self.vcmd)

    def _pack_cell_size_widgets(self):
        self.cell_width_label.pack()
        self.cell_width_entry.pack()
        self.cell_height_label.pack()
        self.cell_height_entry.pack()
