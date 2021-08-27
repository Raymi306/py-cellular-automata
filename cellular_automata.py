import tkinter as tk
import random
import time

class Gui(tk.Frame):

    __slots__ = ()
    SIDE_COLUMN_PADDING = 10
    BOTTOM_COLUMN_PADDING = 2
    canvas_color = "#bbbbbb"
    current_canvas_callback = -1
    toplevel_rules = None
    
    def __init__(self, parent, *args, **kwargs):
        
        super().__init__(parent)

        vcmd = self.register(self.entry_int_checker), '%S'
        
        self.master.title("Cellular automata - tkinter test")        
        #frames
        self.side_frame = tk.Frame(self, padx = self.SIDE_COLUMN_PADDING, pady = self.SIDE_COLUMN_PADDING)
        self.canvas_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self, pady = self.BOTTOM_COLUMN_PADDING)        
        self.side_frame.pack(side="left", fill="y")
        self.canvas_frame.pack(fill="both", expand="1")
        self.bottom_frame.pack(side="bottom")        

        #canvas frame
        self.canvas = tk.Canvas(self.canvas_frame, bg = self.canvas_color)
        self.canvas.pack(expand=1)
        
        #bottom frame
        self.clear_button = tk.Button(self.bottom_frame, text="Clear", command=None, padx=15)
        self.run_button = tk.Button(self.bottom_frame, text="Run", command=None, width=15, fg="white", bg="green", anchor="s")
        self.step_button = tk.Button(self.bottom_frame, text="Step", command=None)
        self.step_entry = tk.Entry(self.bottom_frame, width=5, justify="center", validate="key", vcmd=vcmd)
        self.randomize_button = tk.Button(self.bottom_frame, text="Randomize", command=None)
        self.clear_button.pack(side="left", padx=45)
        self.run_button.pack(side="left")
        self.step_button.pack(side="left")
        self.step_entry.pack(side="left", padx=4)
        self.randomize_button.pack(side="right", padx=15)
        #TODO change to spinboxes
        #left frame / settings        
        self.board_width_label = tk.Label(self.side_frame, text="Board Width", relief="ridge")
        self.board_width_entry = tk.Entry(self.side_frame, width=6, justify="center", validate="key", vcmd=vcmd)
        self.board_height_label = tk.Label(self.side_frame, text="Board Height", relief="ridge")
        self.board_height_entry = tk.Entry(self.side_frame, width=6, justify="center", validate="key", vcmd=vcmd)
        self.cell_width_label = tk.Label(self.side_frame, text="Cell Width", relief="ridge")
        self.cell_width_entry = tk.Entry(self.side_frame, width=4, justify="center", validate="key", vcmd=vcmd)
        self.cell_height_label = tk.Label(self.side_frame, text="Cell Height", relief="ridge")
        self.cell_height_entry = tk.Entry(self.side_frame, width=4, justify="center", validate="key", vcmd=vcmd)
        self.tickrate_label = tk.Label(self.side_frame, text="Tickrate", relief="ridge")
        self.tickrate_entry = tk.Entry(self.side_frame, width=4, justify="center", validate="key", vcmd=vcmd)
        self.tickrate_scale = tk.Scale(self.side_frame, from_=500, to=1, length=80, showvalue=0, sliderlength=15, bd=0)
        self.outline_bool = tk.IntVar() #in this scope due to struggle with toggle box
        self.outline_toggle_box = tk.Checkbutton(self.side_frame, text="Cell Outline", variable=self.outline_bool, relief="raised")
        self.cell_color_selector = tk.Menubutton(self.side_frame, text="Cell Colors", relief="raised")

        self.ccs_menu = tk.Menu(self.cell_color_selector, tearoff=0)
        self.ccs_menu.add_command(label="Blk")
        self.ccs_menu.add_command(label="Red")
        self.ccs_menu.add_command(label="Blu")
        self.ccs_menu.add_command(label="Grn")
        self.ccs_menu.add_command(label="Bkg")
        self.ccs_menu.add_command(label="Rbw")

        self.rules_button = tk.Button(self.side_frame, text="Rules")
        
        self.apply_settings_button = tk.Button(self.side_frame, text="Apply\nSettings", command=None, padx=self.SIDE_COLUMN_PADDING, pady=self.SIDE_COLUMN_PADDING)


        self.outline_bool.set(1)
        
        
        self.cell_color_selector["menu"]=self.ccs_menu        
        self.board_width_label.pack()
        self.board_width_entry.pack()
        self.board_height_label.pack()
        self.board_height_entry.pack()
        #self.board_color_label.pack()
        #self.board_color_entry.pack()
        self.cell_width_label.pack()
        self.cell_width_entry.pack()
        self.cell_height_label.pack()
        self.cell_height_entry.pack()
        #self.cell_color_label.pack()
        #self.cell_color_entry.pack()
        self.tickrate_label.pack()
        self.tickrate_entry.pack()
        self.tickrate_scale.pack(pady=3)
        self.outline_toggle_box.pack()
        self.cell_color_selector.pack(pady=3)
        self.rules_button.pack()
        self.apply_settings_button.pack(side="bottom")  #rename and move..?      
        
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


    def entry_int_checker(self, new_val):
        try:
            int(new_val)
            return True
        except:
            return False
        
        


