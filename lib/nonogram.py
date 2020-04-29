from copy import copy, deepcopy

# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from utils.visualizers import plot, update_plot, end_iplot
from utils.tools import print_complain, show_basic_hint, \
    show_basic_hint_assumption, show_explicit_hint
from utils.read_from_file import read_datafile, read_presolved_datafile,\
    structure_raw_cells, strip_trailing_empty_cells, transpose_rows


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


    def __init__(self, filename=None, presolved=None):
        if filename is None:
            self.rows = [[]]
            self.cols = [[]]
            self.row_hints = [[]]
            self.col_hints = [[]]
        else:
            self.row_hints, self.col_hints = read_datafile(filename)
            if presolved is None:
                raw_rows = [[0] * len(self.col_hints)] * len(self.row_hints)
            else:
                raw_rows = read_presolved_datafile(presolved)
            self.rows = structure_raw_cells(raw_rows)
            self.cols = transpose_rows(self.rows)

        if not self.self_consistency_check():
            print_complain()
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
        number_of_pixels_in_rows = sum([sum(row) for row in self.row_hints])
        # number of filled cells in columns
        number_of_pixels_in_cols = sum([sum(col) for col in self.col_hints])
        if number_of_pixels_in_rows != number_of_pixels_in_cols:
            return False

        return True


    def transpose(self):
        """
        Exchanges rows with columns.
        """
        self.row_hints, self.col_hints = self.col_hints, self.row_hints
        self.rows, self.cols = self.cols, self.rows


    def copy(self):
        """
        Function makes a copy of a class instance.
        Copied class share common hints with the original one.
        """
        new_data = Data()
        new_data.row_hints = self.row_hints
        new_data.col_hints = self.col_hints
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


    def get_row_hints(self, row=None, block_index=None):
        """
        Return hints for rows.
        get_row_hints()    - returns all of them
        get_row_hints(row) - returns hints for a given row
        get_row_hints(row, block_index) - returns hints for
        a given block in a given row
        """
        if row is None:
            return self.row_hints
        elif block_index is None:
            return self.row_hints[row]
        else:
            return self.row_hints[row][block_index]


    def get_col_hints(self, col=None, block_index=None):
        """
        Return hints for columns.
        get_col_hints()    - returns all of them
        get_col_hints(col) - returns hints for a given column
        get_col_hints(col, block_index) - returns hints for
        a given block in a given column
        """
        if col is None:
            return self.col_hints
        elif block_index is None:
            return self.col_hints[col]
        else:
            return self.col_hints[col][block_index]


    def get_row(self, row=None, col=None):
        """
        Return rows of cells of a nonogram.
        get_row()    - returns all nonogram cells
        get_row(row) - returns only given row
        get_row(row, col) - returns single cell
        """
        if row is None:
            return self.rows
        elif col is None:
            return self.rows[row]
        else:
            return self.rows[row][col]


    def get_col(self, col=None, row=None):
        """
        Return columns of cells of a nonogram.
        get_col()    - returns all nonogram cells
        get_col(col) - returns only given column
        get_col(col, col) - returns single cell
        """
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


    def __init__(self, row_hints=None, col_hints=None):
        if (row_hints is None) or (col_hints is None):
            self.row_block_origins = [[]]
            self.row_block_endings = [[]]
            self.col_block_origins = [[]]
            self.col_block_endings = [[]]
        else:
            self.row_block_origins = [[0] * len(hints) for hints in row_hints]
            self.col_block_origins = [[0] * len(hints) for hints in col_hints]
            self.row_block_endings = [[len(col_hints) - 1] * len(hints) \
                                    for hints in row_hints]
            self.col_block_endings = [[len(row_hints) - 1] * len(hints) \
                                    for hints in col_hints]


    def copy(self):
        """
        Returns a deepcopy of a class.
        """
        return deepcopy(self)


    def transpose(self):
        """
        Exchanges rows with columns.
        """
        self.row_block_origins, self.col_block_origins = \
            self.col_block_origins, self.row_block_origins
        self.row_block_endings, self.col_block_endings = \
            self.col_block_endings, self.row_block_endings


    def get_row_origins(self, row, block_index=None):
        """
        Returns deduced minimal origins of blocks in rows.
        get_row_origins() - returns all of them
        get_row_origins(row) - returns origins for a given row
        get_row_origins(row, block_index) - returns origin for a given block
        """
        if block_index is None:
            return self.row_block_origins[row]
        else:
            return self.row_block_origins[row][block_index]


    def get_row_endings(self, row, block_index=None):
        """
        Returns deduced maximal endings of blocks in rows.
        get_row_endings() - returns all of them
        get_row_endings(row) - returns endings for a given row
        get_row_endings(row, block_index) - returns ending for a given block
        """
        if block_index is None:
            return self.row_block_endings[row]
        else:
            return self.row_block_endings[row][block_index]


    def get_col_origins(self, col, block_index=None):
        """
        Returns deduced minimal origins of blocks in columns.
        get_col_origins() - returns all of them
        get_col_origins(col) - returns origins for a given column
        get_col_origins(col, block_index) - returns origin for a given block
        """
        if block_index is None:
            return self.col_block_origins[col]
        else:
            return self.col_block_origins[col][block_index]


    def get_col_endings(self, col, block_index=None):
        """
        Returns deduced maximal endings of blocks in columns.
        get_col_endings() - returns all of them
        get_col_endings(col) - returns endings for a given column
        get_col_endings(col, block_index) - returns ending for a given block
        """
        if block_index is None:
            return self.col_block_endings[col]
        else:
            return self.col_block_endings[col][block_index]


    def set_row_origins(self, row, new_origins):
        """
        Updates minimal origins of blocks in a given row.
        """
        self.row_block_origins[row] = new_origins


    def set_col_origins(self, row, new_origins):
        """
        Updates minimal origins of blocks in a given column.
        """
        self.col_block_origins[row] = new_origins


    def set_row_endings(self, row, new_endings):
        """
        Updates maximal endings of blocks in a given row.
        """
        self.row_block_endings[row] = new_endings


    def set_col_endings(self, row, new_endings):
        """
        Updates maximal endings of blocks in a given column.
        """
        self.col_block_endings[row] = new_endings


