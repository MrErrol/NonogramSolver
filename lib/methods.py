from lib.nonogram import Nonogram
from copy import copy

def push_block_Origins(hints, blockOrigins, index=0, exh=False):
    """
    Function updates minimal position of block origins starting from NEXT to given block index.
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
        i += 1
        if  blockOrigins[i] < blockOrigins[i-1] + hints[i-1] + 1:
            blockOrigins[i] = blockOrigins[i-1] + hints[i-1] + 1
            sth_changed = True 
            continue
            
        if not exh:
            break
    
    return sth_changed, blockOrigins

def push_block_Endings(hints, blockEndings, index=0, exh=False):
    """
    Function updates minimal position of block endings starting from NEXT to given block index.
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
    sth_changed, blockOrigins = push_block_Origins(hints[::-1], blockOrigins, index=index, exh=exh)
    
    # Reversing back obtained solution
    blockEndings = [blockEndings[-1] - origin for origin in blockOrigins[::-1]]
    
    return sth_changed, blockEndings

def pull_block_origins(line, hints, blockOrigins):
    """
    Function tries to pull further blockOrigins by filled cells that do not belong to the next block.
    Function should be used only by function deduce_new_block_origins as it performs more complete analysis.
    
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
        if 1 in line[blockOrigins[i]+hints[i]:blockOrigins[i+1]]:
            shift = line[blockOrigins[i]+hints[i]:blockOrigins[i+1]][::-1].index(1)
            shift = blockOrigins[i+1] - blockOrigins[i] - hints[i] - shift
            blockOrigins[i] += shift
            # pushing following blocks origins further away
            dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
            sth_changed = True
        i -= 1
    
    # removing virtual block
    del blockOrigins[-1]
    
    return sth_changed, blockOrigins

def deduce_new_block_origins(line, hints, blockOrigins):
    """
    Function tries to deduce higher than given block origins for a single given line.
    
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
        # Situation when there is filled cell just before the block need not te be checked, due to use of push_block_Origins
        required_cells = line[blockOrigins[i]:blockOrigins[i]+hints[i]]
        # Situation when there is empty cell blocking place
        if -1 in required_cells:
            blockOrigins[i] += hints[i] - required_cells[::-1].index(-1)
            # pushing following blocks origins further away
            dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
            sth_changed = True
            continue
        # Situation when there is filled cell just after place for the block
        if line[blockOrigins[i]+hints[i]] == 1:
            blockOrigins[i] += 1
            # pushing following blocks origins further away
            dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
            sth_changed = True
            continue
        # Situation when there is enough space for the block and following empty cell
        else:
            i += 1
            continue
        
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
    sth_changed, blockOrigins = deduce_new_block_origins(newline, hints[::-1], blockOrigins)
    
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
        change =  nonogram.fill_cell(row, col, value)
        sth_changed = sth_changed or change
    
    return sth_changed

def fill_inside_of_the_blocks(nonogram, row):
    """
    Function fills inside the blocks that are limited to area smaller than twice their size.
    
    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has changed
    """
    hints = nonogram.rowHints[row]
    endings = nonogram.rowBlockEndings[row]
    origins = nonogram.rowBlockOrigins[row]
    
    sth_changed = False
    
    for i in range(len(hints)):
        cols = range( endings[i] + 1 - hints[i] , origins[i] + hints[i] )
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
    hints = nonogram.rowHints[row]
    endings = nonogram.rowBlockEndings[row]
    origins = nonogram.rowBlockOrigins[row]
    
    sth_changed = False
    
    for i in range(len(hints) - 1):
        cols = range( endings[i] + 1 , origins[i+1] )
        changed = fill_range_in_row(nonogram, row, cols, -1)
        sth_changed = sth_changed or changed
    
    return sth_changed


