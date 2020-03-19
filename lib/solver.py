from copy import copy
import lib.methods as methods
import lib.methods_advanced as advanced
from utils.tools import print_failure_statement


def perform_good_start(nono):
    # Simple beggining, gives nice block limits initialization and usually even
    # fills some cells
    for i in range(2):
        for row in range(nono.nRows):
            sth_changed, nono.rowBlockOrigins[row] = methods.push_block_Origins(
                nono.rowHints[row],
                nono.rowBlockOrigins[row],
                index=0,
                )
            sth_changed, nono.rowBlockEndings[row] = methods.push_block_Endings(
                nono.rowHints[row],
                nono.rowBlockEndings[row],
                index=0,
                )
            methods.fill_row(nono, row)
        nono.transpose()


def perform_simple_deducing_for_single_row(nono, row):
    """
    Function tries to deduce new block limits for a single row of nonogram.
    If succeeded it appropriately updates them in the nonogram class.
    """
    sth_changed_1, origins = methods.deduce_new_block_origins(
        nono.rows[row],
        nono.rowHints[row],
        nono.rowBlockOrigins[row],
    )
    sth_changed_2, endings = methods.deduce_new_block_endings(
        nono.rows[row],
        nono.rowHints[row],
        nono.rowBlockEndings[row],
    )
    if sth_changed_1 or sth_changed_2:
        nono.rowBlockOrigins[row] = origins
        nono.rowBlockEndings[row] = endings
        nono.rowsChanged.add(row)
        methods.fill_row(nono, row)


def perform_simple_deducing(nono, rowsChanged_input, colsChanged_input):
    """
    Function performs simple deducing over rows and columns of nonogram provided
    as the arguments of the function. Deduction is simple in the sens that:
    - it treats every row/column separately
    - it includes block relations only between neighbouring blocks
    """
    rowsChanged = rowsChanged_input
    colsChanged = colsChanged_input
    # Loop over Nonogram dimensions (rows and columns)
    for i in range(2):
        # Loop over Nonogram rows (columns if transposed)
        for row in rowsChanged:
            # Deduction over single row
            perform_simple_deducing_for_single_row(nono, row)
        nono.transpose()
        rowsChanged, colsChanged = colsChanged, rowsChanged


def make_single_iteration_of_deduction(nono, rowsChanged, colsChanged,
                                       searching_depth=2,
                                       interactive=False,
                                       ):
    """
    Performs single iteration of deduction. May use all implemented methods,
    yet stops after the cheapest finds solution.
    """
    # Simple and cheap deduction - does most of the work
    perform_simple_deducing(nono, rowsChanged, colsChanged)

    # Check if anything improved
    if nono.rowsChanged == set() and nono.colsChanged == set():
        # Calling advanced, more costly function
        methods.analyze_multi_block_relations(nono)

    # Check if anything improved
    if nono.rowsChanged == set() and nono.colsChanged == set():
        # Calling advanced, even more costly function
        advanced.search_for_assumptions(nono, searching_depth=searching_depth)


def solver(nono, searching_depth=2):
    """
    Main solver of the nonogram. Uses all implemented methods iteratively until
    nonogram is solved or there is no improvement.

    Returns:
    cycle - number of cycles spent to solve nonogram
    """
    # Gives nice block limits initialization
    perform_good_start(nono)

    cycle = 0 
    # main loop
    while nono.undetermind:
        # Stores basic information about improvements since last cycle
        rowsChanged = copy(nono.rowsChanged)
        colsChanged = copy(nono.colsChanged)
        nono.rowsChanged = set()
        nono.colsChanged = set()

        # Performs cheapest deduction possible
        make_single_iteration_of_deduction(
            nono, rowsChanged, colsChanged,
            searching_depth=searching_depth,
        )

        # Check if anything improved
        if nono.rowsChanged == set() and nono.colsChanged == set():
            print_failure_statement(cycle)
            return cycle

        cycle += 1

    return cycle
