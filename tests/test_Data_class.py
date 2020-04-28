# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from unittest.mock import patch, call
import lib.nonogram as nonogram


filename_1 = "tests/data/nono_test_1.dat"
filename_3 = "tests/data/nono_test_3.dat"
filename_3_pre = "tests/data/nono_test_3-presolved.dat"
filename_3_inconsistent = "tests/data/nono_test_3_inconsistent.dat"


def test_Data_initialisation_empty():
    # empty initialisation
    empty = nonogram.Data()
    assert empty.rows == [[]]
    assert empty.cols == [[]]
    assert empty.row_hints == [[]]
    assert empty.col_hints == [[]]


def test_Data_initialisation_simple():
    # some simple nonogram
    data_1 = nonogram.Data(filename_1)
    assert data_1.rows == [[0, 0, 0, 0, 0, 0, 0, -1]] * 4
    assert data_1.cols == [[0, 0, 0, 0, -1]] * 7
    assert data_1.row_hints == [[2, 2], [2, 2], [1], [3]]
    assert data_1.col_hints == [[2], [2], [2], [1], [1], [2], [2]]


def test_Data_initialisation_presolved():
    # presolved nonogram
    data_3 = nonogram.Data(filename_3, presolved=filename_3_pre)
    assert data_3.rows == [[1, 1, -1, -1], [-1, 1, 0, -1], [0, -1, 1, -1]]
    assert data_3.cols == [[1, -1, 0, -1], [1, 1, -1, -1], [-1, 0, 1, -1]]


@patch('builtins.quit')
def test_Data_initialisation_inconsistent(mocked_quit):
    # inconsistent nonogram
    nonogram.Data(filename_3_inconsistent)
    assert mocked_quit.mock_calls == [call()]


def test_Data_transpose():
    # Compare with test_Data_initialisation_presolved
    data_3 = nonogram.Data(filename_3, presolved=filename_3_pre)
    data_3.transpose()
    assert data_3.row_hints == [[1, 1], [2], [2]]
    assert data_3.col_hints == [[2], [2], [1, 1]]
    assert data_3.rows == [[1, -1, 0, -1], [1, 1, -1, -1], [-1, 0, 1, -1]]
    assert data_3.cols == [[1, 1, -1, -1], [-1, 1, 0, -1], [0, -1, 1, -1]]


def test_Data_copy():
    data_3 = nonogram.Data(filename_3, presolved=filename_3_pre)
    nono_copy = data_3.copy()
    assert data_3.rows == nono_copy.rows
    assert data_3.cols == nono_copy.cols
    assert data_3.row_hints is nono_copy.row_hints
    assert data_3.col_hints is nono_copy.col_hints


def test_Data_fill_cell_filling():
    data_3 = nonogram.Data(filename_3, presolved=filename_3_pre)
    # filling cell
    assert data_3.fill_cell(1, 2, 1) == True
    assert data_3.rows[1][2] == 1
    assert data_3.cols[2][1] == 1
    assert data_3.fill_cell(2, 0, -1) == True
    assert data_3.rows[2][0] == -1
    assert data_3.cols[0][2] == -1


def test_Data_fill_cell():
    data_3 = nonogram.Data(filename_3, presolved=filename_3_pre)
    # changes nothing
    assert data_3.fill_cell(0, 0, 1) == False
    # trying to overwrite 1 with -1
    with pytest.raises(nonogram.OverwriteException):
        data_3.fill_cell(0, 1, -1)


def test_Data_get_row_hints():
    data_1 = nonogram.Data(filename_1)
    assert data_1.get_row_hints() == [[2, 2], [2, 2], [1], [3]]
    assert data_1.get_row_hints(0) == [2, 2]
    assert data_1.get_row_hints(3, 0) == 3


def test_Data_get_col_hints():
    data_3 = nonogram.Data(filename_3)
    assert data_3.get_col_hints() == [[1, 1], [2], [2]]
    assert data_3.get_col_hints(2) ==  [2]
    assert data_3.get_col_hints(0, 1) == 1


def test_Data_get_row():
    data_3 = nonogram.Data(filename_3, presolved=filename_3_pre)
    assert data_3.get_row() == [[1, 1, -1, -1], [-1, 1, 0, -1], [0, -1, 1, -1]]
    assert data_3.get_row(1) == [-1, 1, 0, -1]
    assert data_3.get_row(0, 2) == -1


def test_Data_get_col():
    data_3 = nonogram.Data(filename_3, presolved=filename_3_pre)
    assert data_3.get_col() == [[1, -1, 0, -1], [1, 1, -1, -1], [-1, 0, 1, -1]]
    assert data_3.get_col(2) == [-1, 0, 1, -1]
    assert data_3.get_col(1, 0) == 1
