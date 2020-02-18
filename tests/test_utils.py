# some utils test are performed in test_nonogram.py
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from utils.read_from_file import read_datafile, read_numeric_lines, read_presolved_nonogram_representation, is_beggining_of_row_hints, is_beggining_of_col_hints, is_beggining_of_cells, does_it_contain_only_numbers

file_1 = open('tests/broken_nono_1.dat', 'r')
file_2 = open('tests/test_nono_2.dat', 'r')
filename_3 = 'tests/test_nono_3.dat'

filename_small_1 = 'nonograms/small_1.dat'
file_small_1 = open(filename_small_1, 'r')

def test_does_it_contain_only_numbers():
    assert does_it_contain_only_numbers('1234214963483') == True
    assert does_it_contain_only_numbers('123a483') == False
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

def test_read_datafile():
    assert read_datafile(filename_small_1) == ([[2], [2], [1, 1]], [[1, 1], [2], [2]], True)
    assert read_datafile(filename_3, presolved=True) == ([[2], [2], [1, 1]],\
                                                         [[1, 1], [2], [2]],\
                                                         [[1, 1, -1], [-1, 1, 0], [0, -1, 1]])
