class Nonogram:
    def __init__(self, filename):
        self.rowHints = []
        self.colHints = []
        self.read_nonogram_from_file(filename)
        self.nRows = len(self.rowHints)
        self.nCols = len(self.colHints)
        self.rows = [[0]*self.nCols + [-1] for i in range(self.nRows)]
        self.cols = [[0]*self.nRows + [-1] for i in range(self.nCols)]
        self.rowBlockOrigins = [[0]*len(hints) for hints in self.rowHints]
        self.colBlockOrigins = [[0]*len(hints) for hints in self.colHints]
        self.rowBlockEndings = [[self.nCols - 1]*len(hints) for hints in self.rowHints]
        self.colBlockEndings = [[self.nRows - 1]*len(hints) for hints in self.colHints]
        self.undetermind = self.nRows*self.nCols
        self.rowsChanged = set(range(self.nRows))
        self.colsChanged = set(range(self.nCols))
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
    
    def fill_cell(self, row, col, value):
        """
        Fills the cell at position [row][col] with value.
        +1 represents filled cell.
        -1 represents empty cell.
         0 represents yet unknown cell.
        
        Return:
        -------
        sth_changed - bool variable informing if cell state has been changed
        """
        if self.rows[row][col] == self.cols[col][row] == value:
            return False
        elif self.rows[row][col] == self.cols[col][row] == 0:
            self.rows[row][col] = self.cols[col][row] = value
            self.undetermind -= 1
            return True
        else:
            raise Exception("Trying to overwrite filled/empty cell!")