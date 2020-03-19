from lib.nonogram import Nonogram
import lib.methods as methods
import lib.methods_advanced as advanced
from copy import copy


def perform_good_start(nono, interactive=False):
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
            methods.fill_row(nono, row, interactive=interactive)
        nono.transpose()


def perform_simple_deducing_for_single_row(nono, row, interactive):
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
        methods.fill_row(nono, row, interactive=interactive)


def perform_simple_deducing(nono, rowsChanged_input, colsChanged_input,
                            interactive=False):
    rowsChanged = rowsChanged_input
    colsChanged = colsChanged_input
    # Loop over Nonogram dimensions (rows and columns)
    for i in range(2):
        # Loop over Nonogram rows (columns if transposed)
        for row in rowsChanged:
            # Deduction over single row
            perform_simple_deducing_for_single_row(nono, row, interactive)
        nono.transpose()
        rowsChanged, colsChanged = colsChanged, rowsChanged


def solver(nono, searching_depth=2, interactive=False):
    # Gives nice block limits initialization
    perform_good_start(nono, interactive=interactive)

    cycle = 0 
    # main loop
    while nono.undetermind:
        # Stores basic information about improvements since last cycle
        rowsChanged = copy(nono.rowsChanged)
        colsChanged = copy(nono.colsChanged)
        nono.rowsChanged = set()
        nono.colsChanged = set()

        # Simple and cheap deduction - does most of the work
        perform_simple_deducing(nono, rowsChanged, colsChanged,
                                interactive=interactive)

        # Check if anything improved
        if nono.rowsChanged == set() and nono.colsChanged == set():
            # Calling advanced, more costly function
            methods.analyze_multi_block_relations(nono)

        # Check if anything improved
        if nono.rowsChanged == set() and nono.colsChanged == set():
            # Calling advanced, even more costly function
            if not advanced.search_for_assumptions(nono,
                                                   searching_depth=searching_depth):
                print("Failed to solve Nonogram.")
                print("Cycle : " + str(cycle))
                return cycle

        cycle += 1

    return cycle
