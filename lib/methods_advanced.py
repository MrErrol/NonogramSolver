from lib.methods import deduce_new_block_origins, deduce_new_block_endings, push_block_Origins, push_block_Endings, fill_row

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
            del rows[0]
            # to prevent calling last element of empty list
            try:
                del rows[-1]
            except:
                break
        
        # transposing nonogram for dimension loop
        nonogram.transpose()
    
    return sth_changed
    
