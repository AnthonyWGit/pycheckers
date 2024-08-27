class Cell:
    def __init__(self, x, y, color):
        # Coordinates
        self.x = x
        self.y = y
        self.free = True
        self.pawned = None  # Will tell if there is a pawn at this pos or not
        self.color = color

        
    def __repr__(self):
        return f"Cell at ({self.x}, {self.y}), free: {self.free}, pawn: {self.pawned}, color: {self.color}"