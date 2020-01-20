def find_beggining_of_data(file):
    """
    This function is used to find beggining of the data in the data file effectively discarding beggining lines.
    """
    while True:
        line = file.readline()
        if line[:5] == 'ROWS:':
            break
        elif line[:8] == 'COLUMNS:':
            raise Exception('Lack of data in input file.')
        elif line == '':
            raise Exception('Incorrect data file.')

def read_lines(file, stop=None):
    """
    This function read hints (rowHints or colHints) from a datafile and returns them.
    
    Returns:
    --------
    read_list = list of list of hints read from datafile
    """
    read_list = []
    while True:
        line = file.readline()
        if line[:len(stop)] == stop and stop != '':
            break
        elif line == stop == '':
            break
        elif line == '':
            raise Exception('Incorrect data file.')
        else:
            read_list.append(list(map(int, line.split(' '))))
    return read_list