class Cell(object):
    __slots__ = ('state', 'lifetime', 'previous_lifetime', 'tk_obj', 'neighbors', 'alive_neighbors', 'colors')
    
    def __init__(self, x1, y1, x2, y2, colors):        
        self.state = 0
        self.lifetime = 0
        self.previous_lifetime = 0
        self.tk_obj = gui.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[self.lifetime], outline="")
        self.neighbors = None
        self.alive_neighbors = 0
        self.colors = colors

    def __str__(self):
        return(f"\nstate:{self.state}\nlifetime:{self.lifetime}\nprevious_lifetime:{self.previous_lifetime}\ntk_obj_id:{self.tk_obj}\nnum_neighbors:{len(self.neighbors)}\n")

    def tick(self, rule):       
        self.state = rule(self.state, self.alive_neighbors)
        
        if self.state and self.lifetime <= 5:
            self.lifetime += 1
        elif not self.state:
            self.lifetime = 0        

    def toggle(self):
        self.previous_lifetime = self.lifetime
        if self.state:
            self.state = 0
            self.lifetime = 0            
        else:
            self.state = 1
            self.lifetime = 1            
        self.update_canvas()
            
    def check_neighbors(self):
        self.alive_neighbors = 0
        for neighbor in self.neighbors:
            if neighbor.state != 0:
                self.alive_neighbors += 1
        
    def update_canvas(self):   
        if gui.canvas.itemcget(self.tk_obj, 'fill') != self.colors[self.lifetime]:            
            gui.canvas.itemconfig(self.tk_obj, fill=(self.colors[self.lifetime]))
      

    def reset(self):
        self.previous_lifetime = self.lifetime
        self.state = 0        
        self.lifetime = 0
        self.update_canvas()



        

