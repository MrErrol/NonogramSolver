from string import digits


def is_beggining_of_row_hints(line):
    return line[:5] == 'ROWS:'


def is_beggining_of_col_hints(line):
    return line[:8] == 'COLUMNS:'


def is_beggining_of_cells(line):
    return line[:6] == 'CELLS:'


def default_mapping():
    return {'f':1, 'F':1, 'u':0, 'U':0, 'e':-1, 'E':-1,\
            '+':1, '-':-1, '0':0, '1':1, '2':-1}


def does_it_contain_only_numbers(text):
    return all([[letter in digits for letter in word][0] for word in text])


def structure_raw_cells(raw_cells):
    return [row + [-1] for row in raw_cells]


def strip_trailing_empty_cells(structured_cells):
    return [row[:-1] for row in structured_cells]


def transpose_raw_cells(raw_cells):
    return [[raw_cells[j][i] \
            for j, dummy_value_1 in enumerate(raw_cells[i])] \
            for i, dummy_value_2 in enumerate(raw_cells)]


def transpose_rows(rows):
    new_rows = strip_trailing_empty_cells(rows)
    new_rows = transpose_raw_cells(new_rows)
    new_rows = structure_raw_cells(new_rows)
    return new_rows


def read_presolved_nonogram_representation(file, mapping=default_mapping()):
    read_list = []
    while True:
        line = file.readline()

        # End of file
        cond1 = line == ''
        # Smoke-gun of a new block
        cond2 = ':' in line
        # Empty line
        cond3 = line.isspace()

        if cond1 or cond2 or cond3:
            break

        read_list.append(line.rstrip())

    return [[mapping[letter] for letter in row] for row in read_list], line


def read_numeric_lines(file):
    """
    Function read block of numbers (developed for reading hints) as a list of
    lists of numbers.

    Returns:
    --------
    read_list - list of list of numbers read from datafile
    line - line following the block of numbers
    """
    read_list = []

    while True:
        line = file.readline()
        # End of file
        if line == '':
            break
        # Not integer-only line
        if not does_it_contain_only_numbers(line.split()):
            break
        # appending read hints
        read_list.append(list(map(int, line.split())))

    return read_list, line


def read_datafile(filename, presolved=False):
    """
    Function reads from datafile hints (lengths of blocks) for rows and columns
    of nonogram.

    Returns:
    --------
    rowHints - list of list of hints for rows for nonogram
    colHints - list of list of hints for columns for nonogram
    """

    rowHints = []
    colHints = []
    cells = not presolved

    file = open(filename, 'r')
    line = file.readline()

    while not (rowHints and colHints and cells):
        if line == '':
            break
        if is_beggining_of_row_hints(line):
            rowHints, line = read_numeric_lines(file)
            continue
        if is_beggining_of_col_hints(line):
            colHints, line = read_numeric_lines(file)
            continue
        if is_beggining_of_cells(line) and presolved:
            cells, line = read_presolved_nonogram_representation(file)
            continue
        line = file.readline()

    file.close()

    return rowHints, colHints, cells
