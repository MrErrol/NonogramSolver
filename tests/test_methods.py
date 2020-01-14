# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
from nonogram import Nonogram
from methods import push_block_Origins, push_block_Endings, deduce_new_block_origins, deduce_new_block_endings, fill_row
from methods import find_min_block_length, analyze_multi_block_relations_in_row, analyze_multi_block_relations
from methods import check_if_line_is_fillable, make_assumption, ivestigate_row_with_assumptions, search_for_assumptions

hints1 = [1, 1, 1]
hints2 = [1, 2, 1, 3]
blockOrigins1 = [0, 0, 0]
blockOrigins2 = [0, 0, 0, 0]
blockOrigins3 = [0, 0, 5]
blockOrigins4 = [0, 0, 7, 5]
blockOrigins5 = [0, 2, 4]

def test_push_block_Origins():
    assert push_block_Origins(hints1, blockOrigins1) == (True, [0, 2, 4])
    assert push_block_Origins(hints2, blockOrigins2) == (True, [0, 2, 5, 7])
    assert push_block_Origins(hints1, blockOrigins3) == (True, [0, 2, 5])
    assert push_block_Origins(hints2, blockOrigins4) == (True, [0, 2, 7, 5])
    assert push_block_Origins(hints1, blockOrigins1, index=1) == (True, [0, 0, 2])
    assert push_block_Origins(hints1, blockOrigins1, index=2) == (False, [0, 0, 0])
    assert push_block_Origins(hints2, blockOrigins4, index=2) == (True, [0, 0, 7, 9])

blockEndings_1 = [8, 8, 8]
blockEndings_2 = [12, 12, 12, 12]
blockEndings_3 = [3, 8, 8]
blockEndings_4 = [8, 5, 12, 12]
    
def test_push_block_Endings():
    assert push_block_Endings(hints1, blockEndings_1) == (True, [4, 6, 8])
    assert push_block_Endings(hints2, blockEndings_2) == (True, [3, 6, 8, 12])
    assert push_block_Endings(hints1, blockEndings_3) == (True, [3, 6, 8])
    assert push_block_Endings(hints2, blockEndings_4) == (True, [8, 5, 8, 12])
    assert push_block_Endings(hints1, blockEndings_1, index=1) == (True, [6, 8, 8])
    assert push_block_Endings(hints1, blockEndings_1, index=2) == (False, [8, 8, 8])
    assert push_block_Endings(hints2, blockEndings_4, index=2) == (True, [2, 5, 12, 12])    
    
line1 = [0]*5 + [-1]
line2 = [0, 1, 0, 0, 0, 0, -1]
line3 = [-1, 0, 0, 0, 0, 0, -1]
line4 = [-1, 0, 1, 0, -1, 0, 0, 1, -1]
line5 = [0, 0, 0, 0, 0, 0, 1, 0, -1]
line6 = [0, 0, 0, 0, 0, 0, 0, -1, -1]
line7 = [0, 1, 0, 0, -1, 0, 1, 0, -1]
line8 = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1]
line9 = [-1, 0, 0, 1, 0, 0, 1, 0, 1, -1]
line10 = [-1, 0, 0, 1, 0, 0, 1, 0, 1, 0, -1]
    
# function behaviour depends on the function push_block_Origins (see tests above)
def test_deduce_new_block_origins():
    assert deduce_new_block_origins(line1, hints1, blockOrigins1) == (False, [0, 0, 0]), "for not initialized blockOrigins gives no gain"
    assert deduce_new_block_origins(line1, hints1, blockOrigins5) == (False, [0, 2, 4])
    assert deduce_new_block_origins(line2, hints1, blockOrigins1) == (True,  [1, 3, 5])
    assert deduce_new_block_origins(line3, hints1, blockOrigins1) == (True,  [1, 3, 5])
    assert deduce_new_block_origins(line4, hints1, blockOrigins1) == (True,  [2, 5, 7])
    assert deduce_new_block_origins(line8, hints2, blockOrigins2) == (True,  [1, 3, 6, 8])
    assert deduce_new_block_origins(line9, hints1, blockOrigins1) == (True,  [3, 6, 8])
    assert deduce_new_block_origins(line10, hints1, blockOrigins1) == (True,  [3, 6, 8])

blockEndings1 = [4, 4, 4]
blockEndings2 = [0, 2, 4]
blockEndings3 = [7, 7, 7]
blockEndings4 = [11, 11, 11, 11]
    
