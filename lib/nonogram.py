from copy import copy, deepcopy

# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from utils.visualizers import plot, update_plot, end_iplot
from utils.read_from_file import read_datafile, structure_raw_cells, transpose_rows


class OverwriteException(Exception):
    """
    Exception raised, when program tries to overwrite filled/empty cell.
    If not raised while assumption making it means that nonogram provided
    is unsolvable.
    """
    pass


class Data:
    """
    Class containing actual status (filled, empty, unknown) of nonogram cells
    along with hints provided by user.
    """


    def __init__(self, filename=None, presolved=False):
        if filename is None:
            self.rows = [[]]
            self.cols = [[]]
            self.rowHints = [[]]
            self.colHints = [[]]
        else:
            self.rowHints, self.colHints, rawRows = read_datafile(
                filename,
                presolved=presolved,
            )
            self.rows = structure_raw_cells(rawRows)
            self.cols = transpose_rows(self.rows)

        if not self.self_consistency_check():
            self.complain()
            quit()


    def self_consistency_check(self):
        """
        Checks if sum of filled cell according to hints on rows and columns
        is the same.
        Usually allows to smoke-gun typing error.

        Return:
        bool - bool variable informing if nonogram seems to be self-consistet
        """
        # number of filled cells in rows
        numberPixelRows = sum([sum(row) for row in self.rowHints])
        # number of filled cells in columns
        numberPixelCols = sum([sum(col) for col in self.colHints])
        if not numberPixelRows == numberPixelCols:
            return False

        return True


    def complain(self):
        """
        Function informs user about inconsistency in provided data.
        It is usually caused by typing error.
        """
        print('Input nonogram is not self consistent.')
        print('The sum of filled cells in rows is different than in columns.')


    def transpose(self):
        """
        Exchanges rows with columns.
        """
        self.rowHints, self.colHints = self.colHints, self.rowHints
        self.rows, self.cols = self.cols, self.rows


    def copy(self):
        """
        Function makes a copy of a class instance.
        Copied class share common hints with the original one.
        """
        new_data = Data()
        new_data.rowHints = self.rowHints
        new_data.colHints = self.colHints
        new_data.rows = deepcopy(self.rows)
        new_data.cols = deepcopy(self.cols)
        return new_data


    def fill_cell(self, row, col, value):
        """
        Fills the cell at position [row][col] with value.
        +1 represents filled cell.
        -1 represents empty cell.
         0 represents yet unknown cell.

        In order to preserve data consistency the method should be used only by
        corresponding method of class Nonogram.

        Return:
        -------
        sth_changed - bool variable informing if cell state has been changed
        """
        if self.rows[row][col] == self.cols[col][row] == value:
            return False
        elif self.rows[row][col] == self.cols[col][row] == 0:
            self.rows[row][col] = self.cols[col][row] = value
            return True
        else:
            raise OverwriteException(
                "Trying to overwrite filled/empty cell! " + \
                str(row) + ' ' + str(col)
            )


    def get_row_hints(self, row, blockIndex=None):
        if blockIndex is None:
            return self.rowHints[row]
        else:
            return self.rowHints[row][blockIndex]


    def get_col_hints(self, col, blockIndex=None):
        if blockIndex is None:
            return self.colHints[col]
        else:
            return self.colHints[col][blockIndex]


    def get_row(self, row=None):
        if row is None:
            return self.rows
        else:
            return self.rows[row]


    def get_col(self, col=None):
        if col is None:
            return self.cols
        else:
            return self.cols[col]


