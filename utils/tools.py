def print_mistakes(mistakes, verbose):
    """
    Prints misclassified cells.
    """
    print("Whoops! You have made a mistake!")
    if verbose:
        print("List of misclassified cells:")
        print("(row_index, column_index)")
        for pair in mistakes:
            print(pair)    

def compare_values(value1, value2):
    """
    Checks whether two values of cells are consistent.
    
    Treats unsolved cell (value = 0) as consistent with any other.
    
    Returns:
    --------
    bool - bool variable informing whether provided values are consistent
    """
    if value1 == 0 or value2 == 0:
        return True
    elif value1 == value2:
        return True
    else:
        return False
        
def compare_tables(rows1, rows2):
    """
    Compares two nonogram cell tables, checking whether there is a discrepancy between their solved cells.
    
    Function is used to verify whether user has made a mistake while (at least) partially solving Nonogram.
    
    Parameters:
    -----------
    nono1 - one of two cell tables to be compared
    nono2 - one of two cell tables to be compared
    
    Returns:
    --------
    mistakes - list of pairs of coordinates of misclassified cells
    """
    mistakes = []

    for row in range(len(rows1)):
        for col in range(len(rows1[0])-1):
            ok = compare_values(rows1[row][col], rows2[row][col])
            if not ok:
                mistakes.append((row, col))

    return mistakes
    
def compare_nonograms(nono1, nono2, verbose=verbose):
    """
    Compares two Nonograms, checking whether there is a discrepancy between their solved cells.
    
    Function is used to verify whether user has made a mistake while (at least) partially solving Nonogram.
    
    Parameters:
    -----------
    nono1 - one of two Nonograms to be compared
    nono2 - one of two Nonograms to be compared
    verbosity - for value != 0 prints misclassified cells
    
    Returns:
    --------
    bool - bool variable informing whether nonograms are consistent
    """
    # Correction for possible nonogram transposition
    if nono1.transposed:
        rows1 = nono1.cols
    else
        rows1 = nono1.rows

    # Correction for possible nonogram transposition
    if nono2.transposed:
        rows2 = nono1.cols
    else
        rows2 = nono1.rows

    mistakes = compare_tables(rows1, rows2)
    
    if verbose and mistakes:
        print_mistakes(mistakes, verbose)
    
    return bool(mistakes)