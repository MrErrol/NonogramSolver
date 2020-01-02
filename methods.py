from nonogram import Nonogram
from copy import copy

def push_block_Origins(hints, blockOrigins, index=0):
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
        if blockOrigins[i+1] < blockOrigins[i] + hints[i] + 1:
            blockOrigins[i+1] = blockOrigins[i] + hints[i] + 1
            sth_changed = True
            i += 1
        else:
            break
    return sth_changed, blockOrigins

def push_block_Endings(hints, blockEndings, index=0):
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
    sth_changed, blockOrigins = push_block_Origins(hints[::-1], blockOrigins, index=index)
    
    # Reversing back obtained solution
    blockEndings = [blockEndings[-1] - origin for origin in blockOrigins[::-1]]
    
    return sth_changed, blockEndings

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
        # Checking if there is enough space for the block and following empty cell
        if not -1 in line[blockOrigins[i]:blockOrigins[i]+hints[i]] and not line[blockOrigins[i]+hints[i]] == 1:
            i += 1
            continue
        # Situation when there is empty cell blocking place
        elif -1 in line[blockOrigins[i]:blockOrigins[i]+hints[i]]:
            shift = line[blockOrigins[i]:blockOrigins[i]+hints[i]][::-1].index(-1)
            shift = hints[i] - shift
            blockOrigins[i] += shift
            # pushing following blocks origins further away
            dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
            sth_changed = True
            continue
        # Situation when there is filled cell just after place for the block
        else:
            blockOrigins[i] += 1
            # pushing following blocks origins further away
            dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
            sth_changed = True
            continue
        
    # backward loop
    i = len(hints) - 1
    while i >= 0:
        # Checking if there is a filled cell to pull block origin
        try:
            if 1 in line[blockOrigins[i]+hints[i]:blockOrigins[i+1]]:
                shift = line[blockOrigins[i]+hints[i]:blockOrigins[i+1]][::-1].index(1)
                shift = blockOrigins[i+1] - blockOrigins[i] - hints[i] - shift
                blockOrigins[i] += shift
                # pushing following blocks origins further away
                dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
                sth_changed = True
        except:
            # last block exception
            if 1 in line[blockOrigins[i]+hints[i]:]:
                shift = line[blockOrigins[i]+hints[i]:][::-1].index(1)
                shift = len(line[blockOrigins[i]+hints[i]:]) - shift
                blockOrigins[i] += shift
                # pushing following blocks origins further away
                dummy, blockOrigins = push_block_Origins(hints, blockOrigins, index=i)
                sth_changed = True
        i -= 1
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

def fill_row(nono, row):
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
    sth_changed = False
    
    # Marking as empty beggining of the line
    for j in range( origins[0] ):
        change =  nono.fill_cell(row, j, -1)
        sth_changed = sth_changed or change

    # Marking as empty end of the line
    for j in range( endings[-1] + 1 , nono.nCols ):
        change = nono.fill_cell(row, j, -1)
        sth_changed = sth_changed or change
    
    for i in range(len(hints)):
        
        # Filling inside the block
        if endings[i] - origins[i] < 2*hints[i] - 1 :
            for j in range( endings[i] + 1 - hints[i] , origins[i] + hints[i] ):
                change = nono.fill_cell(row, j, 1)
                sth_changed = sth_changed or change
        
        # Marking as empty area between blocks
        if i + 1 < len(hints):
            if endings[i] + 1 < origins[i+1] :
                for j in range( endings[i] + 1 , origins[i+1] ):
                    change = nono.fill_cell(row, j, -1)
                    sth_changed = sth_changed or change
    
    return sth_changed
    
    
    