class Board(object):

    palettes = [['', 'black', 'black', 'black', 'black', 'black', 'black'],
            ['', '#ed2b08', '#af0808', '#8c0505', '#4f0505', '#280404', 'black'],
            ['', '#1200ff', '#2e0eba', '#28157c', '#211942', '#130a21', 'black'],
            ['', '#98ff11', '#54cc0a', '#229e06', '#18560a', '#0e3006', 'black'],
            ['', '#b2b1a4', '#b2b1a4', '#b2b1a4', '#b2b1a4', '#b2b1a4', '#b2b1a4'],
            ['', '#E70000', '#FF8C00', '#FFEF00', '#00811F', '#0044FF', '#760089']]    

    board_width = 640
    board_height = 480
    cell_width = 16
    cell_height = 16
    tickrate = 100
    timestep = 1
    
    max_x_pos = int(board_width / cell_width)
    max_y_pos = int(board_height / cell_height)
    total_cells = max_x_pos * max_y_pos
    cells = ()
    grid = ()
    is_running = False    

    def __init__(self):
        
        print(f"tickrate={self.tickrate}")
        self.rules = ({3}, {2, 3})
        self.current_rule = self.define_rules(self.rules)
        self.current_neighborhood = [0, 1, 2, 3, 4, 5, 6, 7]
        self.current_color = self.palettes[0]
        self.register_gui_callbacks()
        self.reset()
    
    def generate_cells(self):        
        cells = []
        if len(self.cells):
            for cell in self.cells:
                del(cell)
        index = 0
        neighbors = []
        for y in range(0, self.board_height, self.cell_height):
            for x in range(0, self.board_width, self.cell_width):
                neighbors_var = [] #very poorly named
                for i in self.current_neighborhood:
                    neighbors_var.append(self.neighbor_functions[i](self, index))               
                neighbors.append(tuple(neighbors_var))
                cells.append(Cell(x, y, x + self.cell_width, y + self.cell_height, self.current_color))
                index += 1
        for i, cell in enumerate(cells):
            cell.neighbors = [cells[u] for u in neighbors[i]]
        return tuple(cells)
        #print(self.cells[0].neighbors)

    def generate_grid(self):        
        grid = []
        color = "white"
        
        if gui.outline_bool.get():            
            state = "normal"
        else:
            state = "hidden"
            
        if len(self.grid):
            for line in self.grid:
                del(line)
                
        for y in range(0, self.board_height, self.cell_height):
            grid.append(gui.canvas.create_line(0, y, self.board_width, y, fill=color, state=state))

        for x in range(0, self.board_width, self.cell_width):
            grid.append(gui.canvas.create_line(x, 0, x, self.board_height, fill=color, state=state))

        return tuple(grid)

    def step(self):
        #timer = time.perf_counter()
        counter = self.timestep
        while counter:
            
            for cell in self.cells:
                cell.check_neighbors()
            for cell in self.cells:
                cell.tick(self.current_rule)
            counter -= 1
            
        for cell in self.cells:
            cell.update_canvas()
        #timer = int((time.perf_counter() - timer) * 1000)
        #print(timer)

    def run(self):
        self.step()
        gui.current_canvas_callback = gui.canvas.after(self.tickrate, self.run)

    def stop(self):
        self.is_running = False        
        gui.canvas.after_cancel(gui.current_canvas_callback)
        gui.run_button.config(bg = "green", text = "Run")

    def reset(self):
        gui.canvas.delete('all')
        self.max_x_pos = int(self.board_width / self.cell_width)
        self.max_y_pos = int(self.board_height / self.cell_height)
        self.total_cells = self.max_x_pos * self.max_y_pos
        print(f"{self.total_cells} cells")
        gui.update_canvas_dim(self.board_width, self.board_height)
        self.cells = self.generate_cells()
        self.grid = self.generate_grid()

