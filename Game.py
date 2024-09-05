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
        self.direction = ''
        self.hypoX = None #Used in queen movement
        self.hypoY = None
        self.turn_color_set()
        self.pawnsEncountered = [] # Used in queen movement
        self.capture = False
    
    def run(self):
        self.window.mainloop()

    def turn_color_set(self):
        if self.turn % 2 == 0:
            self.turn_color = 'black'
            self.turn_label.config(text=f'Turn {self.turn}')
            self.player_color_turn.config(text='Blacks turn')
        else:
            self.turn_color = 'white'
            self.turn_label.config(text=f'Turn {self.turn}')
            self.player_color_turn.config(text='Whites turn')

    def turn_switch(self):
        self.turn += 1
        self.turn_color_set()
        self.turn_label.config(text=f'Turn {self.turn}')
        self.instruction_label.config(text=f'Choose a pawn to move')
        self.reset_values()

    def select_pawn(self):
        #when Whites turn
        if (self.turn % 2 != 0):
            #change label anouncing player turn 
            if (self.last_clicked_cell.free == False and self.last_clicked_cell.pawned.color == 'white'):
                self.instruction_label.config(text="Choose where you want your pawn to go")
                self.pawn_current_pos = self.last_clicked_cell
                self.selected_pawn = self.pawn_current_pos.pawned
                return True
        else:
            if (self.last_clicked_cell.free == False and self.last_clicked_cell.pawned.color == 'black'):
                self.instruction_label.config(text="Choose where you want your pawn to go")
                self.pawn_current_pos = self.last_clicked_cell
                self.selected_pawn = self.pawn_current_pos.pawned
                return True

        # get x and y pos in the canvas 
    def on_click(self, event):
        # remove the whole division // and you will get the position in pixels where you click ! 
        # using floor division so no we get an integer and not a float  
        cell_x = event.x // self.board.x 
        cell_y = event.y // self.board.y 
        # Now you can use these coordinates to move the pawn
        clicked_cell = self.board.cells[cell_x][cell_y]
        self.last_clicked_cell = clicked_cell
        
        if self.selected_pawn == None:
            if self.select_pawn() == True:
                print(f'Selected Pawn : {self.selected_pawn}')
                return
            
        if (self.selected_pawn != None):
            # In this if a pawn is already select : first we check if the last clicked cell is the same so the user can cancel his choice
            if (self.selected_pawn.x == self.last_clicked_cell.x) & (self.selected_pawn.y == self.last_clicked_cell.y):
                self.reset_values()
                self.instruction_label.config(text=f'Choose a pawn to move')
                return
            if self.movement_is_valid() == True or self.capture_pawn() == True:
                #check if capture
                # Get the old cell
                old_cell = self.board.cells[self.pawn_current_pos.x][self.pawn_current_pos.y]
                # Update the old cell
                old_cell.free = True
                old_cell.pawned = None
                #selected pawn getting the same coords as the last clicked cell 
                self.selected_pawn.x = self.last_clicked_cell.x
                self.selected_pawn.y = self.last_clicked_cell.y
                # Get the new cell
                new_cell = self.board.cells[self.last_clicked_cell.x][self.last_clicked_cell.y]
                # Update the new cell
                new_cell.free = False
                new_cell.pawned = self.selected_pawn
                self.move_pawn(self.selected_pawn, self.selected_pawn.x, self.selected_pawn.y)
                #check promotions
                self.promote_pawn()
                self.pawn_current_pos = self.selected_pawn
                #when everything is good increase turn count and clean values
                if self.capture_additional() == False:
                    self.turn_switch()
            if self.movement_is_valid == False:
                print('false movement')
                self.soft_reset()

    def movement_is_valid(self):
        #check if white movement is correct
        if self.selected_pawn.type == 'pawn':
            print(f'XXXXX----{self.last_clicked_cell}----XXXXX{self.selected_pawn}')
            if self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'white':
                newX = self.last_clicked_cell.x - self.pawn_current_pos.x
                newY = self.last_clicked_cell.y - self.pawn_current_pos.y
                print(f'{newX} /--/ {newY}')
                print(f'{self.last_clicked_cell.x} - {self.pawn_current_pos.x} / {self.last_clicked_cell.y} - {self.pawn_current_pos.y}')
                if newX == -1 and newY == -1 or newX == 1 and newY == -1:  # No absolute because we are using pawn movvement (standard)
                    self.pawn_new_pos = self.last_clicked_cell
                    return True
            elif self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'black':
                newX = self.last_clicked_cell.x - self.pawn_current_pos.x
                newY = self.last_clicked_cell.y - self.pawn_current_pos.y
                print(f'{newX} - {newY}')
                if newX == -1 and newY == 1 or newX == 1 and newY == 1:  #  No absolute because we are using pawn movvement (standard)
                    self.pawn_new_pos = self.last_clicked_cell
                    return True
            return False
        elif self.selected_pawn.type == 'queen':
            newX = self.last_clicked_cell.x - self.pawn_current_pos.x
            newY = self.last_clicked_cell.y - self.pawn_current_pos.y
            direction_label = self.movement_direction(newX,newY)
            if self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'white':
                if self.last_clicked_cell.color == 'grey' and self.movement_direction(newX, newY) != None:  # Check if the absolute difference is 1 because queen will be able to go  backwards
                    if self.calc_diagonal(newX, newY, direction_label) == 1: #Not correct move
                        self.soft_reset()
                        return False
                    elif self.calc_diagonal(newX, newY, direction_label) == 0: #legit move - no capture
                        self.pawn_new_pos = self.last_clicked_cell
                        return True
                    elif (self.calc_diagonal(newX,newY, direction_label) == 3): #capture opposite
                        self.capture = True
                        self.capture_queen(self.hypoX, self.hypoY, direction_label)
                        self.pawn_new_pos = self.last_clicked_cell
                        return True
            elif self.last_clicked_cell.free == True and self.last_clicked_cell.color == 'grey' and self.turn_color == 'black':
                if self.last_clicked_cell.color == 'grey' and self.movement_direction(newX, newY) != None:  # Check if the absolute difference is 1 because queen will be able to go  backwards
                    if self.calc_diagonal(newX, newY, direction_label) == 1: #invalid move
                        self.soft_reset() #clears the encountered list 
                        return False
                    elif self.calc_diagonal(newX, newY, direction_label) == 0:
                        self.pawn_new_pos = self.last_clicked_cell
                        return True
                    elif self.calc_diagonal(newX, newY, direction_label) == 3:
                        self.capture = True
                        self.capture_queen(self.hypoX, self.hypoY, direction_label)
                        self.pawn_new_pos = self.last_clicked_cell
                        return True
            return False
            
    
    def move_pawn(self, pawn, new_x, new_y):
        # Calculate the new coordinates for the pawn
        new_coords = (new_x * self.board.x + 5, new_y * self.board.y + 5,
                    (new_x + 1) * self.board.x - 5, (new_y + 1) * self.board.y - 5)
        # Use the coords method to update the pawn's position on the canvas
        self.board.canvas.coords(pawn.id, new_coords)


    def capture_pawn(self):
        if self.selected_pawn.type == 'pawn':
            if self.last_clicked_cell.free == True:
                newX = self.last_clicked_cell.x - self.pawn_current_pos.x
                newY = self.last_clicked_cell.y - self.pawn_current_pos.y
                if self.last_clicked_cell.color == 'grey' and self.turn_color == 'white':
                    if newX == -2 and newY == -2:  #Up left movement from whites 
                        midX = self.last_clicked_cell.x + 1
                        midY = self.last_clicked_cell.y + 1
                        if self.board.cells[midX][midY].free != True:
                            self.capture = True
                            self.remove_pawn_from_board(midX, midY)
                            return True
                    if newX == 2 and newY == -2:  #Up right movement from whites
                        midX = self.last_clicked_cell.x - 1
                        midY = self.last_clicked_cell.y + 1
                        if self.board.cells[midX][midY].free != True:
                            self.capture = True
                            self.remove_pawn_from_board(midX, midY)
                            return True
                if self.capture == True:
                        if newX == -2 and newY == 2:  #Down left movement from whites 
                            midX = self.last_clicked_cell.x + 1
                            midY = self.last_clicked_cell.y - 1
                            if self.board.cells[midX][midY].free != True:
                                self.capture = True
                                self.remove_pawn_from_board(midX, midY)
                                return True
                        if newX == 2 and newY == 2:  #Down right movement from whites
                            midX = self.last_clicked_cell.x - 1
                            midY = self.last_clicked_cell.y - 1
                            if self.board.cells[midX][midY].free != True:
                                self.capture = True
                                self.remove_pawn_from_board(midX, midY)
                                return True
                if self.last_clicked_cell.color == 'grey' and self.turn_color == 'black':
                    if newX == -2 and newY == 2:  #down left movement from blacks
                        midX = self.last_clicked_cell.x + 1
                        midY = self.last_clicked_cell.y - 1
                        if self.board.cells[midX][midY].free != True:
                            self.capture = True
                            self.remove_pawn_from_board(midX, midY)
                            return True
                    if newX == 2 and newY == 2:  #Down right movement from blacks
                        midX = self.last_clicked_cell.x - 1
                        midY = self.last_clicked_cell.y - 1
                        if self.board.cells[midX][midY].free != True:
                            self.capture = True
                            self.remove_pawn_from_board(midX, midY)
                            return True
                    if self.capture == True:
                        if newX == -2 and newY == -2:  #Up left movement from blacks
                            midX = self.last_clicked_cell.x + 1
                            midY = self.last_clicked_cell.y + 1
                            if self.board.cells[midX][midY].free != True:
                                self.capture = True
                                self.remove_pawn_from_board(midX, midY)
                                return True
                        if newX == 2 and newY == -2:  #Up right movement from blacks
                            midX = self.last_clicked_cell.x - 1
                            midY = self.last_clicked_cell.y + 1
                            if self.board.cells[midX][midY].free != True:
                                self.capture = True
                                self.remove_pawn_from_board(midX, midY)
                                return True
                return False
        return False

    def capture_queen(self, hypoX, hypoY, direction):
        if self.selected_pawn.type == "queen":
            if self.last_clicked_cell.free == True:
                print(f'remoove')
                xToRemove = self.pawnsEncountered[0].x
                yToRemove = self.pawnsEncountered[0].y
                self.remove_pawn_from_board(xToRemove, yToRemove)

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
        if abs(new_x) != abs(new_y): #using absolutes to verify diagonals
            return None  

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
    
    def calc_diagonal(self, newX, newY, direction):
        while self.hypoX != self.last_clicked_cell.x and self.hypoY != self.last_clicked_cell.y:
            if self.hypoX == None and self.hypoY == None:
                self.hypoX = self.selected_pawn.x
                self.hypoY = self.selected_pawn.y
            if direction == "down_left":
                self.hypoX = self.hypoX - 1
                self.hypoY = self.hypoY + 1
            if direction == "down_right":
                self.hypoX = self.hypoX + 1
                self.hypoY = self.hypoY + 1
            if direction == "up_left":
                self.hypoX = self.hypoX - 1
                self.hypoY = self.hypoY - 1
            if direction == "up_right":
                self.hypoX = self.hypoX + 1
                self.hypoY = self.hypoY - 1
            #Store all encountered pawns in a list
            if self.board.cells is not None and self.board.cells[self.hypoX][self.hypoY].pawned:
                encounteredPawn = self.board.cells[self.hypoX][self.hypoY].pawned
                self.pawnsEncountered.append(encounteredPawn)
            print(f'{self.hypoX} --- {self.hypoY} -- {self.last_clicked_cell.x} -- {self.last_clicked_cell.y} -- {self.pawnsEncountered}')
            
        #If there is one or more pawn of the same color of the player in the diagonal the move is not valid
        #If there are more than one pawn of the opposite color the move is not valid
        for pawn in self.pawnsEncountered:
            if pawn.color == self.turn_color or len(self.pawnsEncountered) > 1:
                self.soft_reset()
                print('roadblock')
                return 1 
        if len(self.pawnsEncountered) == 1 and self.pawnsEncountered[0].color != self.turn_color:
                print('capture')
                return 3

        print('nothing')
        return 0

    def capture_additional(self):
        additional_turn = False
        # Out of bounds checks to avoid error index out of range 
        bX = [0, 7]
        bY = [0, 7]
        filtered_cells = []

        # First check the nearest cells of the pawn that did a capture
        cells2Check = {
            "up_right": (self.selected_pawn.x + 1, self.selected_pawn.y - 1),
            "up_left": (self.selected_pawn.x - 1, self.selected_pawn.y - 1),
            "down_left": (self.selected_pawn.x - 1, self.selected_pawn.y + 1),
            "down_right": (self.selected_pawn.x + 1, self.selected_pawn.y + 1)
        }

        # Loop over all the cells to check and add the correct ones to the filtered cells list 
        for direction, (x, y) in cells2Check.items():
            if bX[0] <= x <= bX[1] and bY[0] <= y <= bY[1]:
                filtered_cells.append((direction, x, y))

        # Loop all over the filtered cells and if there is one where there is an enemy pawn and a free cell behind, turn on the additional turn to true
        for direction, x, y in filtered_cells:
            cell = self.board.cells[x][y]
            if direction == "up_right":
                behind_x, behind_y = x + 1, y - 1
            elif direction == "up_left":
                behind_x, behind_y = x - 1, y - 1
            elif direction == "down_right":
                behind_x, behind_y = x + 1, y + 1
            elif direction == "down_left":
                behind_x, behind_y = x - 1, y + 1

            if (bX[0] <= behind_x <= bX[1] and bY[0] <= behind_y <= bY[1]):
                behind_cell = self.board.cells[behind_x][behind_y]
                if (cell.pawned is not None and cell.pawned.color != self.turn_color and behind_cell.free == True and self.capture):
                    additional_turn = True
                    break  # No need to check further if we already found a valid capture
        
        return additional_turn

    def reset_values(self):
        self.pawn_current_pos = None
        self.pawn_new_pos = None
        self.last_clicked_cell = None
        self.selected_pawn = None
        self.pawnsEncountered.clear()
        self.hypoX = None
        self.hypoY = None
        self.capture = False

    #soft reset does not erase the current position of pawn. Is is used to reset variables without deselecting a pawn
    def soft_reset(self):
        self.pawnsEncountered.clear()
        self.hypoX = None
        self.hypoY = None
        self.pawn_new_pos = None
        self.last_clicked_cell = None
