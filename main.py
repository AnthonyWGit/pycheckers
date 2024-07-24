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
        self.turn_label = tk.Label(window, text=f"")
        self.turn_label.grid(row=0, column=0)
        self.player_color_turn = tk.Label(window, text="Whites turn") 
        self.player_color_turn.grid(row=1, column=0)
        self.instruction_label = tk.Label(window, text="Choose a pawn to move") 
        self.instruction_label.grid(row=2, column=0)
        self.button = tk.Button(window, text="Debug cells", command=self.board.log_debug_cells)
        self.button.grid(row=11, column=0)
        self.button = tk.Button(window, text="Debug Pawns", command=self.board.log_debug_pawns)
        self.button.grid(row=11, column=1)

class Board:
    def __init__(self, window):
        #bord is a Canvas widget from Tkinter class
        self.canvas = tk.Canvas(window, borderwidth=1)
        self.window = window
        self.last_clicked_cell = None
        #Drawing the grid
        self.canvas.grid(row = 3, column = 0, sticky = "ew", columnspan= 8, rowspan= 8)
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

class Cell:
    def __init__(self, x, y, color):
        #coordinates
        self.x = x
        self.y = y
        self.free = True
        self.pawned = None #Will tell if there is a pawn at this pos or not
        self.color = color

    def __repr__(self):
        return f"Cell at ({self.x}, {self.y}), free: {self.free}, pawn : {self.pawned}, color {self.color}"

class Pawn:
    def __init__(self, color, x ,y, id=None):
        self.color = color
        self.x = x
        self.y = y
        self.id = id #Imagine this is chess there are lots of two pieces and there is a notation of each piece 

    def moving_forward(self): #Not complete and not functional, the idea is to retrieve where user clicks and move whithe to top of board 
        #and blacks bot
        if (self.color == "white"):
            x = x - 1
            y = y - 1
        
        if (self.color == "black"):
            x = x + 1
            y = y + 1
            
    def __repr__(self):
        return f"Pawn at ({self.x}, {self.y}), color: {self.color}, id: {self.id}."

