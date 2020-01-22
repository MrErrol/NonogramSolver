# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from utils.visualizers import plot, update_plot, end_iplot
from utils.read_from_file import read_datafile
from copy import copy

class Nonogram:
    def __init__(self, filename):
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
        self.fig = None
        self.im = None
    
    def self_consistency_check(self):
        """
        Checks if sum of filled cell according to hints on rows and columns is the same.
        Usually allows to smoke-gun typing error.
        
        Return:
        bool - bool variable informing if nonogram seems to be self-consistet
        """
        npixR = sum([sum(row) for row in self.rowHints]) # number of filled cells in rows
        npixC = sum([sum(col) for col in self.colHints]) # number of filled cells in columns
        if not npixR == npixC:
            print('Input nonogram is not self consistent.')
            print('The sum of filled cells in rows is different than in columns.')
            return False
        
        return True
        
    def read_nonogram_from_file(self, filename):
        """
        Fills the rowHints and colHints with data read from file.
        """
        # This part of code is used by method copy()
        if filename == None: 
            self.rowHints = []
            self.colHints = []
            return 0
        
        # Reading datafile
        self.rowHints, self.colHints = read_datafile(filename)
        
        # simple check of self-consistency
        # usually allows to smoke-gun typing error
        if not self.self_consistency_check():
            quit()
    
    def transpose(self):
        self.rowHints, self.colHints = self.colHints, self.rowHints
        self.nRows, self.nCols = self.nCols, self.nRows
        self.rows, self.cols = self.cols, self.rows
        self.rowBlockOrigins, self.colBlockOrigins = self.colBlockOrigins, self.rowBlockOrigins
        self.rowBlockEndings, self.colBlockEndings = self.colBlockEndings, self.rowBlockEndings
        self.rowsChanged, self.colsChanged = self.colsChanged, self.rowsChanged
        self.transposed = not self.transposed
    
    def copy(self):
        """
        Method that copies Nonogram. It does not copy interactive plot references.
        """
        nono = Nonogram(None)
        nono.rowHints = self.rowHints
        nono.colHints = self.colHints
        nono.nRows = self.nRows
        nono.nCols = self.nCols
        nono.rows = [[item for item in row] for row in self.rows]
        nono.cols = [[item for item in row] for row in self.cols]
        nono.rowBlockOrigins = [[item for item in row] for row in self.rowBlockOrigins]
        nono.colBlockOrigins = [[item for item in row] for row in self.colBlockOrigins]
        nono.rowBlockEndings = [[item for item in row] for row in self.rowBlockEndings]
        nono.colBlockEndings = [[item for item in row] for row in self.colBlockEndings]
        nono.undetermind = copy(self.undetermind)
        nono.rowsChanged = copy(self.rowsChanged)
        nono.colsChanged = copy(self.colsChanged)
        nono.transposed = copy(self.transposed)
        nono.fig = None
        nono.im = None
        return nono
    
    def get_picture_data(self):
        """
        The function does not modify Nonogram.
        Strips empty cells from row endings and transposes obtained data if nonogram is transposed.
        
        Returns:
        --------
        data - matrix (list of lists) of nonogram cell values        
        """
        if not self.transposed:
            data = [row[:-1] for row in self.rows]
        else:
            data = [col[:-1] for col in self.cols]
        return data
    
    def plot(self, interactive=False):
        """
        Calls plotting function and stores obtained figure and image.
        """
        data = self.get_picture_data()
        self.fig, self.im = plot(data, interactive=interactive)
        
    def update_plot(self):
        """
        Calls function that updates plot.
        Figure and image are updated by it.
        """
        data = self.get_picture_data()
        update_plot(data, self.fig, self.im)
    
    def end_iplot(self):
        self.update_plot()
        end_iplot()
    
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
            self.rowsChanged.add(row)
            self.colsChanged.add(col)
            self.undetermind -= 1
            return True
        else:
            raise Exception("Trying to overwrite filled/empty cell!"+' '+str(row)+' '+str(col))