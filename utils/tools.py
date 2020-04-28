def print_congrats():
    """
    Prints congratulations to raise up spirit when no mistakes were found.
    """
    print("So far, so good!")
    print("No mistakes found.")


def print_failure_statement(cycle):
    """
    Prints information that solver failed to solve nonogram.
    """
    print("Failed to solve Nonogram.")
    print("Cycle : " + str(cycle))


def print_complain():
    """
    Function informs user about inconsistency in provided data.
    It is usually caused by typing error.
    """
    print('Input nonogram is not self consistent.')
    print('The sum of filled cells in rows is different than in columns.')


def print_mistakes(mistakes, verbose):
    """
    Prints misclassified cells.
    """
    print("Whoops! You have made a mistake!")
    if verbose:
        print("List of misclassified cells:")
        print("Counting from 1.")
        print("(row number, column number)")
        for pair in mistakes:
            shifted_pair = (pair[0]+1, pair[1]+1)
            print(shifted_pair)


def show_basic_hint(row, transposed):
    """
    Prints basic hint about next cell to be filled.
    Used with simple solving methods.
    """
    if transposed:
        print('Analyze column ' + str(row) + '.')
    else:
        print('Analyze row ' + str(row) + '.')


def show_basic_hint_assumption(row, col, transposed):
    """
    Print basic hint about next cell to be filled.
    Deduction requires assumption making.
    """
    if transposed:
        print("Assume the cell at row=" + str(col) + " and col=" + \
              str(row) + " to be filled and try to deduce consequences.")
    else:
        print("Assume the cell at row=" + str(row) + " and col=" + \
              str(col) + " to be filled and try to deduce consequences.")


def show_explicit_hint(row, col, value, transposed):
    """
    Prints explicit information about next cell to be filled.
    """
    values = {-1: 'empty.', 1: 'filled.'}
    if transposed:
        print("Cell at row=" + str(col + 1) + " and col=" + str(row + 1) +
              " may be deduced to be " + values[value])
    else:
        print("Cell at row=" + str(row + 1) + " and col=" + str(col + 1) +
              " may be deduced to be " + values[value])


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
    Compares two nonogram cell tables, checking whether there is a discrepancy
    between their solved cells.

    Function is used to verify whether user has made a mistake while (at least)
    partially solving Nonogram.

    Parameters:
    -----------
    nono1 - one of two cell tables to be compared
    nono2 - one of two cell tables to be compared

    Returns:
    --------
    mistakes - list of pairs of coordinates of misclassified cells
    """
    mistakes = []

    for row, dummy_row_list in enumerate(rows1):
        for col in range(len(rows1[0])-1):
            # checks whether values are consistent
            if not compare_values(rows1[row][col], rows2[row][col]):
                mistakes.append((row, col))

    return mistakes


def compare_nonograms(nono1, nono2, verbose=0):
    """
    Compares two Nonograms, checking whether there is a discrepancy between
    their solved cells.

    Function is used to verify whether user has made a mistake while (at
    least) partially solving Nonogram.

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
    rows1 = nono1.get_true_rows()
    rows2 = nono2.get_true_rows()

    mistakes = compare_tables(rows1, rows2)

    if mistakes:
        print_mistakes(mistakes, verbose)
    else:
        print_congrats()

    return not bool(mistakes)
