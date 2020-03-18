# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from unittest.mock import patch, call
import lib.nonogram as nonogram
from lib.solver import solver

nono  = nonogram.Nonogram("nonograms/small_1.dat")
nono1 = nonogram.Nonogram("nonograms/small_1.dat")
nono2 = nonogram.Nonogram("nonograms/small_1.dat")
nono_pre = nonogram.Nonogram("tests/data/nono_test_3.dat", presolved=True)


@patch('builtins.print')
@patch('builtins.quit')
def test_Nonogram_read_nonogram_from_file(mocked_quit, mocked_print):
    nonogram.Nonogram("tests/data/nono_test_3_inconsistent.dat")
    assert mocked_print.mock_calls == [
        call('Input nonogram is not self consistent.'),
        call('The sum of filled cells in rows is different than in columns.'),
        ]
    assert mocked_quit.mock_calls == [call()]


def test_transpose_rows():
    rows = [[1, 2, 3, -1], [4, 5, 6, -1], [7, 8, 9, -1]]
    assert nonogram.transpose_rows(rows) == [[1, 4, 7, -1], [2, 5, 8, -1], [3, 6, 9, -1]]


def test_Nonogram_initialisation():
    assert nono.nRows == 3
    assert nono.nCols == 3
    assert nono.rows == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.cols == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.rowHints == [[2], [2], [1, 1]]
    assert nono.colHints == [[1, 1], [2], [2]]
    assert nono.rowBlockOrigins == [[0], [0], [0, 0]]
    assert nono.colBlockOrigins == [[0, 0], [0], [0]]
    assert nono.rowBlockEndings == [[2], [2], [2, 2]]
    assert nono.colBlockEndings == [[2, 2], [2], [2]]
    assert nono.undetermind == 9
    assert nono.rowsChanged == {0, 1, 2}
    assert nono.colsChanged == {0, 1, 2}
    assert nono.transposed == False    


def test_Nonogram_initialisation_presolved():
    assert nono_pre.rows == [[ 1,  1, -1, -1],
                             [-1,  1,  0, -1],
                             [ 0, -1,  1, -1],
                             ]
    assert nono_pre.cols == [[ 1, -1,  0, -1],
                             [ 1,  1, -1, -1],
                             [-1,  0,  1, -1],
                             ]


def test_Nonogram_transpose():
    nono.transpose()
    assert nono.nRows == 3
    assert nono.nCols == 3
    assert nono.rows == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.cols == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.rowHints == [[1, 1], [2], [2]]
    assert nono.colHints == [[2], [2], [1, 1]]
    assert nono.rowBlockOrigins == [[0, 0], [0], [0]]
    assert nono.colBlockOrigins == [[0], [0], [0, 0]]
    assert nono.rowBlockEndings == [[2, 2], [2], [2]]
    assert nono.colBlockEndings == [[2], [2], [2, 2]]
    assert nono.undetermind == 9
    assert nono.rowsChanged == {0, 1, 2}
    assert nono.colsChanged == {0, 1, 2}
    assert nono.transposed == True
    nono.transpose()


def test_Nonogram_fill_cell():
    nono.rowsChanged = set()
    nono.colsChanged = set()
    nono.fill_cell(1, 2,  1)
    nono.fill_cell(0, 1, -1)
    assert nono.rows == [[0, -1, 0, -1], [0, 0, 1, -1], [0, 0, 0, -1]]
    assert nono.cols == [[0, 0, 0, -1], [-1, 0, 0, -1], [0, 1, 0, -1]]
    assert nono.rowsChanged == {0, 1}
    assert nono.colsChanged == {1, 2}
    assert nono.undetermind == 7
    with pytest.raises(Exception):
        nono.fill_cell(1, 2, -1)


def test_Nonogram_self_consistency_check():
    assert nono1.self_consistency_check() == True
    nono1.rowHints[0][0] += 1
    assert nono1.self_consistency_check() == False


def test_Nonogram_get_picture_data():
    solver(nono2)
    assert nono2.get_picture_data() == [[1, 1, -1], [-1, 1, 1], [1, -1, 1]]
    nono2.transpose()
    assert nono2.get_picture_data() == [[1, 1, -1], [-1, 1, 1], [1, -1, 1]]
