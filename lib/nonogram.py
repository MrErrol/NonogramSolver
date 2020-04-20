from copy import copy, deepcopy

# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from utils.visualizers import plot, update_plot, end_iplot
from utils.read_from_file import read_datafile, structure_raw_cells, \
    strip_trailing_empty_cells, transpose_rows


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


    def get_row_hints(self, row=None, blockIndex=None):
        if row is None:
            return self.rowHints
        elif blockIndex is None:
            return self.rowHints[row]
        else:
            return self.rowHints[row][blockIndex]


    def get_col_hints(self, col, blockIndex=None):
        if col is None:
            return self.colHints
        elif blockIndex is None:
            return self.colHints[col]
        else:
            return self.colHints[col][blockIndex]


    def get_row(self, row=None, col=None):
        if row is None:
            return self.rows
        elif col is None:
            return self.rows[row]
        else:
            return self.rows[row][col]


    def get_col(self, col=None, row=None):
        if col is None:
            return self.cols
        elif row is None:
            return self.cols[col]
        else:
            return self.cols[col][row]


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


class ProgressTracker:
    """
    Class containing progress data of the solver:
    - rows changed since last reset
    - columns changed since last reset
    - number of undetermind cells
    """
    def __init__(self, nRows, nCols):
        self.rowsChanged = set(range(nRows))
        self.colsChanged = set(range(nCols))
        self.undetermind = nRows * nCols


    def transpose(self):
        """
        Exchanges rows with columns.
        """
        self.rowsChanged, self.colsChanged = \
            self.colsChanged, self.rowsChanged


    def copy(self):
        """
        Returns deepcopy of itself.
        """
        return deepcopy(self)


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


class MetaData:
    """
    Class containing metadata of nonogram used by logic of solving algorithm.
    Solver metadata are located in ModeData class.

    Contains:
    - number of rows and columns
    - class ProgressTracker
    - information whether nonogram is transposed
    """


    def __init__(self, nRows, nCols):
        self.n_rows = nRows
        self.n_cols = nCols
        self.progress_tracker = ProgressTracker(nRows, nCols)
        self.transposed = False


    def copy(self):
        """
        Returns deepcopy of itself.
        """
        new_meta_data = MetaData(self.n_rows, self.n_cols)
        new_meta_data.transposed = copy(self.transposed)
        new_meta_data.progress_tracker = self.progress_tracker.copy()
        return new_meta_data


    def transpose(self):
        """
        Exchanges rows with columns and stores information about transposition
        state of the nonogram.
        """
        self.n_rows, self.n_cols = self.n_cols, self.n_rows
        self.progress_tracker.transpose()
        self.transposed = not self.transposed


    def is_transposed(self):
        """
        Informs whether nonogram data are transposed with respect to
        the original ones.
        """
        return self.transposed


    def get_number_of_rows(self):
        """
        Returns number of rows of a nonogram.
        (In a given transposition state)
        """
        return self.n_rows


    def get_number_of_cols(self):
        """
        Returns number of cols of a nonogram.
        (In a given transposition state)
        """
        return self.n_cols


class ModeData:
    """
    Class containing nonlogistic metadata of Nonogram.

    It contains:
    - image data
    - verbosity level for hinter mode
    """


    def __init__(self, wait=None, verbosity=0):
        self.fig = None
        self.im = None
        self.wait = wait
        self.verbosity = verbosity


    def copy(self):
        """
        Copies the class ignoring all image data.
        (Only verbosity is copied.)
        """
        return ModeData(verbosity=self.verbosity)


    def plot(self, data, interactive=False):
        """
        Calls plotting function and stores obtained figure and image.
        """
        self.fig, self.im = plot(data, interactive=interactive)


    def update_plot(self, data):
        """
        Calls function that updates plot.
        Figure and image are updated by it.
        """
        update_plot(data, self.fig, self.im, self.wait)


    def end_iplot(self):
        """
        Finalizes interactive plot.
        Plot is updated before finalization.
        """
        self.update_plot()
        end_iplot()


    def is_interactive_plot_active(self):
        """
        Informs whether interactive plot is started.
        """
        if self.fig:
            return True
        else:
            return False


    def get_verbosity(self):
        return self.verbosity


class Nonogram:
    """
    Class that holds all data about given nonogram.
    All the interaction with subclasses (except for getters) should be done via
    methods of this class.
    """


    def __init__(self, filename=None, presolved=False, wait=0.0, verbosity=0):
        self.data = Data(filename=filename, presolved=presolved)
        self.limits = Limits(
            self.data.get_row_hints(),
            self.data.get_col_hints(),
        )
        self.meta_data = MetaData(
            len(self.data.get_row()),
            len(self.data.get_col()),
        )
        self.mode_data = ModeData(wait=wait, verbosity=verbosity)


    def transpose(self):
        """
        Methods that transposes nonogram, effectiveli exchanging rows with
        columns. The plot functions are not affected.
        """
        self.data.transpose()
        self.limits.transpose()
        self.meta_data.transpose()


    def copy(self):
        """
        Method that copies Nonogram. It does not copy interactive plot references.
        """
        nono = Nonogram()
        nono.data = self.copy()
        nono.limits = self.limits.copy()
        nono.meta_data = self.meta_data.copy()
        nono.mode_data = self.mode_data.copy()
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
        if self.meta_data.is_transposed():
            return copy(self.data.get_col())
        else:
            return copy(self.data.get_row())


    def get_picture_data(self):
        """
        The function does not modify Nonogram.
        Strips empty cells from row endings and transposes obtained data if
        nonogram is transposed.

        Returns:
        --------
        data - matrix (list of lists) of nonogram cell values
        """
        return strip_trailing_empty_cells(self.get_true_rows())


    def plot(self, interactive=False):
        """
        Calls plotting function and stores obtained figure and image.
        """
        data = self.get_picture_data()
        self.mode_data.plot(data, interactive=interactive)


    def update_plot(self):
        """
        Calls function that updates plot.
        Figure and image are updated by it.
        """
        data = self.get_picture_data()
        self.mode_data.update_plot(data)


    def end_iplot(self):
        """
        Calls the function that finalizes interactive plot.
        """
        self.mode_data.end_iplot()


    def fill_cell(self, row, col, value):
        """
        Fills the cell at position [row][col] with value.
        +1 represents filled cell.
        -1 represents empty cell.
         0 represents yet unknown cell.

         Keeps track of nonogram metadata.

        Return:
        -------
        sth_changed - bool variable informing if cell state has been changed
        """
        # filling cell
        self.data.fill_cell(self, row, col, value)
        # updating nonogram metadata
        self.meta_data.progress_tracker.filled_cell(row, col)


    def show_basic_hint(self, row, col):
        """
        Prints basic hint about next cell to be filled.
        """
        if self.mode_data.get_verbosity():
            if self.meta_data.is_transposed():
                print('Analyze column ' + str(row) + '.')
            else:
                print('Analyze row ' + str(row) + '.')
        else:
            if self.meta_data.is_transposed():
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

        if self.mode_data.get_verbosity():
            values = {-1:'empty.', 1:'filled.'}
            print("Cell at row=" + str(row+1) + " and col=" + str(col+1) +
                  " may be deduced to be " + values[value])
            #if self.hinter == 'assumption_making':
            #    print('You will need to analyze more than just single row or column.')
        quit()