class Limits:
    """
    Class containing all block origins and endings deduced up to now.
    Block limits (origins and endings) are initialized at their maximal
    possible values. No analysis is performed.

    When fed with incomplete data returns empty class.
    """


    def __init__(self, rowHints=None, colHints=None):
        if (rowHints is None) or (colHints is None):
            self.rowBlockOrigins = [[]]
            self.rowBlockEndings = [[]]
            self.colBlockOrigins = [[]]
            self.colBlockEndings = [[]]
        else:
            self.rowBlockOrigins = [[0] * len(hints) for hints in rowHints]
            self.colBlockOrigins = [[0] * len(hints) for hints in colHints]
            self.rowBlockEndings = [[len(colHints) - 1] * len(hints) \
                                    for hints in rowHints]
            self.colBlockEndings = [[len(rowHints) - 1] * len(hints) \
                                    for hints in colHints]


    def copy(self):
        """
        Returns a deepcopy of a class.
        """
        return deepcopy(self)


    def transpose(self):
        """
        Exchanges rows with columns.
        """
        self.rowBlockOrigins, self.colBlockOrigins = \
            self.colBlockOrigins, self.rowBlockOrigins
        self.rowBlockEndings, self.colBlockEndings = \
            self.colBlockEndings, self.rowBlockEndings


    def get_row_origins(self, row, blockIndex=None):
        if blockIndex is None:
            return self.rowBlockOrigins[row]
        else:
            return self.rowBlockOrigins[row][blockIndex]


    def get_row_endings(self, row, blockIndex=None):
        if blockIndex is None:
            return self.rowBlockEndings[row]
        else:
            return self.rowBlockEndings[row][blockIndex]


    def get_col_origins(self, col, blockIndex=None):
        if blockIndex is None:
            return self.colBlockOrigins[col]
        else:
            return self.colBlockOrigins[col][blockIndex]


    def get_col_endings(self, col, blockIndex=None):
        if blockIndex is None:
            return self.colBlockEndings[col]
        else:
            return self.colBlockEndings[col][blockIndex]


    def set_row_origins(self, row, newOrigins):
        self.rowBlockOrigins[row] = newOrigins


    def set_col_origins(self, row, newOrigins):
        self.colBlockOrigins[row] = newOrigins


    def set_row_endings(self, row, newEndings):
        self.rowBlockEndings[row] = newEndings


    def set_col_endings(self, row, newEndings):
        self.colBlockEndings[row] = newEndings


class MetaData:
    """
    Class containing metadata of nonogram used by logic of solving algorithm.
    Solver metadata are located in ModeData class.

    Contains:
    - number of yet unsolved cells
    - indices of rows and columns that changed since last reset (usually
      since beggining of iteration)
    - information whether nonogram is transosed
    """


    def __init__(self, nRows, nCols):
        self.undetermind = nRows * nCols
        self.rowsChanged = set(range(nRows))
        self.colsChanged = set(range(nCols))
        self.transposed = False


    def copy(self):
        """
        Returns deepcopy of itself.
        """
        return deepcopy(self)


    def transpose(self):
        """
        Exchanges rows with columns and stores information about transposition
        state of the nonogram.
        """
        self.rowsChanged, self.colsChanged = \
            self.colsChanged, self.rowsChanged
        self.transposed = not self.transposed


    def filled_cell(self, row, col):
        """
        Updates metadata after filling the cell at position (row, col).
        """
        self.rowsChanged.add(row)
        self.colsChanged.add(col)
        self.undetermind -= 1


    def reset_changed_rows_and_cols(self):
        """
        Resets counter of changed rows and columns.
        """
        self.rowsChanged = set()
        self.colsChanged = set()


    def get_rows_changed(self):
        """
        Returns rows changed since last reset.
        """
        return self.rowsChanged


    def get_cols_changed(self):
        """
        Returns columns changed since last reset.
        """
        return self.rowsChanged


