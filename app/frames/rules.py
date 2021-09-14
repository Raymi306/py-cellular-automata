import tkinter as tk


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
    def __init__(self, parent):
        super().__init__(parent)
        self.row1 = tk.Frame(self)
        self.nwn = NeighborSelectorBox(self)
        self.nn = NeighborSelectorBox(self)
        self.nen = NeighborSelectorBox(self)
        self.row2 = tk.Frame(self)
        self.wn = NeighborSelectorBox(self)
        self.center = NeighborSelectorBox(self, bg='brown')
        self.en = NeighborSelectorBox(self)
        self.row3 = tk.Frame(self)
        self.swn = NeighborSelectorBox(self)
        self.sn = NeighborSelectorBox(self)
        self.sen = NeighborSelectorBox(self)
        self.neighbor_wrap_toggle = tk.Checkbutton(self, text='Wrap')

        self.neighbor_selectors = [
                self.nwn, self.nn, self.nen,
                self.wn, self.en,
                self.swn, self.sn, self.sen
                ]

        for widget in self.neighbors_selectors:
            widget.bind('<Button-1>', widget.click_handler)

        _selectors = self.neighbor_selectors[:]
        _selectors.insert(4, self.center)  # put center in between wn and en

        for widget in _selectors:
            widget.pack(side='left', padx=2, pady=2)

        _rows = (self.row1, self.row2, self.row3)

        for widget in _rows:
            widget.pack()


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


class RulesPopup(tk.TopLevel):
    def __init__(self, parent):
        # intent of bare try-except is to avoid duplicates w/o singleton
        # might not be needed
        try:
            self.destroy()
        except:
            pass
        super().__init__(parent)
        self.neighbor_selector = NeighborSelectorFrame(self)
        self.apply_button = tk.Button(self, text='Apply')
        self.born_listbox = RuleListbox(self)
        self.survives_listbox = RuleListbox(self)

        self.neighbor_selector.pack(side='left', anchor='nw')
        self.rule_selector.pack(side='left', anchor='nw', padx=10)
        self.born_listbox.pack(side='left')
        self.survives_listbox.pack(side='left')
        self.apply_button.pack()  # TODO no apply hook
