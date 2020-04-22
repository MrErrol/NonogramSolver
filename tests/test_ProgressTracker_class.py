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


def test_ProgressTracker_transpose():
    progress = nonogram.ProgressTracker(2, 3)
    progress.transpose()
    assert progress.rowsChanged == {0, 1, 2}
    assert progress.colsChanged == {0, 1}


def test_ProgressTracker_copy():
    progress = nonogram.ProgressTracker(2, 3)
    progress_copy = progress.copy()
    assert progress_copy.rowsChanged == progress.rowsChanged
    assert progress_copy.colsChanged == progress.colsChanged
    assert progress_copy.undetermind == progress.undetermind
    assert progress is not progress_copy


def test_ProgressTracker_reset_rows_and_cols():
    progress = nonogram.ProgressTracker(2, 3)
    progress.reset_changed_rows_and_cols()
    assert progress.rowsChanged == set()
    assert progress.colsChanged == set()
    assert progress.undetermind == 6


def test_ProgressTracker_filled_cell():
    progress = nonogram.ProgressTracker(2, 3)
    progress.reset_changed_rows_and_cols()
    progress.filled_cell(0, 1)
    assert progress.rowsChanged == {0}
    assert progress.colsChanged == {1}
    assert progress.undetermind == 5


def test_ProgressTracker_mark_row_as_changed():
    progress = nonogram.ProgressTracker(2, 3)
    progress.reset_changed_rows_and_cols()
    progress.mark_row_as_changed(1)
    assert progress.rowsChanged == {1}


def test_ProgressTracker_mark_col_as_changed():
    progress = nonogram.ProgressTracker(2, 3)
    progress.reset_changed_rows_and_cols()
    progress.mark_col_as_changed(2)
    assert progress.colsChanged == {2}


def test_ProgressTracker_get_rows_changed():
    progress = nonogram.ProgressTracker(2, 3)
    assert progress.get_rows_changed() == progress.rowsChanged


def test_ProgressTracker_get_cols_changed():
    progress = nonogram.ProgressTracker(2, 3)
    assert progress.get_cols_changed() == progress.colsChanged


def test_ProgressTracker_get_number_of_undetermind_cells():
    progress = nonogram.ProgressTracker(2, 3)
    assert progress.get_number_of_undetermind_cells() == progress.undetermind


def test_ProgressTracker_anything_improved():
    progress = nonogram.ProgressTracker(2, 3)
    # since initializition is treated as change
    assert progress.anything_improved() == True
    # reset to unchanged state
    progress.reset_changed_rows_and_cols()
    assert progress.anything_improved() == False