def fill_row(nono, row, interactive=False):
    """
    Function tries to fill/mark as empty each cell in the pointed row based on actual knowledge.
    Filling in columns should be done by transposing nonogram.
    
    Parameters:
    -----------
    nono - Nonogram class instance to be updated
    row - index of a row to be checked
    
    Returns:
    --------
    sth_changed - bool variable
    """
    hints = nono.rowHints[row]
    endings = nono.rowBlockEndings[row]
    origins = nono.rowBlockOrigins[row]
    
    # Filling inside the blocks
    changed_1 = fill_inside_of_the_blocks(nono, row)
    # Marking as empty beggining of the line
    changed_2 = fill_range_in_row(nono, row, range( origins[0] ), -1)
    # Marking as empty end of the line
    changed_3 = fill_range_in_row(nono, row, range( endings[-1] + 1 , nono.nCols ), -1)
    # Marking as empty area between blocks
    changed_4 = fill_between_the_blocks(nono, row)
    
    sth_changed = changed_1 or changed_2 or changed_3 or changed_4
    
    if interactive and sth_changed:
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
    indices_o = [index for index, value in enumerate(nonogram.rowBlockOrigins[row]) if value <= cell_position]
    indices_e = [index for index, value in enumerate(nonogram.rowBlockEndings[row]) if value >= cell_position]
    # intersection of both sets
    indices = set(indices_o) & set(indices_e)
    block_lengths = [nonogram.rowHints[row][index] for index in indices]
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
    left_cells = nonogram.rows[row][:col]
    leeway = (left_cells[::-1]+[-1]).index(-1)
    
    block_length = find_min_block_length(nonogram, row, col)
    
    # filling cells enforced by minimal block length
    for position in range( col + 1, col + block_length - leeway ):
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
    right_cells = nonogram.rows[row][col+1:]
    leeway = (right_cells + [-1]).index(-1)
    
    block_length = find_min_block_length(nonogram, row, col)
    
    # filling cells enforced by minimal block length
    for position in range(col + leeway + 1 - block_length , col ):
        nonogram.fill_cell(row, position, 1)
        sth_changed = True
        
    return sth_changed

def analyze_multi_block_relations_in_row(nonogram, row):
    """
    Function analyzes regions of overlapping blocks in the row trying to fill some cells.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = False

    # filled line case
    if not 0 in nonogram.rows[row]:
        return False

    # loop over cells in row
    for col in range(1, len(nonogram.rows[row]) - 1 ):
        # filling in right direction
        if nonogram.rows[row][col] == 1 and nonogram.rows[row][col+1] == 0:
            changed = fill_cells_to_the_right(nonogram, row, col)
            sth_changed = sth_changed or changed
            
        # filling in left direction
        if nonogram.rows[row][col] == 1 and nonogram.rows[row][col-1] == 0:
            changed = fill_cells_to_the_left(nonogram, row, col)
            sth_changed = sth_changed or changed

    return sth_changed

def analyze_multi_block_relations(nonogram):
    """
    Function analyzes regions of overlapping blocks in the whole nonogram trying to fill some cells.

    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = False

    # loop over nonogram dimensions (rows and columns)
    for i in range(2):
        # loop over nonogram rows (columns)
        for row in range(len(nonogram.rows)):
            sth_changed_loc = analyze_multi_block_relations_in_row(nonogram, row)
            sth_changed = sth_changed or sth_changed_loc
        nonogram.transpose()

    return sth_changed

def check_if_line_is_fillable(line, hints, blockOrigins, blockEndings):
    """
    Function performs few simple checks if it is possible to fill the line according to actual knowledge. It may misclassify unfillable row as fillable, but not fillable as unfillable.
    
    Returns:
    --------
    bool - bool variable answearing the question whether line is fillable
    """
    # Check if there are filled cells before the first block
    if 1 in line[:blockOrigins[0]]:
        return False
    # Check if there are filled cells after the last block
    if 1 in line[blockEndings[-1]+1:]:
        return False
    # loop over blocks
    for i in range(len(hints)):
        # check if there is enough space for a block
        if blockEndings[i] - blockOrigins[i] + 1 < hints[i] :
            return False
        # check if there are filled cells between blocks
        try:
            if blockEndings[i] + 1 < blockOrigins[i+1] :
                if 1 in line[ blockEndings[i] + 1 : blockOrigins[i+1] ]:
                    return False
        except:
            # Last block exception
            pass
    # No problems found
    return True

def safe_deduce(nono, row):
    """
    Function used while making assumptions to find discrepancy in considered nonogram.
    Function being safe means that it will not raise Exception while handling incorrect nonogram.
    
    Returns:
    --------
    found_discrepancy - bool variable informing whether discrepancy has been found
    """
    try:
        sth_changed1, blockOrigins = deduce_new_block_origins(nono.rows[row], nono.rowHints[row], nono.rowBlockOrigins[row])
        sth_changed2, blockEndings = deduce_new_block_endings(nono.rows[row], nono.rowHints[row], nono.rowBlockEndings[row])
    except:
        return True
    if sth_changed1 or sth_changed2 :
        nono.rowBlockOrigins[row] = blockOrigins
        nono.rowBlockEndings[row] = blockEndings
        try:
            fill_row(nono, row)
        except:
            return True
    return False

