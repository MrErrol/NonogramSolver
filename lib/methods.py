from copy import copy


def push_block_Origins(hints, blockOrigins, index=0, exh=False):
    """
    Function updates minimal position of block origins starting from NEXT to
    given block index.
    Function uses only the simplest distance condition.
    It does NOT check the row/column state!

    Returns
    -------
    sth_changed - bool variable
    blockOrigins - copy of (possibly updated) block origins
    """
    blockOrigins = copy(blockOrigins)
    # Storing information whether function deduced anything new
    sth_changed = False

    i = index
    while i+1 < len(hints):
        minimalNextBlockPosition = blockOrigins[i] + hints[i] + 1
        i += 1
        if  blockOrigins[i] < minimalNextBlockPosition:
            blockOrigins[i] = minimalNextBlockPosition
            sth_changed = True
            continue

        if not exh:
            break

    return sth_changed, blockOrigins


def push_block_Endings(hints, blockEndings, index=0, exh=False):
    """
    Function updates minimal position of block endings starting from NEXT to
    given block index.
    Function uses only the simplest distance condition.
    It does NOT check the row/column state!

    Returns
    -------
    sth_changed - bool variable
    blockOrigins - copy of (possibly updated) block origins
    """
    # Reversing line (extra empty cell removed from the end and put at the end)
    blockOrigins = [blockEndings[-1] - ending for ending in blockEndings[::-1]]

    # Solving equivalent problem with reversed line
    sth_changed, blockOrigins = push_block_Origins(hints[::-1], blockOrigins,
                                                   index=index, exh=exh)

    # Reversing back obtained solution
    blockEndings = [blockEndings[-1] - origin for origin in blockOrigins[::-1]]

    return sth_changed, blockEndings


def pull_single_block_origin(line, hints, blockOrigins, blockIndex):
    """
    Function pulls given block by a filled cell.
    Does not check whether such a cell exists.

    WARNING!
    Function will modify provided blockOrigins.

    Returns:
    blockOrigins - updated blockOrigins
    """
    # renamed to make code more clear
    i = blockIndex
    # cells between given and following blocks
    cells = line[blockOrigins[i] + hints[i] : blockOrigins[i + 1]]
    # shift stores distance of pulling cell from the next block origin
    shift = cells[::-1].index(1)
    # blockOrigins[i + 1] - blockOrigins[i] is a free space
    # hints[i] + shift is the maximal distance of the block origin from next block origin
    # difference of the two above gives desired shift of the block origin
    shift = blockOrigins[i + 1] - blockOrigins[i] - hints[i] - shift
    blockOrigins[i] += shift
    return blockOrigins


def pull_block_origins(line, hints, blockOrigins):
    """
    Function tries to pull further blockOrigins by filled cells that do not
    belong to the next block.
    Function should be used only by the function deduce_new_block_origins as it
    performs more complete analysis.

    WARNING!
    Function will modify provided blockOrigins.

    Returns:
    --------
    sth_changed - bool variable informing whether anything new has been deduced
    blockOrigins - updated blockOrigins
    """
    sth_changed = False
    i = len(hints) - 1

    # Adding virtual block for sake of simplicity of procedure that measures distance
    blockOrigins += [len(line)]

    # backward loop
    while i >= 0:
        # Checking if there is a filled cell to pull block origin
        if 1 in line[blockOrigins[i] + hints[i] : blockOrigins[i + 1]]:
            # pulling the block
            blockOrigins = pull_single_block_origin(line, hints, blockOrigins, i)
            # pushing following blocks origins further away
            dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
            sth_changed = True
        i -= 1

    # removing virtual block
    del blockOrigins[-1]

    return sth_changed, blockOrigins


def check_no_empty_cell_inside(line, hints, blockOrigins, blockIndex):
    """
    Functions check whether there are empty cells inside the most left available
    position for the i-th block and shifts the block origin if there is at least
    one.

    Returns:
    --------
    sth_changed - bool variable informing whether block Origins has been changed
    blockOrigins - (possibly updated) block Origins
    """
    sth_changed = False
    # for compactness
    i = blockIndex

    required_cells = line[blockOrigins[i]:blockOrigins[i] + hints[i]]
    if -1 in required_cells:
        blockOrigins[i] += hints[i] - required_cells[::-1].index(-1)
        # pushing following blocks origins further away
        dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
        sth_changed = True

    return sth_changed, blockOrigins


