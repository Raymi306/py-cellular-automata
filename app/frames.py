import tkinter as tk


def entry_int_checker(new_val):
    try:
        int(new_val)
        return True
    except ValueError:
        return False


class CanvasFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg='#bbbbbb')
        self.canvas.pack(expand=1)


class BottomFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, pady=2)
        vcmd = self.register(entry_int_checker), '%S'
        self.clear_button = tk.Button(
                self,
                text="Clear",
                command=None,
                padx=15)
        self.run_button = tk.Button(
                self,
                text="Run",
                command=None,
                width=15,
                fg="white",
                bg="green",
                anchor="s")
        self.step_button = tk.Button(
                self,
                text="Step",
                command=None)
        self.step_entry = tk.Entry(
                self,
                width=5,
                justify="center",
                validate="key",
                vcmd=vcmd)
        self.randomize_button = tk.Button(
                self,
                text="Randomize",
                command=None)
        self.clear_button.pack(side="left", padx=45)
        self.run_button.pack(side="left")
        self.step_button.pack(side="left")
        self.step_entry.pack(side="left", padx=4)
        self.randomize_button.pack(side="right", padx=15)


class SideFrame(tk.Frame):
    def __init__(self, parent, outline_bool):
        super().__init__(parent, padx=10, pady=10)
        self.vcmd = self.register(entry_int_checker), '%S'
        self.outline_bool = outline_bool
        # TODO change to spinboxes
        self._init_board_size_widgets()
        self._init_cell_size_widgets()
        self.tickrate_label = tk.Label(self, text="Tickrate", relief="ridge")
        self.tickrate_entry = tk.Entry(
                self,
                width=4,
                justify="center",
                validate="key",
                vcmd=self.vcmd)
        self.tickrate_scale = tk.Scale(
                self,
                from_=500,
                to=1,
                length=80,
                showvalue=0,
                sliderlength=15,
                bd=0)
        self.outline_toggle_box = tk.Checkbutton(
                self,
                text="Cell Outline",
                variable=self.outline_bool,
                relief="raised")
        self.cell_color_selector = CellColorSelector(self)
        self.rules_button = tk.Button(self, text="Rules")
        self.apply_settings_button = tk.Button(
                self,
                text="Apply\nSettings",
                command=None,
                padx=10,
                pady=10)
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
        self.cell_width_label.pack()
        self.cell_width_entry.pack()
        self.cell_height_label.pack()
        self.cell_height_entry.pack()


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
