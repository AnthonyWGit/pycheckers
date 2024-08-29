import tkinter as tk
from MainWindow import MainWindow
from Cell import Cell
from Board import Board
from Pawn import Pawn

class Game(MainWindow):
    def __init__(self, window):
        super().__init__(window)  # Call the constructor of MainWindow
        self.waiting = True
        self.board.canvas.bind("<Button-1>", self.on_click)  # Bind left mouse click event
        self.pawn_current_pos = None
        self.pawn_new_pos = None
        self.selected_pawn = None
        self.last_clicked_cell = None
        self.turn = 1
        self.turn_color = ''
        self.turn_color_set()
    
    def run(self):
        self.window.mainloop()

    def turn_color_set(self):
        if self.turn % 2 == 0:
            self.turn_color = 'black'
            self.turn_label.config(text=f'Turn {self.turn}')
        else:
            self.turn_color = 'white'
            self.turn_label.config(text=f'Turn {self.turn}')

    def turn_switch(self):
        self.turn += 1
        self.turn_color_set()
        self.turn_label.config(text=f'Turn {self.turn}')
        self.instruction_label.config(text=f'Choose a pawn to move')
        self.reset_values()

    def select_pawn(self):
        #when Whites turn
        if (self.turn % 2 != 0):
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
            # In this if a pawn is already select : first we check if the last clicked cell is the same so the user can cancel his choice
            if (self.selected_pawn.x == self.last_clicked_cell.x) & (self.selected_pawn.y == self.last_clicked_cell.y):
                self.reset_values()
                self.instruction_label.config(text=f'Choose a pawn to move')
                print(f'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++JIJJI+++++++')
                return
            if self.movement_is_valid() == True or self.capture_pawn() == True:
                # Get the old cell
                old_cell = self.board.cells[self.pawn_current_pos.x][self.pawn_current_pos.y]
                # Update the old cell
                old_cell.free = True
                old_cell.pawned = None
                print(f'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD {self.board.cells} DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
                #selected pawn getting the same coords as the last clicked cell 
                self.selected_pawn.x = self.last_clicked_cell.x
                self.selected_pawn.y = self.last_clicked_cell.y
                # Get the new cell
                print(f'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP{self.board.cells} DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
                # Get the new cell
                new_cell = self.board.cells[self.last_clicked_cell.x][self.last_clicked_cell.y]
                # Update the new cell
                new_cell.free = False
                new_cell.pawned = self.selected_pawn
                self.move_pawn(self.selected_pawn, self.selected_pawn.x, self.selected_pawn.y)
                print(f'graphic movement {self.selected_pawn}')
                #check promotions
                self.promote_pawn()
                #when everything is good increase turn count and clean values
                self.turn_switch()


    def movement_is_valid(self):
        #check if white movement is correct
        print(f'ee RTT {self.last_clicked_cell} ////// {self.pawn_current_pos}')
        if self.selected_pawn.type == 'pawn':
            if self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'white':
                newX = self.last_clicked_cell.x - self.pawn_current_pos.x
                newY = self.last_clicked_cell.y - self.pawn_current_pos.y
                print(newX, newY, self.last_clicked_cell, self.pawn_current_pos)
                if newX == -1 and newY == -1 or newX == 1 and newY == -1:  # No absolute because we are using pawn movvement (standard)
                    self.pawn_new_pos = self.last_clicked_cell
                    print(f'validated move, Pawn new pos : {self.pawn_new_pos}')
                    self.player_color_turn.config(text='Blacks turn')
                    return True
            elif self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'black':
                print('NEED TO SEE THIS PRINTTT')
                newX = self.last_clicked_cell.x - self.pawn_current_pos.x
                newY = self.last_clicked_cell.y - self.pawn_current_pos.y
                print(newX, newY)
                if newX == -1 and newY == 1 or newX == 1 and newY == 1:  #  No absolute because we are using pawn movvement (standard)
                    self.pawn_new_pos = self.last_clicked_cell
                    print(f'validated move, Pawn new pos : {self.pawn_new_pos}')
                    self.player_color_turn.config(text='Whites turn')
                    return True
            return False
        elif self.selected_pawn.type == 'queen':
            newX = self.last_clicked_cell.x - self.pawn_current_pos.x
            newY = self.last_clicked_cell.y - self.pawn_current_pos.y
            if self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'white':
                print(newX, newY, self.last_clicked_cell, self.pawn_current_pos)
                if self.last_clicked_cell.color == 'grey' and self.movement_direction(newX, newY) != None:  # Check if the absolute difference is 1 because queen will be able to go  backwards
                    self.pawn_new_pos = self.last_clicked_cell
                    print(f'validated move, Pawn new pos : {self.pawn_new_pos}')
                    self.player_color_turn.config(text='Blacks turn')
                    return True
            elif self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'black':
                print('NEED TO SEE THIS PRINTTT')
                print(newX, newY)
                if self.last_clicked_cell.color == 'grey' and self.movement_direction(newX, newY) != None:  # Check if the absolute difference is 1 because queen will be able to go backwards
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

    def capture_pawn(self):
        if self.last_clicked_cell.free == True:
            newX = self.last_clicked_cell.x - self.pawn_current_pos.x
            newY = self.last_clicked_cell.y - self.pawn_current_pos.y
            if self.last_clicked_cell.color == 'grey' and self.turn_color == 'white':
                if newX == -2 and newY == -2:  #Up left movement from whites 
                    midX = self.last_clicked_cell.x + 1
                    midY = self.last_clicked_cell.y + 1
                    if self.board.cells[midX][midY].free != True:
                        self.remove_pawn_from_board(midX, midY)
                        self.player_color_turn.config(text='Blacks turn')
                        return True
                elif newX == 2 and newY == -2:  #Up right movement from whites
                    midX = self.last_clicked_cell.x - 1
                    midY = self.last_clicked_cell.y + 1
                    if self.board.cells[midX][midY].free != True:
                        self.remove_pawn_from_board(midX, midY)
                        self.player_color_turn.config(text='Blacks turn')
                        return True
            if self.last_clicked_cell.color == 'grey' and self.turn_color == 'black':
                if newX == -2 and newY == 2:  #down left movement from blacks
                    midX = self.last_clicked_cell.x + 1
                    midY = self.last_clicked_cell.y - 1
                    if self.board.cells[midX][midY].free != True:
                        self.remove_pawn_from_board(midX, midY)
                        self.player_color_turn.config(text='Whites turn')
                        return True
                elif newX == 2 and newY == 2:  #Down right movement from blacks
                    midX = self.last_clicked_cell.x - 1
                    midY = self.last_clicked_cell.y - 1
                    if self.board.cells[midX][midY].free != True:
                        self.remove_pawn_from_board(midX, midY)
                        self.player_color_turn.config(text='Whites turn')
                        return True
        return False

        #check if white movement is correct
        # if self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'white':
        #     newX = self.last_clicked_cell.x - self.pawn_current_pos.x
        #     newY = self.last_clicked_cell.y - self.pawn_current_pos.y
        #     if newX == -2 and newY == -2:  #Up left movement from whites 
        #         midX = self.last_clicked_cell.x + 1
        #         midY = self.last_clicked_cell.y + 1
        #         if self.board.cells[midX][midY].free != True:
        #             self.remove_pawn_from_board(midX, midY)
        #             self.player_color_turn.config(text='Blacks turn')
        #             return True
        #     elif newX == 2 and newY == -2:  #Up right movement from whites
        #         midX = self.last_clicked_cell.x - 1
        #         midY = self.last_clicked_cell.y + 1
        #         if self.board.cells[midX][midY].free != True:
        #             self.remove_pawn_from_board(midX, midY)
        #             self.player_color_turn.config(text='Blacks turn')
        #             return True
        # elif self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'black':
        #     newX = self.last_clicked_cell.x - self.pawn_current_pos.x
        #     newY = self.last_clicked_cell.y - self.pawn_current_pos.y
        #     if newX == -2 and newY == 2:  #down left movement from blacks
        #         midX = self.last_clicked_cell.x + 1
        #         midY = self.last_clicked_cell.y - 1
        #         if self.board.cells[midX][midY].free != True:
        #             self.remove_pawn_from_board(midX, midY)
        #             self.player_color_turn.config(text='Whites turn')
        #             return True
        #     elif newX == 2 and newY == 2:  #Down right movement from blacks
        #         midX = self.last_clicked_cell.x - 1
        #         midY = self.last_clicked_cell.y -1
        #         if self.board.cells[midX][midY].free != True:
        #             self.remove_pawn_from_board(midX, midY)
        #             self.player_color_turn.config(text='Whites turn')
        #             return True
        # return False
    
    def movement_direction(self, new_x, new_y):
        if self.selected_pawn.type == 'pawn':
            if self.turn_color == 'white':
                if new_x == -1 and new_y == -1:
                    return 'up_left'
                if new_x == 1 and new_y == -1:
                    return 'up_right'
            if self.turn_color == 'black':
                if new_x == -1 and new_y == 1:
                    return 'down_left'
                if new_x == 1 and new_y == 1:
                    return 'down_right'
        if self.selected_pawn.type == 'queen':
            if new_x < 0 and new_y > 0:
                return 'down_left'
            if new_x > 0 and new_y > 0:
                return 'down_right'
            if new_x < 0 and new_y < 0:
                return 'up_left'
            if new_x > 0 and new_y < 0:
                return 'up_right'
        return None

    def tracing_queen_diag(self, new_x, new_y):
        print(f'a')
            

    def remove_pawn_from_board(self, midX, midY):
        captured_pawn = self.board.cells[midX][midY].pawned
        self.board.pawns.remove(captured_pawn)
        self.board.canvas.delete(captured_pawn.id)
        self.board.cells[midX][midY].free = True
        self.board.cells[midX][midY].pawned = None

    def promote_pawn(self):
        # Promote whites when they reach opposite side of the board
        if (self.selected_pawn.type == 'pawn' and self.turn_color == 'white' 
            and self.selected_pawn.x % 2 != 0 and self.selected_pawn.y == 0):
            self.selected_pawn.type = 'queen'
            self.board.canvas.itemconfig(self.selected_pawn.id,fill='blue')

        # Promote blacks when they reach opposite side of the board
        elif (self.selected_pawn.type == 'pawn' and self.turn_color == 'black' 
            and self.selected_pawn.x % 2 == 0 and self.selected_pawn.y == 7):
            self.selected_pawn.type = 'queen'
            self.board.canvas.itemconfig(self.selected_pawn.id,fill='red')

        else:
            print(f'nothing promoted')
    

    def reset_values(self):
        self.pawn_current_pos = None
        self.pawn_new_pos = None
        self.last_clicked_cell = None
        self.selected_pawn = None