def check_no_filled_cell_just_after_block(line, hints, blockOrigins, blockIndex):
    """
    Functions check whether there is filled cell just after the most left
    available position for the i-th block and shifts the block origin by 1
    if there is at least one.

    Returns:
    --------
    sth_changed - bool variable informing whether block Origins has been changed
    blockOrigins - (possibly updated) block Origins
    """
    sth_changed = False
    # for compactness
    i = blockIndex

    if line[blockOrigins[i] + hints[i]] == 1:
        blockOrigins[i] += 1
        # pushing following blocks origins further away
        dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
        sth_changed = True

    return sth_changed, blockOrigins


def deduce_new_block_origins(line, hints, blockOrigins):
    """
    Function tries to deduce higher than given block origins for a single given
    line.

    Returns:
    --------
    sth_changed - bool variable
    blockOrigins - copy of (possibly updated) block origins
    """
    blockOrigins = copy(blockOrigins)
    # Storing information whether function deduced anything new
    sth_changed = False

    # forward loop
    i = 0
    while i < len(hints):
        # Situation when there is filled cell just before the block need not to
        # be checked, due to use of push_block_Origins

        # check for empty space blocking placing
        changed1, blockOrigins = check_no_empty_cell_inside(
            line, hints, blockOrigins, i,
        )

        # check for filled space enforcing push of block origin
        changed2, blockOrigins = check_no_filled_cell_just_after_block(
            line, hints, blockOrigins, i,
        )

        if changed1 or changed2:
            sth_changed = True
        else:
            i += 1

    # backward loop analysis
    changed, blockOrigins = pull_block_origins(line, hints, blockOrigins)
    sth_changed = sth_changed or changed

    return sth_changed, blockOrigins


def deduce_new_block_endings(line, hints, blockEndings):
    """
    Function tries to deduce lower than given block endings for a single given line.

    Returns:
    --------
    sth_changed - bool variable
    blockEndings - copy of (possibly updated) block endings
    """
    # Reversing line (extra empty cell removed from the end and put at the end)
    newline = copy(line[-2::-1] + [-1])
    blockOrigins = [len(newline) - 2 - ending for ending in blockEndings[::-1]]

    # Solving equivalent problem with reversed line
    sth_changed, blockOrigins = deduce_new_block_origins(newline, hints[::-1],
                                                         blockOrigins)

    # Reversing back obtained solution
    blockEndings = [len(newline) - 2 - origin for origin in blockOrigins[::-1]]

    return sth_changed, blockEndings


def fill_range_in_row(nonogram, row, cols, value):
    """
    Fills range of cells in given row with value.

    Parameters:
    -----------
    nonogram - Nonogram to be updated
    row - index of row to be updated
    cols - iterable indices of cells in row to be updated
    value - value to be written into cells

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has changed
    """
    sth_changed = False

    for col in cols:
        change = nonogram.fill_cell(row, col, value)
        sth_changed = sth_changed or change

    return sth_changed


def fill_inside_of_the_blocks(nonogram, row):
    """
    Function fills inside the blocks that are limited to area smaller than
    twice their size.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has changed
    """
    hints = nonogram.data.get_row_hints(row)
    endings = nonogram.limits.get_row_endings(row)
    origins = nonogram.limits.get_row_origins(row)

    sth_changed = False

    for i, hint in enumerate(hints):
        cols = range(endings[i] + 1 - hint, origins[i] + hint)
        changed = fill_range_in_row(nonogram, row, cols, 1)
        sth_changed = sth_changed or changed

    return sth_changed


def fill_between_the_blocks(nonogram, row):
    """
    Function marks as empty area between two blocks.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has changed
    """
    hints = nonogram.data.get_row_hints(row)
    endings = nonogram.limits.get_row_endings(row)
    origins = nonogram.limits.get_row_origins(row)

    sth_changed = False

    for i in range(len(hints) - 1):
        cols = range(endings[i] + 1, origins[i+1])
        changed = fill_range_in_row(nonogram, row, cols, -1)
        sth_changed = sth_changed or changed

    return sth_changed


def fill_beggining_of_the_row(nonogram, row):
    """
    Function marks as empty area before first block.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has changed
    """
    origin = nonogram.limits.get_row_origins(row, 0)
    sth_changed = fill_range_in_row(nonogram, row, range(origin), -1)
    return sth_changed


def fill_end_of_the_row(nono, row):
    """
    Function marks as empty area after last block.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has changed
    """
    ending = nono.limits.get_row_endings(row, -1)
    sth_changed = fill_range_in_row(nono, row,
                                    range(ending + 1, nono.meta_data.n_cols),
                                    -1)
    return sth_changed


