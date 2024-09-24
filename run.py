import tkinter as tk
from MainWindow import MainWindow
from Game import Game

root = tk.Tk()
main_window = MainWindow(root)
game = Game(main_window)
main_window.run()
