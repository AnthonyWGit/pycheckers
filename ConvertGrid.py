class ConvertGrid:
    def __init__(self):
        self.mapping = self.createDict()
        
    def createDict(self):
        # Create a dictionary to map (x, y) to Chinook notation
        mapping = {}
        correctCoords = 1  # because in the program the first cell is 0.0, here we just init value doesn't matter could be 30
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 1:  # Only consider grey
                    mapping[(x, y)] = correctCoords
                    correctCoords += 1
        return mapping
    
    def convert(self, x, y):
        # Convert the (x, y) coordinate to Chinook notation 
        return self.mapping.get((x, y), None)