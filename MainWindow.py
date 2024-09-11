import tkinter as tk
from Board import Board


class MainWindow:
    def __init__(self, window):
        self.window = window
        #Create window at the center of screen
        window_height = 600
        window_width = 600
        screen_height = window.winfo_screenheight()
        screen_width = window.winfo_screenwidth()
        #center of screen
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        window.title("pyCheckers")
        window.geometry(f'{window_height}x{window_width}+{center_x}+{center_y}')
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

