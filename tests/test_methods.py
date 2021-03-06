# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

from unittest.mock import Mock, call
from lib.nonogram import Nonogram
from lib.methods import push_block_origins, push_block_endings,\
    deduce_new_block_origins, deduce_new_block_endings, fill_between_the_blocks,\
    fill_inside_of_the_blocks, fill_cells_to_the_right, fill_cells_to_the_left,\
    fill_row
from lib.methods import find_min_block_length, analyze_multi_block_in_row,\
    analyze_multi_block_relations

hints1 = [1, 1, 1]
hints2 = [1, 2, 1, 3]
blockOrigins1 = [0, 0, 0]
blockOrigins2 = [0, 0, 0, 0]
blockOrigins3 = [0, 0, 5]
blockOrigins4 = [0, 0, 7, 5]
blockOrigins5 = [0, 2, 4]

def test_push_block_origins():
    assert push_block_origins(hints1, blockOrigins1) == (True, [0, 2, 4])
    assert push_block_origins(hints2, blockOrigins2) == (True, [0, 2, 5, 7])
    assert push_block_origins(hints1, blockOrigins3) == (True, [0, 2, 5])
    assert push_block_origins(hints2, blockOrigins4) == (True, [0, 2, 7, 5])
    assert push_block_origins(hints1, blockOrigins1, index=1) == (True, [0, 0, 2])
    assert push_block_origins(hints1, blockOrigins1, index=2) == (False, [0, 0, 0])
    assert push_block_origins(hints2, blockOrigins4, index=2) == (True, [0, 0, 7, 9])

blockEndings_1 = [8, 8, 8]
blockEndings_2 = [12, 12, 12, 12]
blockEndings_3 = [3, 8, 8]
blockEndings_4 = [8, 5, 12, 12]
    
def test_push_block_endings():
    assert push_block_endings(hints1, blockEndings_1) == (True, [4, 6, 8])
    assert push_block_endings(hints2, blockEndings_2) == (True, [3, 6, 8, 12])
    assert push_block_endings(hints1, blockEndings_3) == (True, [3, 6, 8])
    assert push_block_endings(hints2, blockEndings_4) == (True, [8, 5, 8, 12])
    assert push_block_endings(hints1, blockEndings_1, index=1) == (True, [6, 8, 8])
    assert push_block_endings(hints1, blockEndings_1, index=2) == (False, [8, 8, 8])
    assert push_block_endings(hints2, blockEndings_4, index=2) == (True, [2, 5, 12, 12])
    
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

nono_1 = Nonogram("nonograms/small_1.dat")
nono_2 = Nonogram("nonograms/small_1.dat")
nono_3 = Nonogram("nonograms/small_1.dat")

# This test is implemented in test_nonogram.py
# It is present here just to show initial values of nono
#def test_Nonogram_initialisation():
#    assert nono.nRows == 3
#    assert nono.nCols == 3
#    assert nono.rows == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
#    assert nono.cols == [[0, 0, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
#    assert nono.row_hints == [[2], [2], [1, 1]]
#    assert nono.col_hints == [[1, 1], [2], [2]]
#    assert nono.row_block_origins == [[0], [0], [0, 0]]
#    assert nono.col_block_origins == [[0, 0], [0], [0]]
#    assert nono.row_block_endings == [[2], [2], [2, 2]]
#    assert nono.col_block_endings == [[2, 2], [2], [2]]
#    assert nono.undetermind == 9
#    assert nono.rows_changed == []
#    assert nono.cols_changed == []
#    assert nono.transposed == False  

def test_fill_between_the_blocks():
    nono_1.limits.row_block_origins[2] = [0, 2]
    nono_1.limits.row_block_endings[2] = [0, 2]
    fill_between_the_blocks(nono_1, 2)
    assert nono_1.data.rows[2] == [0, -1, 0, -1]
    
def test_fill_inside_of_the_blocks():
    nono_2.limits.row_block_origins[2] = [0, 2]
    nono_2.limits.row_block_endings[2] = [0, 2]
    fill_inside_of_the_blocks(nono_2, 0)
    fill_inside_of_the_blocks(nono_2, 2)
    assert nono_2.data.rows[0] == [0, 1, 0, -1]
    assert nono_2.data.rows[2] == [1, 0, 1, -1]

def test_fill_row():
    fill_row(nono_3, 0)
    assert nono_3.data.rows == [[0, 1, 0, -1], [0, 0, 0, -1], [0, 0, 0, -1]]
    assert nono_3.data.cols == [[0, 0, 0, -1], [1, 0, 0, -1], [0, 0, 0, -1]]
    assert nono_3.meta_data.progress_tracker.undetermind == 8
    nono_3.limits.row_block_origins[2] = [0, 2]
    nono_3.limits.row_block_endings[2] = [0, 2]
    nono_3.update_plot = Mock()
    # fake figure to fake interactive mode on
    nono_3.mode_data.fig = True
    fill_row(nono_3, 2)
    assert nono_3.data.rows == [[0, 1, 0, -1], [0, 0,  0, -1], [1, -1, 1, -1]]
    assert nono_3.data.cols == [[0, 0, 1, -1], [1, 0, -1, -1], [0,  0, 1, -1]]
    assert nono_3.meta_data.progress_tracker.undetermind == 5
    assert nono_3.update_plot.mock_calls == [call()]