class Nonogram:
    def __init__(self, filename, presolved=False, wait=0.0):
        dummy_rows = self.read_nonogram_from_file(filename, presolved=presolved)
        self.rowBlockOrigins = [[0]*len(hints) for hints in self.rowHints]
        self.colBlockOrigins = [[0]*len(hints) for hints in self.colHints]
        self.rowBlockEndings = [[self.nCols - 1]*len(hints) \
                                for hints in self.rowHints]
        self.colBlockEndings = [[self.nRows - 1]*len(hints) \
                                for hints in self.colHints]
        self.undetermind = self.nRows*self.nCols
        self.rowsChanged = set(range(self.nRows))
        self.colsChanged = set(range(self.nCols))
        self.transposed = False
        self.fig = None
        self.im = None
        self.wait = wait
        self.hinter = 'simple'
        self.verbose = 0


    def self_consistency_check(self):
        """
        Checks if sum of filled cell according to hints on rows and columns
        is the same.
        Usually allows to smoke-gun typing error.

        Return:
        bool - bool variable informing if nonogram seems to be self-consistet
        """
        # number of filled cells in rows
        npixR = sum([sum(row) for row in self.rowHints])
        # number of filled cells in columns
        npixC = sum([sum(col) for col in self.colHints])
        if not npixR == npixC:
            return False

        return True


    def read_nonogram_from_file(self, filename, presolved=False):
        """
        Fills the rowHints and colHints with data read from file.
        """
        # This part of code is used by method copy()
        if filename is None:
            self.rowHints = []
            self.colHints = []
            self.nRows = 0
            self.nCols = 0
            return 0

        # Reading datafile
        self.rowHints, self.colHints, rows = read_datafile(filename,
                                                           presolved=presolved,
                                                          )
        self.nRows = len(self.rowHints)
        self.nCols = len(self.colHints)
        self.fill_presolved_cells(rows, presolved=presolved)

        # simple check of self-consistency
        # usually allows to smoke-gun typing error
        if not self.self_consistency_check():
            print('Input nonogram is not self consistent.')
            print('The sum of filled cells in rows is different than in columns.')
            quit()

        return rows


    def fill_presolved_cells(self, rows, presolved=False):
        if presolved:
            self.rows = [row + [-1] for row in rows]
            self.cols = transpose_rows(self.rows)
        else:
            self.rows = [[0]*self.nCols + [-1] for i in range(self.nRows)]
            self.cols = [[0]*self.nRows + [-1] for i in range(self.nCols)]


    def transpose(self):
        self.rowHints, self.colHints = self.colHints, self.rowHints
        self.nRows, self.nCols = self.nCols, self.nRows
        self.rows, self.cols = self.cols, self.rows
        self.rowBlockOrigins, self.colBlockOrigins = \
            self.colBlockOrigins, self.rowBlockOrigins
        self.rowBlockEndings, self.colBlockEndings = \
            self.colBlockEndings, self.rowBlockEndings
        self.rowsChanged, self.colsChanged = \
            self.colsChanged, self.rowsChanged
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
        nono.rows = deepcopy(self.rows)
        nono.cols = deepcopy(self.cols)
        nono.rowBlockOrigins = deepcopy(self.rowBlockOrigins)
        nono.colBlockOrigins = deepcopy(self.colBlockOrigins)
        nono.rowBlockEndings = deepcopy(self.rowBlockEndings)
        nono.colBlockEndings = deepcopy(self.colBlockEndings)
        nono.undetermind = copy(self.undetermind)
        nono.rowsChanged = copy(self.rowsChanged)
        nono.colsChanged = copy(self.colsChanged)
        nono.transposed = copy(self.transposed)
        nono.fig = None
        nono.im = None
        nono.wait = self.wait
        nono.hinter = self.hinter
        nono.verbose = self.verbose
        return nono


    def get_true_rows(self):
        """
        The function returns copy of true rows of the nonogram effectively
        canceling potential nonogram transposition.

        Returns:
        --------
        data - matrix (list of lists) of nonogram cell values (including
               trailing -1)
        """
        if self.transposed:
            return copy(self.cols)
        else:
            return copy(self.rows)


    def get_picture_data(self):
        """
        The function does not modify Nonogram.
        Strips empty cells from row endings and transposes obtained data if
        nonogram is transposed.

        Returns:
        --------
        data - matrix (list of lists) of nonogram cell values
        """
        rows = self.get_true_rows()
        return [row[:-1] for row in rows]


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
        update_plot(data, self.fig, self.im, self.wait)


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
            raise Exception("Trying to overwrite filled/empty cell! " + \
                            str(row) + ' ' + str(col)
                           )


    def show_basic_hint(self, row, col):
        """
        Prints basic hint about next cell to be filled.
        """
        if self.hinter == 'simple':
            if self.transposed:
                print('Analyze column ' + str(row) + '.')
            else:
                print('Analyze row ' + str(row) + '.')
        else:
            if self.transposed:
                print("Assume the cell at row=" + str(col) + " and col=" + \
                      str(row) + " to be filled and try to deduce consequences.")
            else:
                print("Assume the cell at row=" + str(row) + " and col=" + \
                      str(col) + " to be filled and try to deduce consequences.")


    def show_hint(self, row, col, value):
        """
        Prints information about next cell to be filled. Adds small hint
        how to deduce it.
        Shifts index to counting from 1.
        """
        self.show_basic_hint(row + 1, col + 1)

        if self.verbose:
            values = {-1:'empty.', 1:'filled.'}
            print("Cell at row=" + str(row+1) + " and col=" + str(col+1) +
                  " may be deduced to be " + values[value])
            if self.hinter == 'assumption_making':
                print('You will need to analyze more than just single row or column.')
        quit()
