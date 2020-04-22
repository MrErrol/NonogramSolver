# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import lib.nonogram as nonogram


filename_1 = "tests/data/nono_test_1.dat"
filename_3 = "tests/data/nono_test_3.dat"


def test_Limits_initialisation_empty():
    # empty class
    empty_1 = nonogram.Limits()
    assert empty_1.rowBlockOrigins == [[]]
    assert empty_1.rowBlockEndings == [[]]
    assert empty_1.colBlockOrigins == [[]]
    assert empty_1.colBlockEndings == [[]]
    # also empty class
    empty_2 = nonogram.Limits('whatever')
    assert empty_2.rowBlockOrigins == [[]]
    assert empty_2.rowBlockEndings == [[]]
    assert empty_2.colBlockOrigins == [[]]
    assert empty_2.colBlockEndings == [[]]


def test_Limits_initialisation_simple():
    # simple hints for small nonogram
    row_hints = [[2, 1], [2]]
    col_hints = [[1], [2], [1], [2]]
    limits = nonogram.Limits(row_hints, col_hints)
    assert limits.rowBlockOrigins == [[0, 0], [0]]
    assert limits.rowBlockEndings == [[3, 3], [3]]
    assert limits.colBlockOrigins == [[0], [0], [0], [0]]
    assert limits.colBlockEndings == [[1], [1], [1], [1]]


def test_Limits_copy():
    limits = nonogram.Limits([[2], [1]], [[1, 1], [1]])
    limits_copy = limits
    assert limits.rowBlockOrigins == limits_copy.rowBlockOrigins
    assert limits.rowBlockEndings == limits_copy.rowBlockEndings
    assert limits.colBlockOrigins == limits_copy.colBlockOrigins
    assert limits.colBlockEndings == limits_copy.colBlockEndings


def test_Limits_transpose():
    # compare with test_Limits_initialisation_simple
    row_hints = [[2, 1], [2]]
    col_hints = [[1], [2], [1], [2]]
    limits = nonogram.Limits(row_hints, col_hints)
    limits.transpose()
    assert limits.rowBlockOrigins == [[0], [0], [0], [0]]
    assert limits.rowBlockEndings == [[1], [1], [1], [1]]
    assert limits.colBlockOrigins == [[0, 0], [0]]
    assert limits.colBlockEndings == [[3, 3], [3]]


def test_Limits_get_row_origins():
    limits = nonogram.Limits()
    limits.rowBlockOrigins = [[1, 2], [3]]
    assert limits.get_row_origins(0) == [1, 2]
    assert limits.get_row_origins(1, 0) == 3


def test_Limits_get_col_origins():
    limits = nonogram.Limits()
    limits.colBlockOrigins = [[1, 2], [3]]
    assert limits.get_col_origins(0) == [1, 2]
    assert limits.get_col_origins(1, 0) == 3


def test_Limits_get_row_endings():
    limits = nonogram.Limits()
    limits.rowBlockEndings = [[1, 2], [3]]
    assert limits.get_row_endings(0) == [1, 2]
    assert limits.get_row_endings(1, 0) == 3


def test_Limits_get_col_endings():
    limits = nonogram.Limits()
    limits.colBlockEndings = [[1, 2], [3]]
    assert limits.get_col_endings(0) == [1, 2]
    assert limits.get_col_endings(1, 0) == 3


def test_Limits_set_row_origins():
    limits = nonogram.Limits([[1, 1], [1]], [[1], [1, 1]])
    limits.set_row_origins(0, [1, 4, 5])
    assert limits.rowBlockOrigins[0] == [1, 4, 5]


def test_Limits_set_row_endings():
    limits = nonogram.Limits([[1, 1], [1]], [[1], [1, 1]])
    limits.set_row_endings(1, [1, 4, 5])
    assert limits.rowBlockEndings[1] == [1, 4, 5]


def test_Limits_set_col_origins():
    limits = nonogram.Limits([[1, 1], [1]], [[1], [1, 1]])
    limits.set_col_origins(1, [1, 4, 5])
    assert limits.colBlockOrigins[1] == [1, 4, 5]


def test_Limits_set_col_endings():
    limits = nonogram.Limits([[1, 1], [1]], [[1], [1, 1]])
    limits.set_col_endings(0, [1, 4, 5])
    assert limits.colBlockEndings[0] == [1, 4, 5]
