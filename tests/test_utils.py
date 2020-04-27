# some utils test are performed in test_nonogram.py
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch, call
from utils.read_from_file import read_datafile, read_numeric_lines,\
    read_presolved_nonogram_representation, is_beggining_of_row_hints,\
    is_beggining_of_col_hints, is_beggining_of_cells,\
    does_it_contain_only_numbers, read_presolved_nonogram_representation
from utils.tools import print_mistakes, compare_values, compare_tables,\
    compare_nonograms, show_basic_hint
from lib.nonogram import Nonogram


file_1 = open('tests/data/broken_nono_1.dat', 'r')
file_2 = open('tests/data/nono_test_2.dat', 'r')
file_3 = open('tests/data/nono_test_3.dat', 'r')
file_3_pre = open('tests/data/nono_test_3-presolved.dat', 'r')
file_3_pre_a = open('tests/data/nono_test_3-presolved.dat', 'r')
filename_2_broken = 'tests/data/nono_test_2_broken.dat'
filename_3 = 'tests/data/nono_test_3.dat'
filename_3_pre = "tests/data/nono_test_3-presolved.dat"

filename_small_1 = 'nonograms/small_1.dat'
file_small_1 = open(filename_small_1, 'r')

table_1a = [[ 0,  1, -1, -1],
            [ 0,  1, -1, -1]]
table_1b = [[ 0,  1, -1, -1],
            [ 0,  0,  0, -1]]
table_2a = [[ 0,  1,  1, -1],
            [ 0, -1, -1, -1]]

nono_1a = Nonogram(None)
nono_1b = Nonogram(None)
nono_2a = Nonogram(None)

nono_1a.data.rows = table_1a
nono_1b.data.rows = table_1b
nono_2a.data.rows = table_2a


def test_does_it_contain_only_numbers():
    assert does_it_contain_only_numbers('1234214963483') == True
    assert does_it_contain_only_numbers('123a483') == False
    assert does_it_contain_only_numbers('1 24 3a 4b 83\n') == False
    assert does_it_contain_only_numbers(['1','4','6']) == True
    assert does_it_contain_only_numbers(['1','a','6']) == False
    assert does_it_contain_only_numbers(['1','5','\n']) == False


def test_is_functions():
    line = file_2.readline()
    assert is_beggining_of_row_hints(line) == True
    assert is_beggining_of_col_hints(line) == False
    assert is_beggining_of_cells(line) == False
    line = file_2.readline()
    assert is_beggining_of_row_hints(line) == False
    assert is_beggining_of_col_hints(line) == True
    assert is_beggining_of_cells(line) == False
    line = file_2.readline()
    assert is_beggining_of_row_hints(line) == False
    assert is_beggining_of_col_hints(line) == False
    assert is_beggining_of_cells(line) == True
    file_2.close()


def test_read_numeric_lines():
    file_1.readline()
    assert read_numeric_lines(file_1) == ([[1], [1, 2]], '')
    file_small_1.readline()
    assert read_numeric_lines(file_small_1) == ([[2], [2], [1, 1]], 'COLUMNS:\n')
    file_1.close()
    file_small_1.close()


def test_read_presolved_nonogram_representation():
    assert read_presolved_nonogram_representation(file_3_pre) == (
        [[1, 1, -1],
        [-1, 1, 0],
        [0, -1, 1]]
    )
    file_3_pre.close()


def test_read_presolved_nonogram_representation_modified_mapping():
    rotated_mapping = {'f': 0, 'F': 0, 'u': -1, 'U': -1, 'e': 1, 'E': 1,
     '+': 0, '-': 1, '0': -1, '1': 0, '2': 1}
    assert read_presolved_nonogram_representation(file_3_pre_a, mapping=rotated_mapping) == (
        [[0, 0, 1],
        [1, 0, -1],
        [-1, 1, 0]]
    )
    file_3_pre_a.close()


def test_read_datafile():
    assert read_datafile(filename_small_1) ==\
           ([[2], [2], [1, 1]], [[1, 1], [2], [2]])
    assert read_datafile(filename_3) ==\
           ([[2], [2], [1, 1]],\
           [[1, 1], [2], [2]],\
           )
    assert read_datafile(filename_2_broken) == ([], [])


def test_compare_values():
    assert compare_values(0, 1) == True
    assert compare_values(0, -1) == True
    assert compare_values(0, 0) == True
    assert compare_values(1, 1) == True
    assert compare_values(-1, -1) == True
    assert compare_values(1, -1) == False
    assert compare_values(-1, 1) == False


def test_compare_tables():
    assert compare_tables(table_1a, table_1b) == []
    assert compare_tables(table_1a, table_2a) == [(0,2), (1,1)]
    assert compare_tables(table_1b, table_2a) == [(0,2)]


@patch('builtins.print')
def test_print_mistakes(mocked_print):
    print_mistakes([(1,2), (3,5)], 0)
    assert mocked_print.mock_calls == [call("Whoops! You have made a mistake!")]
    mocked_print.reset_mock()
    print_mistakes([(1,2), (3,5)], 1)
    assert mocked_print.mock_calls == [call("Whoops! You have made a mistake!"),
                                      call("List of misclassified cells:"),
                                      call("Counting from 1."),
                                      call("(row number, column number)"),
                                      call((2,3)),
                                      call((4,6))]


@patch('builtins.print')
def test_show_basic_hint(mocked_print):
    show_basic_hint(2, 3, True, 1)
    assert mocked_print.mock_calls == [call("Analyze column 2.")]
    mocked_print.reset_mock()
    show_basic_hint(2, 3, False, 1)
    assert mocked_print.mock_calls == [call("Analyze row 2.")]
    mocked_print.reset_mock()
    show_basic_hint(2, 3, True, 0)
    assert mocked_print.mock_calls == [call("Assume the cell at row=3 and col=2 to be filled and try to deduce consequences.")]
    mocked_print.reset_mock()
    show_basic_hint(2, 3, False, 0)
    assert mocked_print.mock_calls == [call("Assume the cell at row=2 and col=3 to be filled and try to deduce consequences.")]


@patch('builtins.print')
def test_compare_nonograms(mocked_print):
    assert compare_nonograms(nono_1a, nono_1b) == True
    assert mocked_print.mock_calls == [call("So far, so good!"),
                                       call("No mistakes found.")]
    mocked_print.reset_mock()
    assert compare_nonograms(nono_1a, nono_2a) == False
    assert mocked_print.mock_calls == [call("Whoops! You have made a mistake!")]
    mocked_print.reset_mock()
    assert compare_nonograms(nono_1b, nono_2a, verbose=1) == False
    assert mocked_print.mock_calls == [call("Whoops! You have made a mistake!"),
                                      call("List of misclassified cells:"),
                                      call("Counting from 1."),
                                      call("(row number, column number)"),
                                      call((1,3))]
