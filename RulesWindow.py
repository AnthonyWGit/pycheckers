import tkinter as tk
import RulesWindow as RulesWindow

class RulesWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Rules")
        rules = (
            "1. Each player starts with 8 * 2 pawns.\n"
            "2. Pawns can only move diagonally.\n"
            "3. Queens can move through the whole diagonal. \n"
            "4. Pawns can capture opponent's pawns by jumping over them. All 4 directions diagonaly allowed. \n"
            "5. The game ends when a player captures all opponent's pawns or when a draw is declared.\n"
        )
        self.label = tk.Label(self.window, text=rules, justify=tk.LEFT)
        self.label.pack(padx=10, pady=10)
