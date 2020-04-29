from copy import copy
from lib.methods import deduce_new_block_origins, deduce_new_block_endings,\
    push_block_origins, push_block_endings, fill_row


def check_if_line_is_fillable(line, hints, block_origins, block_endings):
    """
    Function performs few simple checks if it is possible to fill the line
    according to actual knowledge. It may misclassify unfillable row
    as fillable, but not fillable as unfillable.

    Returns:
    --------
    bool - bool variable answearing the question whether line is fillable
    """
    # add virtual block at the end, just to simplify comparison
    block_origins = copy(block_origins)
    block_origins.append(len(line) + 1)

    # Check if there are filled cells before the first block
    if 1 in line[:block_origins[0]]:
        return False

    # loop over blocks
    for i, hint in enumerate(hints):
        # check if there is enough space for a block
        if block_endings[i] - block_origins[i] + 1 < hint:
            return False

        # check if there are filled cells between blocks (or after last block)
        if 1 in line[block_endings[i] + 1 : block_origins[i+1]]:
            return False

    # No problems found
    return True


def safe_deduce(nono, row):
    """
    Function used while making assumptions to find discrepancy in considered
    nonogram.
    Function being safe means that it will not raise Exception while handling
    incorrect nonogram.

    Returns:
    --------
    found_discrepancy - bool variable informing whether discrepancy has been found
    """
    try:
        sth_changed1, block_origins = deduce_new_block_origins(
            nono.data.get_row(row),
            nono.data.get_row_hints(row),
            nono.limits.get_row_origins(row),
            )
        sth_changed2, block_endings = deduce_new_block_endings(
            nono.data.get_row(row),
            nono.data.get_row_hints(row),
            nono.limits.get_row_endings(row),
            )
    except:
        return True
    if sth_changed1 or sth_changed2:
        nono.limits.set_row_origins(row, block_origins)
        nono.limits.set_row_endings(row, block_endings)
        try:
            fill_row(nono, row)
        except:
            return True
    return False


def make_deduction(nono):
    """
    Function deduces new information about cells for 2 iterations.
    Designed to be used after making assumption, not for casual solving.

    Returns:
    --------
    bool - bool variable informing whether discrepancy has been found
    """
    # Loop determining the analysis depth
    # Range - 2*depth, where 2 stands for transposition that is going
    # through rows and columns separately
    for dummy_checking_depth in range(2*2):
        # Loop over previously changed rows (or columns)
        for row in nono.meta_data.progress_tracker.get_rows_changed():
            # perform deduction and report possible problems
            if safe_deduce(nono, row):
                # discrepancy found
                return True
        nono.transpose()
    # no discrepancy found yet
    return False


def make_assumption(nonogram, row, col):
    """
    The function makes assumption that cell at position (row, col) is filled
    and tries to find discrepancy.
    The function does not change nonogram as it work on it's copy.

    Returns:
    --------
    bool - bool variable answearing the question if the cell may be filled
    """
    nono = nonogram.copy()
    nono.meta_data.progress_tracker.reset_changed_rows_and_cols()
    # Our assumption
    nono.fill_cell(row, col, 1)

    if make_deduction(nono):
        return False

    # Loops verifying all modified rows
    for row_iter in nono.meta_data.progress_tracker.get_rows_changed():
        if not check_if_line_is_fillable(nono.data.get_row(row_iter),
                                         nono.data.get_row_hints(row_iter),
                                         nono.limits.get_row_origins(row_iter),
                                         nono.limits.get_row_endings(row_iter),
                                        ):
            return False

    # Loops verifying all modified columns
    for col_iter in nono.meta_data.progress_tracker.get_cols_changed():
        if not check_if_line_is_fillable(nono.data.get_col(col_iter),
                                         nono.data.get_col_hints(col_iter),
                                         nono.limits.get_col_origins(col_iter),
                                         nono.limits.get_col_endings(col_iter),
                                        ):
            return False

    # No internal discrepancy found
    return True

def push_limits_within_a_row(nono, row):
    """
    Function pushes all block origins and endings within given row as far
    as possible.
    """
    changed_origins, new_origins = push_block_origins(
        nono.data.get_row_hints(row),
        nono.limits.get_row_origins(row),
        exh=True,
    )
    changed_endings, new_endings = push_block_endings(
        nono.data.get_row_hints(row),
        nono.limits.get_row_endings(row),
        exh=True,
    )

    if changed_origins:
        nono.limits.set_row_origins(row, new_origins)
    if changed_endings:
        nono.limits.set_row_endings(row, new_endings)


def push_everything_from_this_cell(nono, row, col):
    """
    Function pushes all block endings that might be affected be change of
    (row, col) cell state.
    """
    # Loop over nonogram dimensions (rows and columns)
    for dimension in range(2):
        index = col if dimension else row
        push_limits_within_a_row(nono, index)

        nono.transpose()


def investigate_empty_cells_from_left(nono, row, empty_cells):
    """
    Function tries to fill empty_cells in row from the left trying to find
    discrepancy.
    On succes emptifies the cell and proceeds.
    On failure stops.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = False

    for col in empty_cells:
        if not make_assumption(nono, row, col):
            # special call of function showing hint for assumption making mode
            # used only in hint mode (verbotity >= 0)
            if nono.mode_data.get_verbosity() >= 0:
                nono.show_hint_advanced(row, col, -1)
            nono.fill_cell(row, col, -1)
            # Use of pushes after fill_cell is required by deducing functions
            push_everything_from_this_cell(nono, row, col)
            sth_changed = True
        else:
            break

    return sth_changed


def ivestigate_row_with_assumptions(nonogram, row):
    """
    Function tries to cross-out cells at the beggining and at the end of the row
    by making assumptions. If possible updates the state of nonogram.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    # gives indices of empty cells in the row
    def get_empty_cells(nonogram, row):
        return [index for index, value in enumerate(nonogram.data.get_row(row)) if value == 0]

    sth_changed = []
    empty_cells = get_empty_cells(nonogram, row)

    # single forward-backward loop
    for dummy in range(2):
        change = investigate_empty_cells_from_left(nonogram, row, empty_cells)
        sth_changed.append(change)
        # updating and reversing the list to make backward loop
        empty_cells = get_empty_cells(nonogram, row)[::-1]

    return any(sth_changed)


def search_for_assumptions(nonogram, searching_depth=2):
    """
    Function search endings of first searching_depth lines from each border
    for making assumptions. If possible updates the state of nonogram.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = []

    # loop over nonogram dimensions (rows and columns)
    for dummy_dimension in range(2):
        # Finding non-filled rows in nonogram
        rows = [index for index, line in enumerate(nonogram.data.get_row()) if 0 in line]

        # loop over rows truncated by searching_depth
        for dummy_depth in range(searching_depth):
            sth_changed.append(ivestigate_row_with_assumptions(nonogram, rows[0]))
            sth_changed.append(ivestigate_row_with_assumptions(nonogram, rows[-1]))
            del rows[0]
            # to prevent calling element of an empty list
            if not rows:
                break

        # transposing nonogram for dimension loop
        nonogram.transpose()

    return any(sth_changed)
