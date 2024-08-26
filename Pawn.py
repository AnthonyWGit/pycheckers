

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