def fill_row(nono, row):
    """
    Function tries to fill/mark as empty each cell in the pointed row based on
    actual knowledge.
    Filling in columns should be done by transposing nonogram.

    Parameters:
    -----------
    nono - Nonogram class instance to be updated
    row - index of a row to be checked

    Returns:
    --------
    sth_changed - bool variable
    """
    # Filling inside the blocks
    changed_1 = fill_inside_of_the_blocks(nono, row)
    # Marking as empty beggining of the line
    changed_2 = fill_beggining_of_the_row(nono, row)
    # Marking as empty end of the line
    changed_3 = fill_end_of_the_row(nono, row)
    # Marking as empty area between blocks
    changed_4 = fill_between_the_blocks(nono, row)

    sth_changed = changed_1 or changed_2 or changed_3 or changed_4

    # if nonogram is in the interactive mode, update plot
    if nono.mode_data.is_interactive_plot_active() and sth_changed:
        nono.update_plot()

    return sth_changed


def find_min_block_length(nonogram, row, cell_position):
    """
    Function return minimal length of the block that may cover cell at cell_position.

    Returns:
    --------
    min_length - minimal length of the block that may cover chosen cell
    """
    # indices of blocks that may cover chosen position
    indices_origins = [
        index for index, value \
        in enumerate(nonogram.limits.get_row_origins(row)) \
        if value <= cell_position
    ]
    indices_endings = [
        index for index, value \
        in enumerate(nonogram.limits.get_row_endings(row)) \
        if value >= cell_position
    ]
    # intersection of both sets
    indices = set(indices_origins) & set(indices_endings)
    block_lengths = [nonogram.data.get_row_hints(row, index) for index in indices]
    return min(block_lengths)


def fill_cells_to_the_right(nonogram, row, col):
    """
    Function used by analyze_multi_block_relations_in_row().
    It tries to fill cells to the right from filled cell, when structures like:
    [ ... , -1 , ... , 1 , 0 , ...]
    appear.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = False

    # leeway stores a number of fillable cells to the left
    # -1 at the end returns length of line, when there is no true empty cell
    left_cells = nonogram.data.get_row(row)[:col]
    leeway = (left_cells[::-1]+[-1]).index(-1)

    block_length = find_min_block_length(nonogram, row, col)

    # filling cells enforced by minimal block length
    for position in range(col + 1, col + block_length - leeway):
        nonogram.fill_cell(row, position, 1)
        sth_changed = True

    return sth_changed


def fill_cells_to_the_left(nonogram, row, col):
    """
    Function used by analyze_multi_block_relations_in_row().
    It tries to fill cells to the left from filled cell, when structures like:
    [ ... , 0 , 1 , ... , -1 , ...]
    appear.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = False

    # leeway stores a number of fillable cells to the right
    # -1 at the end returns length of line, when there is no true empty cell
    right_cells = nonogram.data.get_row(row)[col+1:]
    leeway = (right_cells + [-1]).index(-1)

    block_length = find_min_block_length(nonogram, row, col)

    # filling cells enforced by minimal block length
    for position in range(col + leeway + 1 - block_length, col):
        nonogram.fill_cell(row, position, 1)
        sth_changed = True

    return sth_changed


def analyze_multi_block_relations_in_row(nonogram, row):
    """
    Function analyzes regions of overlapping blocks in the row trying to fill
    some cells.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = False

    # filled line case
    if not 0 in nonogram.data.get_row(row):
        return False

    # loop over cells in row
    for col in range(1, nonogram.meta_data.get_number_of_cols()):
        # filling in right direction
        if nonogram.data.get_row(row, col) == 1 and nonogram.data.get_row(row, col+1) == 0:
            changed = fill_cells_to_the_right(nonogram, row, col)
            sth_changed = sth_changed or changed

        # filling in left direction
        if nonogram.data.get_row(row, col) == 1 and nonogram.data.get_row(row, col-1) == 0:
            changed = fill_cells_to_the_left(nonogram, row, col)
            sth_changed = sth_changed or changed

    return sth_changed


def analyze_multi_block_relations(nonogram):
    """
    Function analyzes regions of overlapping blocks in the whole nonogram
    trying to fill some cells.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = False

    # loop over nonogram dimensions (rows and columns)
    for dummy_dimension in range(2):
        # loop over nonogram rows (columns)
        for row in range(nonogram.meta_data.get_number_of_rows()):
            sth_changed_loc = analyze_multi_block_relations_in_row(nonogram, row)
            sth_changed = sth_changed or sth_changed_loc
        nonogram.transpose()

    return sth_changed
