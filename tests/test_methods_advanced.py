# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import patch
from lib.nonogram import Nonogram
from lib.methods_advanced import check_if_line_is_fillable, make_assumption,\
    ivestigate_row_with_assumptions, search_for_assumptions


f_line_0 = [0, 0, 0, 0, 0, -1]  
f_line_1 = [1, 0, 0, 0, 1, -1]    
f_line_2 = [0, 0, 1, 0, 0, -1]    


def test_check_if_line_is_fillable():
    assert check_if_line_is_fillable(f_line_1, [3], [0], [3]) == False
    assert check_if_line_is_fillable(f_line_1, [3], [1], [4]) == False
    assert check_if_line_is_fillable(f_line_0, [3], [1], [3]) == True
    assert check_if_line_is_fillable(f_line_0, [3], [2], [3]) == False
    assert check_if_line_is_fillable(f_line_2, [1, 1], [0, 3], [1, 4]) == False


nono_assume_1 = Nonogram("tests/data/nono_test_1.dat")
nono_assume_2 = Nonogram("tests/data/nono_test_1.dat")
nono_assume_3 = Nonogram("tests/data/nono_test_1.dat")
nono_assume_4 = Nonogram("tests/data/nono_test_1.dat")
nono_too_small = Nonogram("tests/data/nono_test_3.dat")


def test_make_assumption():
    assert make_assumption(nono_assume_1, 3, 0) == False
    assert make_assumption(nono_assume_1, 3, 1) == False
    assert make_assumption(nono_assume_1, 3, 2) == True
    assert make_assumption(nono_assume_1, 3, 6) == False


@patch('lib.methods_advanced.make_deduction')
def test_make_assumption_part2(mocked_check):
    mocked_check.return_value = False

    nono_assume_4.limits.row_block_origins[0] = [2, 2]
    nono_assume_4.limits.row_block_endings[0] = [2, 2]

    assert make_assumption(nono_assume_4, 0, 5) == False

    nono_assume_4.limits.row_block_origins[0] = [0, 2]
    nono_assume_4.limits.row_block_endings[0] = [3, 5]
    nono_assume_4.limits.col_block_origins[5] = [2]
    nono_assume_4.limits.col_block_endings[5] = [2]

    assert make_assumption(nono_assume_4, 0, 5) == False


def test_ivestigate_row_with_assumptions():
    assert ivestigate_row_with_assumptions(nono_assume_2, 0) == False
    assert ivestigate_row_with_assumptions(nono_assume_2, 1) == False
    assert ivestigate_row_with_assumptions(nono_assume_2, 3) == True    
    assert nono_assume_2.data.get_row(3) == [-1, -1, 0, 0, 0, -1, -1, -1] # -1 at 5th position is not obvious


def test_search_for_assumptions():
    assert search_for_assumptions(nono_assume_3, searching_depth=1) == True
    assert nono_assume_3.data.get_row(0) == [ 0,  0,  0,  0,  0,  0,  0, -1]
    assert nono_assume_3.data.get_row(3) == [-1, -1,  0,  0,  0, -1, -1, -1]
    assert search_for_assumptions(nono_assume_3, searching_depth=3) == True
    assert nono_assume_3.data.get_row(2) == [-1, -1,  0, -1, -1, -1, -1, -1] # cause we already know all about row 3
