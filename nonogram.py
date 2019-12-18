class Nonogram:
    def __init__(self, filename):
        self.rowHints = []
        self.colHints = []
        self.read_nonogram_from_file(filename)
        self.nRows = len(self.rowHints)
        self.nCols = len(self.colHints)
        self.rows = [[0]*self.nCols + [-1]]*self.nRows
        self.cols = [[0]*self.nRows + [-1]]*self.nCols
        self.rowBlockOrigins = [[0]*len(hints) for hints in self.rowHints]
        self.colBlockOrigins = [[0]*len(hints) for hints in self.colHints]
        self.rowBlockEndings = [[self.nCols - 1]*len(hints) for hints in self.rowHints]
        self.colBlockEndings = [[self.nRows - 1]*len(hints) for hints in self.colHints]
        self.undetermind = self.nRows*self.nCols
        self.rowsChanged = [] # Probably will be changed
        self.colsChanged = [] # Probably will be changed
        self.transposed = False
    
    def read_nonogram_from_file(self, filename):
        """
        Fills the rowHints and colHints with data read from file.
        """
        file = open(filename, 'r')
        while True:
            line = file.readline()
            if line[:5] == "ROWS:":
                while True:
                    line = file.readline()
                    if line[:8] == "COLUMNS:":
                        break
                    elif line == '':
                        raise Exception("Incorrect data file.")
                    else:
                        self.rowHints.append(list(map(int, line.split(' '))))
                while True:
                    line = file.readline()
                    if line == '':
                        break
                    else:
                        self.colHints.append(list(map(int, line.split(' '))))
            if line == '':
                break
                                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        