# function behaviour depends on the function deduce_new_block_origins (see tests above)
# It is just extended wrapper for the function above
def test_deduce_new_block_endings():
    assert deduce_new_block_endings(line1, hints1, blockEndings1) == (False, [4, 4, 4]), "for not initialized blockOrigins gives no gain"
    assert deduce_new_block_endings(line1, hints1, blockEndings2) == (False, [0, 2, 4])
    assert deduce_new_block_endings(line5, hints1, blockEndings3) == (True,  [2, 4, 6])
    assert deduce_new_block_endings(line6, hints1, blockEndings3) == (True,  [2, 4, 6])
    assert deduce_new_block_endings(line7, hints1, blockEndings3) == (True,  [1, 3, 6])
    assert deduce_new_block_endings(line8, hints2, blockEndings4) == (True,  [1, 4, 6, 10])


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

def test_fill_row():
    fill_row(nono, 0)
    assert nono.rows == [[0, 1, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.cols == [[0, 0, 0, -1], [1, 0, 0, -1], [0, 0, 0, -1]]
    assert nono.undetermind == 8
    nono.rowBlockOrigins[2] = [0, 2]
    nono.rowBlockEndings[2] = [0, 2]
    fill_row(nono, 2)
    assert nono.rows == [[0, 1, 0, -1], [0, 0,  0, -1], [1, -1, 1, -1]]
    assert nono.cols == [[0, 0, 1, -1], [1, 0, -1, -1], [0,  0, 1, -1]]
    assert nono.undetermind == 5

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
    assert make_assumption(nono_assume_1, 3, 0) == False
    assert make_assumption(nono_assume_1, 3, 1) == False
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

nono_multi_1 = Nonogram("tests/nono_test_1.dat")
nono_multi_2 = Nonogram("tests/nono_test_1.dat")

def test_find_min_block_length():
    nono_multi_1.rowBlockOrigins[0] = [0, 2, 4, 5]
    nono_multi_1.rowBlockEndings[0] = [3, 5, 7, 9]
    nono_multi_1.rowHints[0] = [2, 4, 5, 1]
    assert find_min_block_length(nono_multi_1, 0, 1) == 2
    assert find_min_block_length(nono_multi_1, 0, 2) == 2
    assert find_min_block_length(nono_multi_1, 0, 4) == 4
    assert find_min_block_length(nono_multi_1, 0, 5) == 1

def test_analyze_multi_block_relations_in_row():
    nono_multi_1.rowHints[1]        = [3, 3]
    nono_multi_1.rowBlockOrigins[1] = [0, 4]
    nono_multi_1.rowBlockEndings[1] = [6, 10]
    nono_multi_1.rows[1] = [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1]

    assert analyze_multi_block_relations_in_row(nono_multi_1, 1) == True
    assert nono_multi_1.rows[1] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]

    nono_multi_1.rowHints[2]        = [3, 3]
    nono_multi_1.rowBlockOrigins[2] = [0, 4]
    nono_multi_1.rowBlockEndings[2] = [6, 10]
    nono_multi_1.rows[2] = [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1]

    assert analyze_multi_block_relations_in_row(nono_multi_1, 2) == True
    assert nono_multi_1.rows[2] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]

    nono_multi_1.rowHints[3]        = [3, 3]
    nono_multi_1.rowBlockOrigins[3] = [0, 4]
    nono_multi_1.rowBlockEndings[3] = [6, 10]
    nono_multi_1.rows[3] = [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1]

    assert analyze_multi_block_relations_in_row(nono_multi_1, 3) == True
    assert nono_multi_1.rows[1] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]

def test_analyze_multi_block_relations():
    nono_multi_2.rowHints        = [[3, 3]]*4
    nono_multi_2.rowBlockOrigins = [[0, 4 ]]*4
    nono_multi_2.rowBlockEndings = [[6, 10]]*4
    nono_multi_2.rows = [[0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1],
                         [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1],
                         [0, 0, 0, -1, 1, 0, 0, -1, 0, 0, 0, -1],
                         [0, 0, 0, -1, 0, 0, 1, -1, 0, 0, 0, -1]]

    assert analyze_multi_block_relations(nono_multi_2) == True
    assert nono_multi_2.rows[0] == [0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1]
    assert nono_multi_2.rows[1] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]
    assert nono_multi_2.rows[2] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]
    assert nono_multi_2.rows[3] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]
