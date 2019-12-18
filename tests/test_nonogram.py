# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import pytest
import nonogram

def test_Nonogram_initialisation():
    nono = nonogram.Nonogram("nonograms/small_1.dat")
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
    assert nono.rowsChanged == []
    assert nono.colsChanged == []
    assert nono.transposed == False    