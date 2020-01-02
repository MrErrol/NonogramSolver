# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
import nonogram

nono = nonogram.Nonogram("nonograms/small_1.dat")

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
    nono.fill_cell(1, 2,  1)
    nono.fill_cell(0, 1, -1)
    assert nono.rows == [[0, -1, 0, -1], [0, 0, 1, -1], [0, 0, 0, -1]]
    assert nono.cols == [[0, 0, 0, -1], [-1, 0, 0, -1], [0, 1, 0, -1]]
    assert nono.undetermind == 7
    with pytest.raises(Exception):
        nono.fill_cell(1, 2, -1)