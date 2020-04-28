from copy import copy
import lib.methods as methods
import lib.methods_advanced as advanced
from utils.tools import print_failure_statement


def perform_good_start(nono):
    """
    Function meaningfully initializes block limits. Usually even fills some cells.
    """
    for dummy_dimension in range(2):
        for row in range(nono.meta_data.get_number_of_rows()):
            advanced.push_limits_within_a_row(nono, row)
            methods.fill_row(nono, row)
        nono.transpose()


def perform_single_row_deduction(nono, row):
    """
    Function tries to deduce new block limits for a single row of nonogram.
    If succeeded it appropriately updates them in the nonogram class.
    """
    origins_changed, new_origins = methods.deduce_new_block_origins(
        nono.data.get_row(row),
        nono.data.get_row_hints(row),
        nono.limits.get_row_origins(row),
    )
    endings_changed, new_endings = methods.deduce_new_block_endings(
        nono.data.get_row(row),
        nono.data.get_row_hints(row),
        nono.limits.get_row_endings(row),
    )
    if origins_changed or endings_changed:
        nono.limits.set_row_origins(row, new_origins)
        nono.limits.set_row_endings(row, new_endings)
        nono.meta_data.progress_tracker.mark_row_as_changed(row)
        methods.fill_row(nono, row)


def perform_simple_deducing(nono, rows_changed_input, cols_changed_input):
    """
    Function performs simple deducing over rows and columns of nonogram provided
    as the arguments of the function. Deduction is simple in the sens that:
    - it treats every row/column separately
    - it includes block relations only between neighbouring blocks
    """
    rows_changed = rows_changed_input
    cols_changed = cols_changed_input
    # Loop over Nonogram dimensions (rows and columns)
    for dummy_dimension in range(2):
        # Loop over Nonogram rows (columns if transposed)
        for row in rows_changed:
            # Deduction over single row
            perform_single_row_deduction(nono, row)
        nono.transpose()
        rows_changed, cols_changed = cols_changed, rows_changed


def single_deduction_iteration(nono, rows_changed, cols_changed,
                               searching_depth,
                              ):
    """
    Performs single iteration of deduction. May use all implemented methods,
    yet stops after the cheapest finds solution.
    """
    # Simple and cheap deduction - does most of the work
    perform_simple_deducing(nono, rows_changed, cols_changed)

    # Check if anything improved
    if not nono.meta_data.progress_tracker.anything_improved():
        # Calling advanced, more costly function
        methods.analyze_multi_block_relations(nono)

    # Check if anything improved
    if not nono.meta_data.progress_tracker.anything_improved():
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
    while nono.meta_data.progress_tracker.get_number_of_undetermind_cells():
        # Stores basic information about improvements since last cycle
        rows_changed = copy(nono.meta_data.progress_tracker.get_rows_changed())
        cols_changed = copy(nono.meta_data.progress_tracker.get_cols_changed())
        nono.meta_data.progress_tracker.reset_changed_rows_and_cols()

        single_deduction_iteration(
            nono, rows_changed, cols_changed, searching_depth,
        )

        # Check if anything improved
        if not nono.meta_data.progress_tracker.anything_improved():
            print_failure_statement(cycle)
            return cycle

        cycle += 1

    return cycle