nono_multi_1 = Nonogram("tests/data/nono_test_1.dat")
nono_multi_2 = Nonogram("tests/data/nono_test_1.dat")
nono_multi_3 = Nonogram("tests/data/nono_test_1.dat")
nono_multi_4 = Nonogram("tests/data/nono_test_1.dat")

def test_find_min_block_length():
    nono_multi_1.limits.row_block_origins[0] = [0, 2, 4, 5]
    nono_multi_1.limits.row_block_endings[0] = [3, 5, 7, 9]
    nono_multi_1.data.row_hints[0] = [2, 4, 5, 1]
    assert find_min_block_length(nono_multi_1, 0, 1) == 2
    assert find_min_block_length(nono_multi_1, 0, 2) == 2
    assert find_min_block_length(nono_multi_1, 0, 4) == 4
    assert find_min_block_length(nono_multi_1, 0, 5) == 1

def test_fill_cells_to_the_right():
    nono_multi_2.data.row_hints[1]        = [3, 3]
    nono_multi_2.limits.row_block_origins[1] = [0, 4]
    nono_multi_2.limits.row_block_endings[1] = [6, 10]
    nono_multi_2.data.rows[1] = [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1]

    assert fill_cells_to_the_right(nono_multi_2, 1, 5) == True
    assert nono_multi_2.data.rows[1] == [0, 0, 0, -1, 0, 1, 1, -1, 0, 0, 0, -1]
    
def test_fill_cells_to_the_left():
    nono_multi_3.data.row_hints[1]        = [3, 3]
    nono_multi_3.limits.row_block_origins[1] = [0, 4]
    nono_multi_3.limits.row_block_endings[1] = [6, 10]
    nono_multi_3.data.rows[1] = [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1]

    assert fill_cells_to_the_left(nono_multi_3, 1, 5) == True
    assert nono_multi_3.data.rows[1] == [0, 0, 0, -1, 1, 1, 0, -1, 0, 0, 0, -1]
    
def test_analyze_multi_block_in_row():
    nono_multi_1.data.row_hints[1]        = [3, 3]
    nono_multi_1.limits.row_block_origins[1] = [0, 4]
    nono_multi_1.limits.row_block_endings[1] = [6, 10]
    nono_multi_1.data.rows[1] = [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1]

    assert analyze_multi_block_in_row(nono_multi_1, 1) == True
    assert nono_multi_1.data.rows[1] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]

    nono_multi_1.data.row_hints[2]        = [3, 3]
    nono_multi_1.limits.row_block_origins[2] = [0, 4]
    nono_multi_1.limits.row_block_endings[2] = [6, 10]
    nono_multi_1.data.rows[2] = [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1]

    assert analyze_multi_block_in_row(nono_multi_1, 2) == True
    assert nono_multi_1.data.rows[2] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]

    nono_multi_1.data.row_hints[3]        = [3, 3]
    nono_multi_1.limits.row_block_origins[3] = [0, 4]
    nono_multi_1.limits.row_block_endings[3] = [6, 10]
    nono_multi_1.data.rows[3] = [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1]

    assert analyze_multi_block_in_row(nono_multi_1, 3) == True
    assert nono_multi_1.data.rows[1] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]

    nono_multi_1.data.rows[3] = [1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1]

    assert analyze_multi_block_in_row(nono_multi_1, 3) == False

def test_analyze_multi_block_relations():
    nono_multi_4.data.row_hints        = [[3, 3]] * 4
    nono_multi_4.limits.row_block_origins = [[0, 4 ]] * 4
    nono_multi_4.limits.row_block_endings = [[6, 10]] * 4
    nono_multi_4.data.rows = [[0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1],
                              [0, 0, 0, -1, 0, 1, 0, -1, 0, 0, 0, -1],
                              [0, 0, 0, -1, 1, 0, 0, -1, 0, 0, 0, -1],
                              [0, 0, 0, -1, 0, 0, 1, -1, 0, 0, 0, -1]]

    assert analyze_multi_block_relations(nono_multi_4) == True
    assert nono_multi_4.data.rows[0] == [0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, -1]
    assert nono_multi_4.data.rows[1] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]
    assert nono_multi_4.data.rows[2] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]
    assert nono_multi_4.data.rows[3] == [0, 0, 0, -1, 1, 1, 1, -1, 0, 0, 0, -1]
                                                                               