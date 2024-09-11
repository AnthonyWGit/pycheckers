import tkinter as tk
from RulesWindow import RulesWindow
from AproposWindow import AproposWindow
from Board import Board


class MainWindow:
    def __init__(self, window):
        self.window = window
        window.title("pyCheckers")
        self.board = Board(window)
        self.turn_label = tk.Label(window, text=f"")
        self.turn_label.grid(row=0, column=0)
        self.player_color_turn = tk.Label(window, text="Whites turn") 
        self.player_color_turn.grid(row=1, column=0)
        self.instruction_label = tk.Label(window, text="Choose a pawn to move") 
        self.instruction_label.grid(row=2, column=0)
        self.additional_info_capture = tk.Label(window, text="")
        self.additional_info_capture.grid(row=3, column=0)
        self.button = tk.Button(window, text="Debug cells", command=self.board.log_debug_cells)
        self.button.grid(row=12, column=0)
        self.button = tk.Button(window, text="Debug Pawns", command=self.board.log_debug_pawns)
        self.button.grid(row=12, column=1)
        # Create menu
        self.menu = tk.Menu(window)
        window.config(menu=self.menu)
        self.rules_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Menu", menu=self.rules_menu)
        self.rules_menu.add_command(label="Show Rules", command=self.show_rules)
        self.rules_menu.add_command(label="About", command=self.show_apropos)
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

