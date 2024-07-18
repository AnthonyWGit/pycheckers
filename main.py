import tkinter as tk

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

    def run(self):
        self.window.mainloop()

class Board:
    def __init__(self, window):
        #bord is a Canvas widget from Tkinter class
        self.board = tk.Canvas(window, borderwidth=1)
        #Drawing the grid
        self.board.grid(row = 1, column = 0, sticky = "ew", columnspan= 8, rowspan= 8)
        self.row = 8
        self.col = 8
        self.x = 30
        self.y = 30
        self.draw_board()

    def start_place_pawns(self):
        print('Hi')

    def draw_board(self):
        for j in range(self.col):
            if (j % 2 == 0):
                for i in range(self.row):
                    #pair number
                    if(i % 2 == 0):
                        #first two numbers for argument are coordinates at top left and rest on px after bottom right 
                        # https://web.archive.org/web/20181223164027/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_rectangle.html
                        self.board.create_rectangle(i * self.x,j * self.y,(i + 1) * self.x,(j + 1) * self.y,fill='black')
                    else:   
                        self.board.create_rectangle(i * self.x,j * self.y,(i + 1) * self.x,(j + 1) *self.y,fill='white')
            else:
                for i in range(self.row):
                    #pair number
                    if(i % 2 == 0):
                        self.board.create_rectangle(i * self.x,j * self.y,(i + 1) * self.x,(j + 1) *self.y,fill='white')
                    else:
                        self.board.create_rectangle(i * self.x,j * self.y,(i + 1) * self.x,(j + 1) *self.y,fill='black')

class Cell:
    def __init__(self):
        #coordinates
        self.x = x
        self.y = y
        self.free = True
class Pawn:
    def __init__(self):
        self.pox = pox

#Create the window and let it run until user quits 
root = tk.Tk()
my_window = MainWindow(root)
my_window.run()


