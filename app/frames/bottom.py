import tkinter as tk

from app.frames.util import entry_int_checker
from app.board import board


class ClearButton(tk.Button):

    def cmd(self):
        board.reset()
        self.event_generate('<<draw_once>>')

    def __init__(self, parent):
        super().__init__(parent, text='Clear', command=self.cmd, padx=15)


class RunButton(tk.Button):

    running_config = {'bg': 'red', 'text': 'Stop'}
    stopped_config = {'bg': 'green', 'text': 'Run'}

    def __init__(self, parent):
        super().__init__(
                parent,
                width=15,
                fg='white',
                command=self.cmd,
                anchor="s")
        self.set_stopped_style()

    def cmd(self):
        if board.is_running:
            board.is_running = False
            self.set_stopped_style()
        else:
            board.is_running = True
            self.set_running_style()
        self.event_generate('<<draw_continuous>>')

    def set_running_style(self):
        self.config(**self.running_config)

    def set_stopped_style(self):
        self.config(**self.stopped_config)


class StepButton(tk.Button):

    def cmd(self):
        self.event_generate('<<draw_once>>')

    def __init__(self, parent):
        super().__init__(
                parent,
                text='Step',
                command=self.cmd)


class TimestepEntry(tk.Entry):
    def cmd(self, *args):
        board.timestep = int(self.get())

    def __init__(self, parent):
        super().__init__(
                parent,
                width=5,
                justify="center",
                validate="key",
                vcmd=parent.vcmd)
        self.insert(0, board.timestep)
        self.bind('<Return>', self.cmd)


class RandomizeButton(tk.Button):

    def cmd(self):
        board.randomize()
        self.event_generate('<<redraw>>')

    def __init__(self, parent):
        super().__init__(parent, text='Randomize', command=self.cmd)


class BottomFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, pady=2)
        vcmd = self.register(entry_int_checker), '%S'
        self.vcmd = vcmd
        # instantiate widgets
        self.clear_button = ClearButton(self)
        self.run_button = RunButton(self)
        self.step_button = StepButton(self)
        self.step_entry = TimestepEntry(self)
        self.randomize_button = RandomizeButton(self)
        # pack
        self.clear_button.pack(side="left", padx=45)
        self.run_button.pack(side="left")
        self.step_button.pack(side="left")
        self.step_entry.pack(side="left", padx=4)
        self.randomize_button.pack(side="right", padx=15)