#--------------------------------------------------------------------------------
    def get_nw(self, index, wrap=None):        
        default_case = index - self.max_x_pos - 1
        
        if index < self.max_x_pos and index % self.max_x_pos != 0: #top row exclude top left
            return default_case + self.total_cells
        elif index % self.max_x_pos == 0: #left col
            left_col_case = index - 1
            if left_col_case < 0: #top left...
               return self.total_cells - 1
            else:
                return left_col_case
        else:
            return default_case

    def get_ne(self, index, wrap=None):
        default_case = index - self.max_x_pos + 1
        
        if index < self.max_x_pos and index % self.max_x_pos != self.max_x_pos - 1: #exclude corner
            return default_case + self.total_cells
        elif index % self.max_x_pos == self.max_x_pos - 1:
            right_col_case = default_case - self.max_x_pos
            if right_col_case < 0:
                return self.total_cells + right_col_case
            else:
                return right_col_case
        else:
            return default_case

    def get_sw(self, index, wrap=None):
        default_case = index + self.max_x_pos - 1
        
        if index + self.max_x_pos >= self.total_cells and index % self.max_x_pos != 0: #bot row exclude bot left
            return default_case - self.total_cells
        elif index % self.max_x_pos == 0: #left col
            left_col_case = default_case + self.max_x_pos            
            if left_col_case >= self.total_cells:
                return self.max_x_pos - 1
            else:
                return left_col_case
        else:
            return default_case        

    def get_se(self, index, wrap=None):
        default_case = index + self.max_x_pos + 1
        
        if index + self.max_x_pos >= self.total_cells and index % self.max_x_pos != self.max_x_pos - 1: #bot row exclude bot right
            return default_case - self.total_cells
        elif index % self.max_x_pos == self.max_x_pos - 1: #right col
            right_col_case = default_case - self.max_x_pos            
            if right_col_case >= self.total_cells:
                return 0
            else:
                return right_col_case
        else:
            return default_case
        
    def get_n(self, index, wrap=None):
        if index >= self.max_x_pos:
            return index - self.max_x_pos
        else:
            return index + self.total_cells - self.max_x_pos
        
    def get_w(self, index, wrap=None):
        if index - 1 >= 0\
        and (index - 1) % self.max_x_pos != self.max_x_pos - 1:
            return index - 1
        else:
            return index + self.max_x_pos - 1
        
    def get_e(self, index, wrap=None):
        if (index + 1) % self.max_x_pos != 0\
           and index + 1 < self.total_cells:
            return index + 1
        else:
            return index - self.max_x_pos + 1
        
    def get_s(self, index, wrap=None):
        if (index + self.max_x_pos) < self.total_cells:
            return index + self.max_x_pos
        else:
            return index - self.total_cells + self.max_x_pos

    neighbor_functions = [get_nw, get_n, get_ne, get_w, get_e, get_sw, get_s, get_se]

    def define_neighborhood(self, neighborhood_func_indices, wrap=None):
        def neighborhood(self, index):
            for i in neighborhood_func_indices:
                self.neighbor_functions[i](index)
        return neighborhood
    
    def define_rules(self, bs_tuple):
        birth_set = bs_tuple[0]
        survive_set = bs_tuple[1]
        def rule(status, alive_neighbors):
            if status:
                if alive_neighbors not in survive_set:
                    return 0
            elif alive_neighbors in birth_set:
                return 1
            return status
        return rule
    
