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
        self.button = tk.Button(window, text="Debug cells", command=self.board.log_debug_cells)
        self.button.grid(row=20, column=2)
        self.button = tk.Button(window, text="Debug Pawns", command=self.board.log_debug_pawns)
        self.button.grid(row=20, column=3)

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
        self.cells = [[Cell(i, j) for j in range(8)] for i in range(8)]
        self.pawns = []
        self.draw_board()
        self.start_place_pawns()

    #EN checkers so 8*8 board and 3*3 rows of pawns
    def start_place_pawns(self):
        for j in range(self.col):
                if (j < 3): # 0-1-2
                    if (j % 2 == 0):
                        for i in range(self.row):
                            if (i % 2 == 0):
                                #Drawning : keep in mind pawn is not yet created 
                                #This id refers the object created by TkInter Canvas 
                                id = self.board.create_oval((i * self.x) + 5,(j * self.y) + 5,((i + 1) * self.x) - 5,((j + 1) * self.y) - 5,fill='white')
                                #Create a pawn 
                                pawn = Pawn('white', i, j, id)
                                self.cells[i][j].pawned = pawn
                                self.pawns.append(pawn)
                    else:
                        for i in range(self.row):
                            if (i % 2 != 0):
                                self.board.create_oval((i * self.x) + 5,(j * self.y) + 5,((i + 1) * self.x) - 5,((j + 1) * self.y) - 5,fill='white')
                                pawn = Pawn('white', i, j, id)
                                self.cells[i][j].pawned = pawn
                                self.pawns.append(pawn)
                elif( 5 <= j <= 7):
                    if (j % 2 != 0):
                        for i in range(self.row):
                            if (i % 2 == 0):
                                id = self.board.create_oval((i * self.x) + 5,(j * self.y) + 5,((i + 1) * self.x) - 5,((j + 1) * self.y) - 5,fill='black')
                                #Create a pawn 
                                pawn = Pawn('black', i, j, id)
                                self.cells[i][j].pawned = pawn
                                self.pawns.append(pawn)
                    else:
                        for i in range(self.row):
                            if (i % 2 != 0):
                                self.board.create_oval((i * self.x) + 5,(j * self.y) + 5,((i + 1) * self.x) - 5,((j + 1) * self.y) - 5,fill='black')
                                pawn = Pawn('black', i, j, id)
                                self.cells[i][j].pawned = pawn
                                self.pawns.append(pawn)


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

    #In GUI environnement it will print adresses so we will need __repr__ or __str__ in Cell/ whatever class
    def log_debug_cells(self):
        print(self.cells)
    
    def log_debug_pawns(self):
        print(self.pawns)

class Cell:
    def __init__(self, x, y):
        #coordinates
        self.x = x
        self.y = y
        self.free = True
        self.pawned = None #Will tell if there is a pawn at this pos or not 

    def __repr__(self):
        return f"Cell at ({self.x}, {self.y}), free: {self.free}"

class Pawn:
    def __init__(self, color, x ,y, id=None):
        self.color = color
        self.x = x
        self.y = y
        self.id = id #Imagine this is chess there are lots of two pieces and there is a notation of each piece 

    def __repr__(self):
        return f"Pawn at ({self.x}, {self.y}), color: {self.color}, id: {self.id}."

#Create the window and let it run until user quits 
root = tk.Tk()
my_window = MainWindow(root)
my_window.run()


