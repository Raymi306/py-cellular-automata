import tkinter as tk

from app.board import board


class NeighborSelectorBox(tk.Label):
    def click_handler(self, e):
        if e.widget.cget('state') == 'normal':
            e.widget.config(state='active')
        else:
            e.widget.config(state='normal')

    def is_active(self):
        return self.cget('state') == 'active'

    def __init__(self, parent, bg='gray'):
        super().__init__(
                parent,
                bg=bg,
                activebackground='black',
                width=4,
                height=2,
                relief='sunken'
                )


class NeighborSelectorFrame(tk.Frame):
    def get_selection(self):
        return [i for i in range(8) if self.neighbor_selectors[i].cget('state') == 'active']

    def __init__(self, parent):
        super().__init__(parent)
        self.nwn = NeighborSelectorBox(self)
        self.nn = NeighborSelectorBox(self)
        self.nen = NeighborSelectorBox(self)
        self.wn = NeighborSelectorBox(self)
        self.center = NeighborSelectorBox(self, bg='brown')
        self.en = NeighborSelectorBox(self)
        self.swn = NeighborSelectorBox(self)
        self.sn = NeighborSelectorBox(self)
        self.sen = NeighborSelectorBox(self)
        self.neighbor_wrap_toggle = tk.Checkbutton(self, text='Wrap')

        self.neighbor_selectors = [
                self.nwn, self.nn, self.nen,
                self.wn, self.en,
                self.swn, self.sn, self.sen
                ]

        for widget in self.neighbor_selectors:
            widget.bind('<Button-1>', widget.click_handler)

        for i in board.neighborhood_func_indices:
            self.neighbor_selectors[i].config(state='active')

        _selectors = self.neighbor_selectors.copy()
        _selectors.insert(4, self.center)  # put center in between wn and en

        for i, widget in enumerate(_selectors):
            widget.grid(row=i//3, column=i % 3, padx=2, pady=2)


class RuleListbox(tk.Listbox):
    def __init__(self, parent):
        super().__init__(
                parent,
                selectmode='multiple',
                exportselection=False,
                width=4,
                height=8,
                activestyle='none')
        for i in range(1, 8):
            self.insert('end', f' {i}')


class RulesPopup(tk.Toplevel):
    def apply_callback(self, *args):
        born = {i + 1 for i in self.born_listbox.curselection()}
        board.born_ruleset = born
        survives = {i + 1 for i in self.survives_listbox.curselection()}
        board.survives_ruleset = survives
        rules = (set(born), set(survives))
        board.current_rule = board.define_rules(rules)
        neighbors = self.neighbor_selector.get_selection()
        board.neighborhood_func_indices = neighbors
        board.current_neighborhood = board.define_neighborhood(neighbors)

    def __init__(self):
        super().__init__()
        self.neighbor_selector = NeighborSelectorFrame(self)
        self.neighborhood_label = tk.Label(self, text='Neighborhood')
        self.apply_button = tk.Button(
                self, text='Apply',
                command=self.apply_callback
                )
        self.born_listbox = RuleListbox(self)
        self.born_label = tk.Label(self, text='Born')
        for i in board.born_ruleset:
            self.born_listbox.selection_set(i-1, last=None)
        self.survives_listbox = RuleListbox(self)
        self.survives_label = tk.Label(self, text='Survive')
        for i in board.survives_ruleset:
            self.survives_listbox.selection_set(i-1, last=None)

        self.neighborhood_label.grid(row=0, columnspan=3)
        self.neighbor_selector.grid(row=1, columnspan=3)
        self.born_label.grid(row=0, column=4)
        self.born_listbox.grid(row=1, column=4)
        self.survives_label.grid(row=0, column=5)
        self.survives_listbox.grid(row=1, column=5)
        self.apply_button.grid(row=2, columnspan=6, pady=4, sticky=tk.E+tk.W+tk.S)
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
        self.maxsize(self.winfo_reqwidth(), self.winfo_reqheight())