#---------------------------------------------------------------------------------------------
    def register_gui_callbacks(self):

        def canvas_click_handler(event):
        #print(f"event: {event}")        
            tk_obj_id = event.widget.find_closest(event.x, event.y)[0]
            #print(f"tk_obj_id clicked: {tk_obj_id}")
            for cell in self.cells:
                if cell.tk_obj == tk_obj_id:
                    
                    cell.toggle()
                    #print(cell)
                    break

        def run_button_handler():
            set_timestep()
            if self.is_running:
                self.stop()
            else:
                self.is_running = True
                gui.run_button.config(bg = "red", text = "Stop")
                self.run()

        def step_button_handler():
            set_timestep()            
            self.step()

        def set_timestep(*args):
            self.timestep = int(gui.step_entry.get())
                
        def clear_button_handler():
            for cell in self.cells:
                cell.reset()

        def randomize_button_handler():
            lottery = random.sample(self.cells, random.randint(1, (self.total_cells - 1)))
            for cell in lottery:
                cell.toggle()            

        def apply_settings_button_handler():                                      
            self.stop()
            try:
                new_width = int(gui.board_width_entry.get())
                new_height = int(gui.board_height_entry.get())
                #print(new_width, new_height)
                if new_width < 50:
                    new_width = 50
                if new_width > 1280:
                    new_width = 1280
                if new_height < 50:
                    new_height = 50
                if new_height > 1024:
                    new_height = 1024
                self.board_width = new_width
                self.board_height = new_height            
            except ValueError:
                pass #replace with old values

            try:
                new_cell_w = int(gui.cell_width_entry.get())
                new_cell_h = int(gui.cell_height_entry.get())
                #print(new_cell_w, new_cell_h)
                if new_cell_w < 1:
                    new_cell_w = 1
                if new_cell_w > 1280:
                    new_cell_w = 1280
                if new_cell_h < 1:
                    new_cell_h = 1
                if new_cell_h > 1024:
                    new_cell_h = 1024
                self.cell_width = new_cell_w
                self.cell_height = new_cell_h
            except ValueError:
                pass

            gui.board_width_entry.delete(0, tk.END)
            gui.board_height_entry.delete(0, tk.END)
            gui.cell_width_entry.delete(0, tk.END)
            gui.cell_height_entry.delete(0, tk.END)
            gui.board_width_entry.insert(0, self.board_width)
            gui.board_height_entry.insert(0, self.board_height)
            gui.cell_width_entry.insert(0, self.cell_width)
            gui.cell_height_entry.insert(0, self.cell_height)
            self.reset()         

        def tickrate_scale_handler(e):
            
            #redundant code
            try:
                new_tr = int(e)
                if new_tr < 1:
                    new_tr = 1
                if new_tr > 9999:
                    new_tr = 9999
                self.tickrate = new_tr
            except ValueError:
                pass

            
            gui.tickrate_entry.delete(0, tk.END)
            gui.tickrate_entry.insert(0, self.tickrate)

        def tickrate_enter_handler(e):
            
            try:
                new_tr = int(e.widget.get())
                if new_tr < 1:
                    new_tr = 1
                if new_tr > 9999:
                    new_tr = 9999
                self.tickrate= new_tr
            except ValueError:
                pass
            #gui.tickrate_scale.set(self.tickrate)

        def outline_toggle_box_handler():
            if gui.outline_bool.get():
                for line in self.grid:
                    gui.canvas.itemconfigure(line, state="normal")
            else:
                for line in self.grid:
                    gui.canvas.itemconfigure(line, state="hidden")
            

        def ccs_menu_handler(i):
            for cell in self.cells:
                self.current_color = self.palettes[i]
                cell.colors = self.palettes[i]
                cell.update_canvas()

        def rules_button():

            #MOORE = 0
            #MOOREW = 1
            #NEUMANN = 2
            #NEUMANNW = 3

            def apply_callback():
                
                b = birthe.get().split()
                for i, n in enumerate(b):
                    b[i] = int(n)
                s = survivee.get().split()
                for i, n in enumerate(s):
                    s[i] = int(n)
                l = lb.curselection()[0]
                print(b, s, l)

                self.rules = (set(b), set(s))                
                self.current_neighborhood = self.neighborhoods[l]
                self.current_rule = self.define_rules(self.rules)
                self.reset()
            
            if(gui.toplevel_rules):
                gui.toplevel_rules.destroy()
            x = gui.master.winfo_x()
            y = gui.master.winfo_y()
            xoff = gui.master.winfo_width()
            yoff = gui.master.winfo_height()            
            
            popup = tk.Toplevel()
            gui.toplevel_rules = popup
            
            neighbor_selector = tk.Frame(popup)
            
            row1 = tk.Frame(neighbor_selector)
            row2 = tk.Frame(neighbor_selector)
            row3 = tk.Frame(neighbor_selector)
            neighbor_wrap_toggle = tk.Checkbutton(neighbor_selector, text="Wrap")
            apply_button = tk.Button(popup, text='Apply')
            
            neighbor_color = 'yellow'
            center_color = 'gray'
            n_width = 4
            n_height = 2
            n_pack_options = {'side':'left', 'padx':2, 'pady':2}

            box_norm_color = 'gray'
        
            nwn = tk.Label(row1, bg=box_norm_color, width=n_width, height=n_height, relief='sunken')
            nn = tk.Label(row1, bg=box_norm_color, width=n_width, height=n_height, relief='sunken')
            nen = tk.Label(row1, bg=box_norm_color, width=n_width, height=n_height, relief='sunken')
            wn = tk.Label(row2, bg=box_norm_color, width=n_width, height=n_height, relief='sunken')
            center = tk.Label(row2, bg='brown', width=n_width, height=n_height)
            en = tk.Label(row2, bg=box_norm_color, width=n_width, height=n_height, relief='sunken')
            swn = tk.Label(row3, bg=box_norm_color, width=n_width, height=n_height, relief='sunken')
            sn = tk.Label(row3, bg=box_norm_color, width=n_width, height=n_height, relief='sunken')
            sen = tk.Label(row3, bg=box_norm_color, width=n_width, height=n_height, relief='sunken')
            neighbors_arr = [nwn, nn, nen, wn, en, swn, sn, sen]

            
            for i in self.current_neighborhood:
                neighbors_arr[i].config(state='active')

            def neighbor_box_clickhandler(label):
                state = label.cget('state')
                if state == 'normal':
                    label.config(state='active')
                else:
                    label.config(state='normal')

            for n in neighbors_arr:
                n.config(activebackground='black')
                def nbox_click_lambda(l):
                    return lambda e : neighbor_box_clickhandler(l)
                n.bind("<Button-1>", nbox_click_lambda(n))

            rule_selector = tk.Frame(popup)
            
            rborn = tk.Listbox(rule_selector, selectmode='multiple', exportselection=False, width=4, height=8, activestyle='none')
            rborn.insert('end', ' 1')
            rborn.insert('end', ' 2')
            rborn.insert('end', ' 3')
            rborn.insert('end', ' 4')
            rborn.insert('end', ' 5')
            rborn.insert('end', ' 6')
            rborn.insert('end', ' 7')
            rborn.insert('end', ' 8')
            for i in self.rules[0]:
                rborn.selection_set(i-1, last=None)

            rsurvives = tk.Listbox(rule_selector, selectmode='multiple', exportselection=False, width=4, height=8, activestyle='none')
            rsurvives.insert('end', ' 1')
            rsurvives.insert('end', ' 2')
            rsurvives.insert('end', ' 3')
            rsurvives.insert('end', ' 4')
            rsurvives.insert('end', ' 5')
            rsurvives.insert('end', ' 6')
            rsurvives.insert('end', ' 7')
            rsurvives.insert('end', ' 8')
            for i in self.rules[1]:
                rsurvives.selection_set(i-1, last=None)

            neighbor_selector.pack(side='left', anchor='nw')
            rule_selector.pack(side='left', anchor='nw', padx=10)
            rborn.pack(side='left')
            rsurvives.pack(side='left')
            row1.pack()
            row2.pack()
            row3.pack()
            neighbor_wrap_toggle.pack()
            apply_button.pack()
            nwn.pack(n_pack_options)
            nn.pack(n_pack_options)
            nen.pack(n_pack_options)
            wn.pack(n_pack_options)
            center.pack(n_pack_options)
            en.pack(n_pack_options)
            swn.pack(n_pack_options)
            sn.pack(n_pack_options)
            sen.pack(n_pack_options)
            
            def button_command():
                self.current_neighborhood = []
                for i in range(8):
                    if neighbors_arr[i].cget('state') == 'active':
                        print(str(i))
                        self.current_neighborhood.append(i)
                self.reset()

                born = []
                survives = []

                for i in rborn.curselection():
                    born.append(i + 1)

                for i in rsurvives.curselection():
                    survives.append(i + 1)

                born = set(born)
                survives = set(survives)

                print(born, survives)
                self.rules = (born, survives)
                self.current_rule = self.define_rules(self.rules)
                    

            apply_button.configure(command=button_command)            
        
        gui.board_width_entry.insert(0, self.board_width)
        gui.board_height_entry.insert(0, self.board_height)
        gui.cell_width_entry.insert(0, self.cell_width)
        gui.cell_height_entry.insert(0, self.cell_height)
        gui.tickrate_entry.insert(0, self.tickrate)
        gui.tickrate_scale.set(self.tickrate)
        
        gui.canvas.bind("<Button-1>", canvas_click_handler)
        gui.step_button.configure(command=step_button_handler)
        gui.step_entry.insert(0, self.timestep)
        gui.step_entry.bind("<Return>", set_timestep)
        gui.run_button.configure(command=run_button_handler)
        gui.clear_button.configure(command=clear_button_handler)
        gui.randomize_button.configure(command=randomize_button_handler)
        gui.apply_settings_button.configure(command=apply_settings_button_handler)
        gui.tickrate_scale.configure(command=tickrate_scale_handler)
        gui.tickrate_entry.bind("<Return>", tickrate_enter_handler)
        gui.outline_toggle_box.configure(command=outline_toggle_box_handler)        

        #num_ccs_menu_items = gui.ccs_menu.index("last") + 1
        
        for i in range(gui.ccs_menu.index("last") + 1):
            def ccs_menu_lambda(x):
                return lambda: ccs_menu_handler(x)            
            gui.ccs_menu.entryconfigure(i, command=ccs_menu_lambda(i))

        gui.rules_button.configure(command=rules_button)
#---------------------------------------------------------------------------------------------

root = tk.Tk()
gui = Gui(root)
board = Board()
root.mainloop()
