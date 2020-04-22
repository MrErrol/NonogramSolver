# This part allows to import from main directory
import os
import sys
sys.path.insert(0, os.path.dirname('__file__'))

import lib.nonogram as nonogram


def test_ProgressTracker_initialisation():
    progress = nonogram.ProgressTracker(2, 3)
    assert progress.rowsChanged == {0, 1}
    assert progress.colsChanged == {0, 1, 2}
    assert progress.undetermind == 6
