import tkinter as tk

class mainWindow:
    def __init__(self, window):
        self.window = window
        window.title("pyCheckers")

    def run(self):
        self.window.mainloop()

#Create the window and let it run until user quits 
root = tk.Tk()
my_window = mainWindow(root)
my_window.run()


