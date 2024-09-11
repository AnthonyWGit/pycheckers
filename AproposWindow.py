import tkinter as tk

class AproposWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Rules")
        aproposRules = "Using custom rules from childhood"
        aproposAuthor = "Made by Wetzstein Anthony. You are free to modify, distribute or copy this program."
        self.label = tk.Label(self.window, text=aproposRules, justify=tk.LEFT)
        self.label2 = tk.Label(self.window, text=aproposAuthor, justify=tk.LEFT)
        self.label.pack(padx=10, pady=10)
        self.label2.pack(padx=10, pady=10)