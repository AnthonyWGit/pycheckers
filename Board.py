import tkinter as tk
from Cell import Cell
from Pawn import Pawn


class Board:
    def __init__(self, window):
        #bord is a Canvas widget from Tkinter class
        self.canvas = tk.Canvas(window, borderwidth=1)
        self.last_clicked_cell = None
        #Drawing the grid
        self.row = 8
        self.col = 8
        #x and y size of square
        self.x = 30
        self.y = 30
        self.cells = [[Cell(i, j, 'black' if (i+j)%2 == 0 else 'grey') for j in range(8)] for i in range(8)]
        self.pawns = []
        self.draw_board()
        self.start_place_pawns()

    #EN checkers so 8*8 board and 3*3 rows of pawns
    def start_place_pawns(self):
        for j in range(self.col):
                if (j < 3): # 0-1-2
                    if (j % 2 == 0):
                        for i in range(self.row):
                            if (i % 2 != 0):
                                #Drawning : keep in mind pawn is not yet created 
                                #This id refers the object created by TkInter Canvas 
                                id = self.canvas.create_oval((i * self.x) + 5,(j * self.y) + 5,((i + 1) * self.x) - 5,((j + 1) * self.y) - 5,fill='black')
                                #Create a pawn 
                                pawn = Pawn('black', i, j, id)
                                self.cells[i][j].pawned = pawn
                                self.pawns.append(pawn)
                                self.cells[i][j].free = False
                    else:
                        for i in range(self.row):
                            if (i % 2 == 0):
                                id = self.canvas.create_oval((i * self.x) + 5,(j * self.y) + 5,((i + 1) * self.x) - 5,((j + 1) * self.y) - 5,fill='black')
                                pawn = Pawn('black', i, j, id)
                                self.cells[i][j].pawned = pawn
                                self.pawns.append(pawn)
                                self.cells[i][j].free = False
                elif( 5 <= j <= 7):
                    if (j % 2 == 0):
                        for i in range(self.row):
                            if (i % 2 != 0):
                                id = self.canvas.create_oval((i * self.x) + 5,(j * self.y) + 5,((i + 1) * self.x) - 5,((j + 1) * self.y) - 5,fill='white')
                                #Create a pawn 
                                pawn = Pawn('white', i, j, id)
                                self.cells[i][j].pawned = pawn
                                self.pawns.append(pawn)
                                self.cells[i][j].free = False
                    else:
                        for i in range(self.row):
                            if (i % 2 == 0):
                                id = self.canvas.create_oval((i * self.x) + 5,(j * self.y) + 5,((i + 1) * self.x) - 5,((j + 1) * self.y) - 5,fill='white')
                                pawn = Pawn('white', i, j, id)
                                self.cells[i][j].pawned = pawn
                                self.pawns.append(pawn)
                                self.cells[i][j].free = False

    def draw_board(self):
        for j in range(self.col):
            if (j % 2 == 0):
                for i in range(self.row):
                    #pair number
                    if(i % 2 == 0):
                        #first two numbers for argument are coordinates at top left and rest on px after bottom right 
                        # https://web.archive.org/web/20181223164027/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_rectangle.html
                        self.canvas.create_rectangle(i * self.x,j * self.y,(i + 1) * self.x,(j + 1) * self.y,fill='black')
                    else:   
                        self.canvas.create_rectangle(i * self.x,j * self.y,(i + 1) * self.x,(j + 1) *self.y,fill='grey')
            else:
                for i in range(self.row):
                    #pair number
                    if(i % 2 == 0):
                        self.canvas.create_rectangle(i * self.x,j * self.y,(i + 1) * self.x,(j + 1) *self.y,fill='grey')
                    else:
                        self.canvas.create_rectangle(i * self.x,j * self.y,(i + 1) * self.x,(j + 1) *self.y,fill='black')
    
    #In GUI environnement it will print adresses so we will need __repr__ or __str__ in Cell/ whatever class
    def log_debug_cells(self):
        print(self.cells)
    
    def log_debug_pawns(self):
        print(self.pawns)

    def wipeAll(self):
        #clean all and reset inital state
        self.canvas.delete("all")
        self.cells = [[Cell(i, j, 'black' if (i+j)%2 == 0 else 'grey') for j in range(8)] for i in range(8)]
        self.pawns = []
        #Redraw
        self.draw_board()
        self.start_place_pawns()