def make_assumption(nonogram, row, col):
    """
    The function makes assumption that cell at position (row, col) is filled and tries to find discrepancy.
    The function does not change nonogram as it work on it's copy.
    
    Returns:
    --------
    bool - bool variable answearing the question if the cell may be filled
    """
    nono = nonogram.copy()
    nono.rowsChanged = set()
    nono.colsChanged = set()
    # Our assumption
    nono.fill_cell(row, col, 1)
    
    # Loop determining the analysis depth
    # Range - 2*depth, 2 stands for transposition - going for rows and columns separately
    for checking_depth in range(2*2):
        # Loop over previously changed rows (or columns)
        for row in nono.rowsChanged:
            found_discr = safe_deduce(nono, row)
            if found_discr:
                return False
            
        nono.transpose()
    
    # Loops verifying all modified rows
    for row in nono.rowsChanged:
        if not check_if_line_is_fillable(nono.rows[row], nono.rowHints[row], nono.rowBlockOrigins[row], nono.rowBlockEndings[row]):
            return False
        
    # Loops verifying all modified columns
    for col in nono.colsChanged:
        if not check_if_line_is_fillable(nono.cols[col], nono.colHints[col], nono.colBlockOrigins[col], nono.colBlockEndings[col]):
            return False
    
    # No internal discrepancy found
    return True

def ivestigate_row_with_assumptions(nonogram, row):
    """
    Function tries to cross-out cells at the beggining and at the end of the row by making assumptions. If possible updates the state of nonogram.
    
    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    # gives indices of empty cells in the row
    def get_empty_cells(nonogram, row):
        return [index for index, value in enumerate(nonogram.rows[row]) if value == 0]
    
    sth_changed = False
    empty_cells = get_empty_cells(nonogram, row)
    
    # single forward-backward loop
    for i in range(2): 
        # investigating firsts (lasts) empty cells in the row
        for col in empty_cells:
            if not make_assumption(nonogram, row, col):
                nonogram.fill_cell(row, col, -1)
                # Use of pushes after fill_cell is required by deducing functions
                dummy, nonogram.rowBlockOrigins[row] = push_block_Origins(nonogram.rowHints[row], nonogram.rowBlockOrigins[row], exh=True)
                dummy, nonogram.rowBlockEndings[row] = push_block_Endings(nonogram.rowHints[row], nonogram.rowBlockEndings[row], exh=True)
                dummy, nonogram.colBlockOrigins[col] = push_block_Origins(nonogram.colHints[col], nonogram.colBlockOrigins[col], exh=True)
                dummy, nonogram.colBlockEndings[col] = push_block_Endings(nonogram.colHints[col], nonogram.colBlockEndings[col], exh=True)
                sth_changed = True
            else:
                break
        # updating and reversing the list to make backward loop
        empty_cells = get_empty_cells(nonogram, row)[::-1]
    
    return sth_changed

def search_for_assumptions(nonogram, searching_depth=1):
    """
    Function search endings of first searching_depth lines from each border for making assumptions. If possible updates the state of nonogram.
    
    Returns:
    --------
    sth_changed - bool variable informing whether nonogram state has been changed
    """
    sth_changed = False
    
    # loop over nonogram dimensions (rows and columns)
    for dim in range(2):
        # Finding non-filled rows in nonogram
        rows = [index for index, line in enumerate(nonogram.rows) if 0 in line]
        depth = 1 # number of lines from edge to be checked 
        
        # loop over rows truncated by searching_depth
        for depth in range(searching_depth):
            sth_changed_1 = ivestigate_row_with_assumptions(nonogram, rows[0])
            sth_changed_2 = ivestigate_row_with_assumptions(nonogram, rows[-1])
            sth_changed = sth_changed_1 or sth_changed_2 or sth_changed
            rows.remove(rows[0])
            # to prevent calling last element of empty list
            try:
                rows.remove(rows[-1])
            except:
                break
        
        # transposing nonogram for dimension loop
        nonogram.transpose()
    
    return sth_changed
    