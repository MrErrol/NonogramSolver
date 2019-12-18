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