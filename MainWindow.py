import tkinter as tk
from RulesWindow import RulesWindow
from AproposWindow import AproposWindow
from Board import Board

class MainWindow:
    def __init__(self, window):
        self.window = window
        window.title("pyCheckers")
        self.main_frame = tk.Frame(window)
        self.board = Board(self.main_frame)
        self.turn_label = tk.Label(self.main_frame, text=f"")
        self.turn_label.grid(row=0, column=0, columnspan=2)
        self.player_color_turn = tk.Label(self.main_frame, text="Whites turn") 
        self.player_color_turn.grid(row=1, column=0, columnspan=2)
        self.instruction_label = tk.Label(self.main_frame, text="Choose a pawn to move") 
        self.instruction_label.grid(row=2, column=0, columnspan=2)
        self.additional_info_capture = tk.Label(self.main_frame, text="")
        self.additional_info_capture.grid(row=3, column=0, columnspan=2)
        self.board.canvas.grid(row = 4, column = 0, sticky = "nswe", columnspan= 2, rowspan= 1)
        self.board.canvas.config(highlightthickness=1, highlightbackground='white', relief='ridge', width=240, height=240) # a cell is 30*30 so 8*30
        self.button1 = tk.Button(self.main_frame, text="Debug cells", command=self.board.log_debug_cells)
        self.button1.grid(row=12, column=0, columnspan='1', rowspan='1', sticky="w")
        self.button2 = tk.Button(self.main_frame, text="Debug Pawns", command=self.board.log_debug_pawns,)
        self.button2.grid(row=12, column=1, columnspan='1', rowspan='1', sticky="e")
        self.buttonHardReset = tk.Button(self.main_frame, text="Reset")
        self.buttonHardReset.grid(row=13, column=0, sticky="nswe", columnspan=2)
        self.main_frame.config(highlightbackground='grey', highlightthickness='1', padx=10, pady=10)
        self.main_frame.grid(sticky='nswe')
        self.main_frame.pack()

        # Create menu
        self.menu = tk.Menu(window)
        window.config(menu=self.menu)
        self.rules_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Menu", menu=self.rules_menu)
        self.rules_menu.add_command(label="Show Rules", command=self.show_rules)
        self.rules_menu.add_command(label="About", command=self.show_apropos)
        self.replay_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Replay', menu=self.replay_menu)
        self.replay_menu.add_command(label='New')
        self.replay_menu.add_command(label='Load')
        # Center the window : separate function to pack calculations
        self.center_window()

    def center_window(self):
        #Get the window size when everything is packed
        self.window.update_idletasks()
        #Get H/W of tkinterwindow
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        #Get screen size
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        #Using calc values for proper geometry
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def show_rules(self):
        rules_window = RulesWindow(self.window)

    def show_apropos(self):
        apropos_window = AproposWindow(self.window)

    def run(self):
        self.window.mainloop()