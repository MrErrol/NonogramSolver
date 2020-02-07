# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from lib.nonogram import Nonogram
from lib.methods_advanced import check_if_line_is_fillable, make_assumption, ivestigate_row_with_assumptions, search_for_assumptions

nono = Nonogram("nonograms/small_1.dat")

# This test is implemented in test_nonogram.py
# It is present here just to show initial values of nono
#def test_Nonogram_initialisation():
#    assert nono.nRows == 3
#    assert nono.nCols == 3
#    assert nono.rows == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
#    assert nono.cols == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
#    assert nono.rowHints == [[2], [2], [1, 1]]
#    assert nono.colHints == [[1, 1], [2], [2]]
#    assert nono.rowBlockOrigins == [[0], [0], [0, 0]]
#    assert nono.colBlockOrigins == [[0, 0], [0], [0]]
#    assert nono.rowBlockEndings == [[2], [2], [2, 2]]
#    assert nono.colBlockEndings == [[2, 2], [2], [2]]
#    assert nono.undetermind == 9
#    assert nono.rowsChanged == []
#    assert nono.colsChanged == []
#    assert nono.transposed == False  

f_line_0 = [0, 0, 0, 0, 0, -1]  
f_line_1 = [1, 0, 0, 0, 1, -1]    
f_line_2 = [0, 0, 1, 0, 0, -1]    
    
def test_check_if_line_is_fillable():
    assert check_if_line_is_fillable(f_line_1, [3], [0], [3]) == False
    assert check_if_line_is_fillable(f_line_1, [3], [1], [4]) == False
    assert check_if_line_is_fillable(f_line_0, [3], [1], [3]) == True
    assert check_if_line_is_fillable(f_line_0, [3], [2], [3]) == False
    assert check_if_line_is_fillable(f_line_2, [1, 1], [0, 3], [1, 4]) == False

nono_assume_1 = Nonogram("tests/nono_test_1.dat")
nono_assume_2 = Nonogram("tests/nono_test_1.dat")
nono_assume_3 = Nonogram("tests/nono_test_1.dat")


def test_make_assumption():
    #assert make_assumption(nono_assume_1, 3, 0) == False
    #assert make_assumption(nono_assume_1, 3, 1) == False
    assert make_assumption(nono_assume_1, 3, 2) == True
    assert make_assumption(nono_assume_1, 3, 6) == False

def test_ivestigate_row_with_assumptions():
    assert ivestigate_row_with_assumptions(nono_assume_2, 0) == False
    assert ivestigate_row_with_assumptions(nono_assume_2, 1) == False
    assert ivestigate_row_with_assumptions(nono_assume_2, 3) == True    
    assert nono_assume_2.rows[3] == [-1, -1, 0, 0, 0, -1, -1, -1] # -1 at 5th position is not obvious

def test_search_for_assumptions():
    assert search_for_assumptions(nono_assume_3) == True
    assert nono_assume_2.rows[0] == [ 0,  0,  0,  0,  0,  0,  0, -1]
    assert nono_assume_3.rows[3] == [-1, -1,  0,  0,  0, -1, -1, -1]
    assert search_for_assumptions(nono_assume_3, searching_depth=2) == True
    assert nono_assume_2.rows[1] == [ 0,  0,  0,  0,  0,  0,  0, -1]
    assert nono_assume_3.rows[2] == [-1, -1,  0, -1, -1, -1, -1, -1] # cause we already know all about row 3