class Game(MainWindow):
    def __init__(self, window):
        super().__init__(window)  # Call the constructor of MainWindow
        self.waiting = True
        self.board.canvas.bind("<Button-1>", self.on_click)  # Bind left mouse click event
        self.pawn_current_pos = None
        self.pawn_new_pos = None
        self.selected_pawn = None
        self.last_clicked_cell = None
        self.turn = 0
        self.turn_color = ''
        self.turn_color_set()
    
    def run(self):
        self.window.mainloop()

    def turn_color_set(self):
        if self.turn % 2 == 0:
            self.turn_color = 'white'
            self.turn_label.config(text=f'Turn {self.turn}')
        else:
            self.turn_color = 'black'

    def select_pawn(self):
        #when Whites turn
        if (self.turn % 2 == 0):
            print(self.turn)
            #change label anouncing player turn 
            print(self.last_clicked_cell, 'fzerze')
            if (self.last_clicked_cell.free == False and self.last_clicked_cell.pawned.color == 'white'):
                print('b')
                self.instruction_label.config(text="Choose where you want your pawn to go")
                self.pawn_current_pos = self.last_clicked_cell
                self.selected_pawn = self.pawn_current_pos.pawned
                return True
            else:
                print('a')
        else:
            if (self.last_clicked_cell.free == False and self.last_clicked_cell.pawned.color == 'black'):
                print('c')
                self.instruction_label.config(text="Choose where you want your pawn to go")
                self.pawn_current_pos = self.last_clicked_cell
                self.selected_pawn = self.pawn_current_pos.pawned
                return True
            else:
                print('d')

        # get x and y pos in the canvas 
    def on_click(self, event):
        # remove the whole division // and you will get the position in pixels where you click ! 
        # using floor division so no we get an integer and not a float  
        cell_x = event.x // self.board.x 
        cell_y = event.y // self.board.y 
        # Now you can use these coordinates to move the pawn
        clicked_cell = self.board.cells[cell_x][cell_y]
        print(f"BEGIN ONCLICK --------------- Clicked on cell ({cell_x}, {cell_y},{clicked_cell}) Turn : {self.turn}")
        print(f'ALL CELLS {self.board.cells} /$$$$$ Clicked_cell var : {clicked_cell}')
        self.last_clicked_cell = clicked_cell
        
        if self.selected_pawn == None:
            if self.select_pawn() == True:
                print(f'Selected Pawn : {self.selected_pawn}')
                return
            
        if (self.selected_pawn != None):
            print(f'Is INSTANCE SLECTED : {self.selected_pawn} TARGET : {self.last_clicked_cell}')
            if self.movement_is_valid() == True:
                # Get the old cell
                old_cell = self.board.cells[self.pawn_current_pos.x][self.pawn_current_pos.y]
                # Update the old cell
                old_cell.free = True
                old_cell.pawned = None
                print(f'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD {self.board.cells} DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
                # Update the pawn's position --> BROKEN they erase the coordinates of the cell
                self.pawn_current_pos.x = self.pawn_new_pos.x
                self.pawn_current_pos.y = self.pawn_new_pos.y
                # Get the new cell
                print(f'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP{self.board.cells} DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
                new_cell = self.board.cells[self.pawn_current_pos.x][self.pawn_current_pos.y]
                # Update the new cell
                new_cell.free = False
                new_cell.pawned = self.selected_pawn

                self.selected_pawn.x = self.pawn_current_pos.x
                self.selected_pawn.y = self.pawn_current_pos.y
                self.move_pawn(self.selected_pawn, self.pawn_current_pos.x, self.pawn_current_pos.y)
                
                print(f'graphic movement {self.selected_pawn}')

                #when everything is good increase turn count and clean values
                self.turn += 1
                self.turn_color_set()
                self.turn_label.config(text=f'Turn {self.turn}')
                self.instruction_label.config(text=f'Choose a pawn to move')
                self.reset_values()


    def movement_is_valid(self):
        #check if white movement is correct
        print(f'ee RTT {self.last_clicked_cell} ////// {self.pawn_current_pos}')
        if self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'white':
            newX = abs(self.last_clicked_cell.x - self.pawn_current_pos.x)
            newY = abs(self.last_clicked_cell.y - self.pawn_current_pos.y)
            print(newX, newY, self.last_clicked_cell, self.pawn_current_pos)
            if newX == 1 and newY == 1:  # Check if the absolute difference is 1 because queen will be able to go  backwards
                self.pawn_new_pos = self.last_clicked_cell
                print(f'validated move, Pawn new pos : {self.pawn_new_pos}')
                self.player_color_turn.config(text='Blacks turn')
                return True
        elif self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'black':
            print('NEED TO SEE THIS PRINTTT')
            newX = abs(self.last_clicked_cell.x - self.pawn_current_pos.x)
            newY = abs(self.last_clicked_cell.y - self.pawn_current_pos.y)
            print(newX, newY)
            if newX == 1 and newY == 1:  # Check if the absolute difference is 1 because queen will be able to go backwards
                self.pawn_new_pos = self.last_clicked_cell
                print(f'validated move, Pawn new pos : {self.pawn_new_pos}')
                self.player_color_turn.config(text='Whites turn')
                return True
        return False
    
    def move_pawn(self, pawn, new_x, new_y):
        # Calculate the new coordinates for the pawn
        new_coords = (new_x * self.board.x + 5, new_y * self.board.y + 5,
                    (new_x + 1) * self.board.x - 5, (new_y + 1) * self.board.y - 5)
        # Use the coords method to update the pawn's position on the canvas
        self.board.canvas.coords(pawn.id, new_coords)

    def reset_values(self):
        self.pawn_current_pos = None
        self.pawn_new_pos = None
        self.last_clicked_cell = None
        self.selected_pawn = None

#Create the window and let it run until user quits 
root = tk.Tk()
my_game = Game(root)
my_game.run()

