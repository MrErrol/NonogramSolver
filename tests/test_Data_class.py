# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch, call
import lib.nonogram as nonogram


filename_1 = "tests/data/nono_test_1.dat"

filename_3 = "tests/data/nono_test_3.dat"
filename_3_inconsistent = "tests/data/nono_test_3_inconsistent.dat"


def test_Data_initialisation_empty():
    # empty initialisation
    empty = nonogram.Data()
    assert empty.rows == [[]]
    assert empty.cols == [[]]
    assert empty.rowHints == [[]]
    assert empty.colHints == [[]]


def test_Data_initialisation_simple():
    # some simple nonogram
    data_1 = nonogram.Data(filename_1)
    assert data_1.rows == [[0, 0, 0, 0, 0, 0, 0, -1]] * 4
    assert data_1.cols == [[0, 0, 0, 0, -1]] * 7
    assert data_1.rowHints == [[2, 2], [2, 2], [1], [3]]
    assert data_1.colHints == [[2], [2], [2], [1], [1], [2], [2]]


def test_Data_initialisation_presolved():
    # presolved nonogram
    data_3 = nonogram.Data(filename_3, presolved=True)
    assert data_3.rows == [[1, 1, -1, -1], [-1, 1, 0, -1], [0, -1, 1, -1]]
    assert data_3.cols == [[1, -1, 0, -1], [1, 1, -1, -1], [-1, 0, 1, -1]]


@patch('builtins.quit')
def test_Data_initialisation_inconsistent(mocked_quit):
    # inconsistent nonogram
    nonogram.Data(filename_3_inconsistent)
    assert mocked_quit.mock_calls == [call()]
