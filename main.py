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


    def run(self):
        self.board()
        self.window.mainloop()

#Draw the board
    def board(self):
        board_borders = tk.Canvas(self.window, borderwidth=1)   
        board_borders.grid(row = 1, column = 0, sticky = "ew", columnspan= 8, rowspan= 8)
        row = 8
        col = 8
        i = 0
        j = 0
        x = 30
        y = 30
        for j in range(col):
            if (j % 2 == 0):
                for i in range(row):
                    #pair number
                    if(i % 2 == 0):
                        #first two numbers for argument are coordinates at top left and rest on px after bottom right 
                        # https://web.archive.org/web/20181223164027/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_rectangle.html
                        board_borders.create_rectangle(i * x,j * y,(i + 1) * x,(j + 1) *y,fill='black')
                    else:
                        board_borders.create_rectangle(i * x,j * y,(i + 1) * x,(j + 1) *y,fill='white')
            else:
                for i in range(row):
                    #pair number
                    if(i % 2 == 0):
                        board_borders.create_rectangle(i * x,j * y,(i + 1) * x,(j + 1) *y,fill='white')
                    else:
                        board_borders.create_rectangle(i * x,j * y,(i + 1) * x,(j + 1) *y,fill='black')



#Create the window and let it run until user quits 
root = tk.Tk()
my_window = MainWindow(root)
my_window.run()