class ProgressTracker:
    """
    Class containing progress data of the solver:
    - rows changed since last reset
    - columns changed since last reset
    - number of undetermind cells
    """
    def __init__(self, nRows, nCols):
        self.rows_changed = set(range(nRows))
        self.cols_changed = set(range(nCols))
        self.undetermind = nRows * nCols


    def transpose(self):
        """
        Exchanges rows with columns.
        """
        self.rows_changed, self.cols_changed = \
            self.cols_changed, self.rows_changed


    def copy(self):
        """
        Returns deepcopy of itself.
        """
        return deepcopy(self)


    def filled_cell(self, row, col):
        """
        Updates metadata after filling the cell at position (row, col).
        """
        self.rows_changed.add(row)
        self.cols_changed.add(col)
        self.undetermind -= 1


    def reset_changed_rows_and_cols(self):
        """
        Resets counter of changed rows and columns.
        """
        self.rows_changed = set()
        self.cols_changed = set()


    def mark_row_as_changed(self, row):
        """
        Adds row to collection of changed rows.
        """
        self.rows_changed.add(row)


    def mark_col_as_changed(self, col):
        """
        Adds column to collection of changed columns.
        """
        self.cols_changed.add(col)


    def get_rows_changed(self):
        """
        Returns rows changed since last reset.
        """
        return self.rows_changed


    def get_cols_changed(self):
        """
        Returns columns changed since last reset.
        """
        return self.cols_changed


    def get_number_of_undetermind_cells(self):
        """
        Returns number of (yet) undetermind cells.
        """
        return self.undetermind


    def anything_improved(self):
        """
        Checks whether there is any row or column marked as changed since last reset.

        Returns:
        sth_changed - bool variable
        """
        return self.rows_changed != set() or self.cols_changed != set()


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


    def __init__(self, wait=None, verbosity=-1):
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


    def end_iplot(self, data):
        """
        Finalizes interactive plot.
        Plot is updated before finalization.
        """
        self.update_plot(data)
        end_iplot()


    def is_interactive_plot_active(self):
        """
        Informs whether interactive plot is started.
        """
        return bool(self.fig)


    def get_verbosity(self):
        """
        Returns verbosity for hinter mode.
        """
        return self.verbosity


    def set_verbosity(self, verbosity):
        """
        Sets verbosity for hinter mode.
        """
        self.verbosity = verbosity


class Nonogram:
    """
    Class that holds all data about given nonogram.
    All the interaction with subclasses (except for getters) should be done via
    methods of this class.
    """


    def __init__(self, filename=None, presolved=None, wait=0.0, verbosity=-1):
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
        nono.data = self.data.copy()
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
        data = self.get_picture_data()
        self.mode_data.end_iplot(data)


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
        # special case for hinter mode
        # no cell is filled, just hint printed and program quits
        if self.mode_data.get_verbosity() >= 0:
            self.show_hint_simple(row, col, value)

        # filling cell
        sth_changed = self.data.fill_cell(row, col, value)
        if sth_changed:
            # updating nonogram metadata
            self.meta_data.progress_tracker.filled_cell(row, col)
        return sth_changed


    def show_hint_simple(self, row, col, value):
        """
        Prints information about next cell to be filled.
        Shifts index to counting from 1.
        Should be called by deductions based on a single row.
        """
        show_basic_hint(row + 1, self.meta_data.is_transposed())

        if self.mode_data.get_verbosity():
            show_explicit_hint(row, col, value, self.meta_data.is_transposed())
        quit()


    def show_hint_advanced(self, row, col, value):
        """
        Prints information about next cell to be filled.
        Shifts index to counting from 1.
        Should be called by deductions based on assumption making.
        """
        show_basic_hint_assumption(row, col, self.meta_data.is_transposed())

        if self.mode_data.get_verbosity():
            show_explicit_hint(row, col, value, self.meta_data.is_transposed())
            print('You will need to analyze more than just single row or column.')
        quit()
